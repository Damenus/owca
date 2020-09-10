
from typing import Dict, List, Tuple
from analyzer.connection import PrometheusClient
from analyzer.model import Task, Node
from analyzer.metrics import Metric, MetricsQueries, Function, FunctionsDescription


def build_function_call_id(function: Function, arg: str):
    return "{}{}".format(FunctionsDescription[function], str(arg))


class AnalyzerQueries:
    """Class used for namespace"""

    @staticmethod
    def query_tasks_list(time) -> Dict[str, Task]:
        query_result = PrometheusClient.instant_query(MetricsQueries[Metric.TASK_UP], time)
        tasks = {}
        for metric in query_result:
            metric = metric['metric']
            task_name = metric['task_name']
            tasks[task_name] = Task(metric['task_name'], metric['app'],
                                    metric['nodename'])
        return tasks

    @staticmethod
    def query_platform_performance_metrics(time: int, nodes: Dict[str, Node], window_length: int = 120):
        # very important parameter - window_length [s]

        metrics = (Metric.PLATFORM_MEM_USAGE, Metric.PLATFORM_CPU_REQUESTED,
                   Metric.PLATFORM_CPU_UTIL, Metric.PLATFORM_MBW_TOTAL,
                   Metric.POD_SCHEDULED, Metric.PLATFORM_DRAM_HIT_RATIO, Metric.PLATFORM_WSS_USED)

        for metric in metrics:
            query_results = PrometheusClient.instant_query(MetricsQueries[metric], time)
            descr = metric.value
            for result in query_results:
                nodes[result['metric']['nodename']].performance_metrics[metric] = {'instant': result['value'][1]}

    @staticmethod
    def query_performance_metrics(time: int, functions_args: List[Tuple[Function, str]],
                                  metrics: List[Metric], window_length: int) -> Dict[str, Dict]:
        """performance metrics which needs aggregation over time"""
        query_results: Dict[Metric, Dict] = {}
        for metric in metrics:
            for function, arguments in functions_args:
                query_template = "{function}({arguments}{prom_metric}[{window_length}s])"
                query = query_template.format(function=function.value,
                                              arguments=arguments,
                                              window_length=window_length,
                                              prom_metric=MetricsQueries[metric])
                query_result = PrometheusClient.instant_query(query, time)
                aggregation_name = build_function_call_id(function, arguments)

                if metric in query_results:
                    query_results[metric][aggregation_name] = query_result
                else:
                    query_results[metric] = {aggregation_name: query_result}
        return query_results

    @staticmethod
    def query_task_performance_metrics(time: int, tasks: Dict[str, Task], window_length: int = 120):

        metrics = (Metric.TASK_THROUGHPUT, Metric.TASK_LATENCY)

        function_args = ((Function.AVG, ''), (Function.QUANTILE, '0.1,'),
                         (Function.QUANTILE, '0.9,'),)

        query_results = AnalyzerQueries.query_performance_metrics(time, function_args, metrics, window_length)
        for metric, query_result in query_results.items():
            for aggregation_name, result in query_result.items():
                for per_app_result in result:
                    task_name = per_app_result['metric']['task_name']
                    value = per_app_result['value'][1]
                    if metric in tasks[task_name].performance_metrics:
                        tasks[task_name].performance_metrics[metric][aggregation_name] = value
                    else:
                        tasks[task_name].performance_metrics[metric] = {aggregation_name: value}