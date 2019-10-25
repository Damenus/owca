# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import time
from typing import Dict, Union, List, Tuple, Callable

from dataclasses import dataclass, field
from enum import Enum

log = logging.getLogger(__name__)


class MetricName(str, Enum):
    # Perf events based.
    # Per task
    INSTRUCTIONS = 'instructions'
    CYCLES = 'cycles'
    CACHE_MISSES = 'cache_misses'
    CACHE_REFERENCES = 'cache_references'
    MEMSTALL = 'stalls_mem_load'
    OFFCORE_REQUESTS_OUTSTANDING_L3_MISS_DEMAND_DATA_RD = \
        'offcore_requests_outstanding_l3_miss_demand_data_rd'
    OFFCORE_REQUESTS_L3_MISS_DEMAND_DATA_RD = 'offcore_requests_l3_miss_demand_data_rd'

    # Extra perf based.
    SCALING_FACTOR_AVG = 'scaling_factor_avg'
    SCALING_FACTOR_MAX = 'scaling_factor_max'

    # Cgroup based.
    CPU_USAGE_PER_TASK = 'cpu_usage_per_task'
    MEM_USAGE_PER_TASK = 'memory_usage_per_task_bytes'
    MEM_MAX_USAGE_PER_TASK = 'memory_max_usage_per_task_bytes'
    MEM_LIMIT_PER_TASK = 'memory_limit_per_task_bytes'
    MEM_SOFT_LIMIT_PER_TASK = 'memory_soft_limit_per_task_bytes'
    MEM_NUMA_STAT_PER_TASK = 'memory_numa_stat'
    MEM_PAGE_FAULTS = 'memory_stat_page_faults'

    # NUMA for whole platform
    MEM_NUMA_FREE = 'memory_numa_free'
    MEM_NUMA_USED = 'memory_numa_used'

    # Generic per task.
    LAST_SEEN = 'last_seen'
    CPUS = 'cpus'  # From Kubernetes or Mesos
    MEM = 'mem'  # From Kubernetes or Mesos

    # Resctrl based.
    MEM_BW = 'memory_bandwidth'
    LLC_OCCUPANCY = 'llc_occupancy'
    MEMORY_BANDWIDTH_LOCAL = 'memory_bandwidth_local'
    MEMORY_BANDWIDTH_REMOTE = 'memory_bandwidth_remote'

    # /proc based (platform scope).
    #
    # Utilization (usage):
    # counter like, sum of all modes based on /proc/stat
    # "cpu line" with 10ms resolution expressed in [ms]
    CPU_USAGE_PER_CPU = 'cpu_usage_per_cpu'
    # [bytes] based on /proc/meminfo (gauge like)
    # difference between MemTotal and MemAvail (or MemFree)
    MEM_USAGE = 'memory_usage'

    # Generic for WCA.
    UP = 'up'


class DerivedMetricName(str, Enum):
    # instructions/second
    IPS = 'ips'
    # instructions/cycle
    IPC = 'ipc'
    # (cache-references - cache_misses) / cache_references
    CACHE_HIT_RATIO = 'cache_hit_ratio'
    # (cache-references - cache_misses) / cache_references
    CACHE_MISSES_PER_KILO_INSTRUCTIONS = 'cache_misses_per_kilo_instructions'


class MetricType(str, Enum):
    GAUGE = 'gauge'  # arbitrary value (can go up and down)
    COUNTER = 'counter'  # monotonically increasing counter

    def __repr__(self):
        return repr(self.value)


MetricValue = Union[float, int]


# Order is enabled to allow sorting metrics according their metadata.
@dataclass(order=True)
class MetricMetadata:
    type: MetricType
    help: str


# Structure linking a metric with description of chierarchy how it is kept.
METRICS_LEVELS = {
    MetricName.MEM_NUMA_STAT_PER_TASK: ["numa_node"],
    MetricName.MEM_NUMA_FREE: ["numa_node"],
    MetricName.MEM_NUMA_USED: ["numa_node"],
    MetricName.CPU_USAGE_PER_CPU: ["cpu"],
}

# Structure linking a metric with its type and help.
METRICS_METADATA: Dict[MetricName, MetricMetadata] = {
    MetricName.INSTRUCTIONS:
        MetricMetadata(
            MetricType.COUNTER,
            'Linux Perf counter for instructions per container.'),
    MetricName.CYCLES:
        MetricMetadata(
            MetricType.COUNTER,
            'Linux Perf counter for cycles per container.'),
    MetricName.CACHE_MISSES:
        MetricMetadata(
            MetricType.COUNTER,
            'Linux Perf counter for cache-misses per container.'),
    MetricName.CPU_USAGE_PER_CPU:
        MetricMetadata(
            MetricType.COUNTER,
            '[1/USER_HZ] Logical CPU usage in 1/USER_HZ (usually 10ms).'
            'Calculated using values based on /proc/stat'),
    MetricName.CPU_USAGE_PER_TASK:
        MetricMetadata(
            MetricType.COUNTER,
            '[ns] cpuacct.usage (total kernel and user space)'),
    MetricName.MEM_BW:
        MetricMetadata(
            MetricType.COUNTER,
            '[bytes] Total memory bandwidth using Memory Bandwidth Monitoring.'),
    MetricName.MEM_USAGE_PER_TASK:
        MetricMetadata(
            MetricType.GAUGE,
            '[bytes] Memory usage_in_bytes per tasks returned from cgroup memory subsystem.'),
    MetricName.MEM_MAX_USAGE_PER_TASK:
        MetricMetadata(
            MetricType.GAUGE,
            '[bytes] Memory max_usage_in_bytes per tasks returned from cgroup memory subsystem.'),
    MetricName.MEM_LIMIT_PER_TASK:
        MetricMetadata(
            MetricType.GAUGE,
            '[bytes] Memory limit_in_bytes per tasks returned from cgroup memory subsystem.'),
    MetricName.MEM_SOFT_LIMIT_PER_TASK:
        MetricMetadata(
            MetricType.GAUGE,
            '[bytes] Memory soft_limit_in_bytes per tasks returned from cgroup memory subsystem.'),
    MetricName.LLC_OCCUPANCY:
        MetricMetadata(
            MetricType.GAUGE,
            '[bytes] LLC occupancy'),
    MetricName.MEM_USAGE:
        MetricMetadata(
            MetricType.GAUGE,
            '[bytes] Total memory used by platform in bytes based on /proc/meminfo '
            'and uses heuristic based on linux free tool (total - free - buffers - cache).'
        ),
    MetricName.MEMSTALL:
        MetricMetadata(
            MetricType.COUNTER,
            'Mem stalled loads'
        ),
    MetricName.CACHE_REFERENCES:
        MetricMetadata(
            MetricType.COUNTER,
            'Cache references'
        ),
    MetricName.SCALING_FACTOR_MAX:
        MetricMetadata(
            MetricType.GAUGE,
            'Perf metric scaling factor, MAX value'
        ),
    MetricName.SCALING_FACTOR_AVG:
        MetricMetadata(
            MetricType.GAUGE,
            'Perf metric scaling factor, average from all CPUs'
        ),
    MetricName.MEM_NUMA_STAT_PER_TASK:
        MetricMetadata(
            MetricType.GAUGE,
            'NUMA Stat TODO!',  # TODO: fix me!
        ),
    MetricName.MEM_PAGE_FAULTS:
        MetricMetadata(
            MetricType.COUNTER,
            'Page faults',  # TODO: fix me!
        ),
    MetricName.MEM_NUMA_FREE:
        MetricMetadata(
            MetricType.GAUGE,
            'NUMA memory free per numa node TODO!',  # TODO: fix me!
        ),
    MetricName.MEM_NUMA_USED:
        MetricMetadata(
            MetricType.GAUGE,
            'NUMA memory used per numa node TODO!',  # TODO: fix me!
        ),
    MetricName.MEMORY_BANDWIDTH_LOCAL:
        MetricMetadata(
            MetricType.COUNTER,
            '[bytes] Total local memory bandwidth using Memory Bandwidth Monitoring.'
        ),
    MetricName.MEMORY_BANDWIDTH_REMOTE:
        MetricMetadata(
            MetricType.COUNTER,
            '[bytes] Total remote memory bandwidth using Memory Bandwidth Monitoring.'
        ),
    MetricName.OFFCORE_REQUESTS_L3_MISS_DEMAND_DATA_RD:
        MetricMetadata(
            MetricType.COUNTER,
            'Increment each cycle of the number of offcore outstanding demand data read '
            'requests from SQ that missed L3.'
        ),
    MetricName.OFFCORE_REQUESTS_OUTSTANDING_L3_MISS_DEMAND_DATA_RD:
        MetricMetadata(
            MetricType.COUNTER,
            'Demand data read requests that missed L3.'
        ),
    MetricName.CPUS:
        MetricMetadata(
            MetricType.GAUGE,
            'Tasks resources cpus initial requests.',
        ),
    MetricName.MEM:
        MetricMetadata(
            MetricType.GAUGE,
            'Tasks resources memory initial requests.'
        ),
    MetricName.LAST_SEEN:
        MetricMetadata(
            MetricType.COUNTER,
            'Time the task was last seen.'
        ),
    MetricName.UP:
        MetricMetadata(
            MetricType.COUNTER,
            'Time the was was last seen.'
        ),
    DerivedMetricName.IPC:
        MetricMetadata(
            MetricType.GAUGE,
            'Instructions per cycle'
        ),
    DerivedMetricName.IPS:
        MetricMetadata(
            MetricType.GAUGE,
            'Instructions per second'
        ),
    DerivedMetricName.CACHE_HIT_RATIO:
        MetricMetadata(
            MetricType.GAUGE,
            'Cache hit ratio, based on cache-misses and cache-references',
        ),
    DerivedMetricName.CACHE_MISSES_PER_KILO_INSTRUCTIONS:
        MetricMetadata(
            MetricType.GAUGE,
            'Cache misses per kilo instructions',
        ),
}


@dataclass
class Metric:
    name: Union[str, MetricName]
    value: MetricValue
    labels: Dict[str, str] = field(default_factory=dict)
    type: MetricType = None
    help: str = None

    @staticmethod
    def create_metric_with_metadata(name, value, labels=None):
        metric = Metric(
            name=name,
            value=value,
            labels=labels or dict()
        )
        if name in METRICS_METADATA:
            metric.type = METRICS_METADATA[name].type
            metric.help = METRICS_METADATA[name].help
        # TODO: add else, cannot be None type and help
        return metric


Measurements = Dict[MetricName, MetricValue]


def merge_measurements(measurements_list: List[Measurements]) -> \
        Tuple[Measurements, List[MetricName]]:
    """Returns dictionary with metrics which are contained in all input measurements with value set
       to arithmetic sum."""
    summed_metrics: Measurements = {}

    all_metrics_names = set()  # Sum of set of names.
    for measurements in measurements_list:
        all_metrics_names.update(measurements.keys())

    for metric_name in all_metrics_names:
        if metric_name in METRICS_METADATA:

            if METRICS_METADATA[metric_name].type == MetricType.GAUGE:
                operation = lambda values: sum(values) / len(values)  # noqa
            else:
                assert METRICS_METADATA[metric_name].type == MetricType.COUNTER
                operation = sum

        else:
            log.debug('By default, unknown metric %r uses "sum" as merge operation.', metric_name)
            operation = sum

        summed_metrics[metric_name] = operation(
            [measurements[metric_name] for measurements in measurements_list
             if metric_name in measurements])

    return summed_metrics


class BaseDerivedMetricsGenerator:
    """ Calculate derived metrics based on predefined rules:

    ipc = instructions / cycle
    ips = instructions / second
    cache_hit_ratio = cache-reference - cache-misses / cache-references
    cache_misses_per_kilo_instructions = cache_misses / (instructions/1000)
    """

    def __init__(self, get_measurements_func: Callable[[], Measurements]):
        self._prev_measurements = None
        self._prev_ts = None
        self.get_measurements_func = get_measurements_func

    def get_measurements(self) -> Measurements:
        measurements = self.get_measurements_func()
        return self._get_measurements_with_derived_metrics(measurements)

    def _get_measurements_with_derived_metrics(self, measurements):
        """Extend given measurements with some derived metrics like IPC, IPS, cache_hit_ratio.
        Extends only if those metrics are enabled in "event_names".
        """

        now = time.time()

        def available(*names):
            return all(name in measurements and name in self._prev_measurements for name in names)

        def delta(*names):
            if not available(*names):
                return 0
            if len(names) == 1:
                name = names[0]
                return measurements[name] - self._prev_measurements[name]
            else:
                return [measurements[name] - self._prev_measurements[name] for name in names]

        # if specific pairs are available calculate derived metrics
        if self._prev_measurements is not None:
            time_delta = now - self._prev_ts
            self._derive(measurements, delta, available, time_delta)

        self._prev_measurements = measurements
        self._prev_ts = now

        return measurements

    def _derive(self, measurements, delta, available, time_delta):
        raise NotImplementedError


class DefaultDerivedMetricsGenerator(BaseDerivedMetricsGenerator):

    def _derive(self, measurements, delta, available, time_delta):

        if available(MetricName.INSTRUCTIONS, MetricName.CYCLES):
            inst_delta, cycles_delta = delta(MetricName.INSTRUCTIONS,
                                             MetricName.CYCLES)
            if cycles_delta > 0:
                measurements[DerivedMetricName.IPC] = float(inst_delta) / cycles_delta

            if time_delta > 0:
                measurements[DerivedMetricName.IPS] = float(inst_delta) / time_delta

        if available(MetricName.INSTRUCTIONS, MetricName.CACHE_MISSES):
            inst_delta, cache_misses_delta = delta(MetricName.INSTRUCTIONS,
                                                   MetricName.CACHE_MISSES)
            if inst_delta > 0:
                measurements[DerivedMetricName.CACHE_MISSES_PER_KILO_INSTRUCTIONS] = \
                    float(cache_misses_delta) * 1000 / inst_delta

        if available(MetricName.CACHE_REFERENCES, MetricName.CACHE_MISSES):
            cache_ref_delta, cache_misses_delta = delta(MetricName.CACHE_REFERENCES,
                                                        MetricName.CACHE_MISSES)
            if cache_ref_delta > 0:
                cache_hits_count = cache_ref_delta - cache_misses_delta
                measurements[DerivedMetricName.CACHE_HIT_RATIO] = (
                        float(cache_hits_count) / cache_ref_delta)


class BaseGeneratorFactory:
    def create(self, get_measurements):
        raise NotImplementedError


class MissingMeasurementException(Exception):
    """when metric has not been collected with success"""
    pass


def export_metrics_from_measurements(name_prefix: str,
                                     measurements: Measurements) -> List[Metric]:
    all_metrics = []
    for metric_name, metric_node in measurements.items():
        if metric_name in METRICS_LEVELS:
            levels = METRICS_LEVELS[metric_name]
            max_depth = len(levels)

            def is_leaf(depth):
                return depth == max_depth

            def create_metric(node, labels):
                return [Metric.create_metric_with_metadata(
                    name=name_prefix + metric_name,
                    value=node,
                    labels=labels
                )]

            def recursive_create_metric(node, parent_labels=None, depth=0):
                if is_leaf(depth):
                    return create_metric(node, parent_labels)
                else:
                    metrics = []
                    for parent_label_value, child in node.items():
                        new_parent_labels = {} if parent_labels is None else dict(parent_labels)
                        new_parent_labels[levels[depth]] = str(parent_label_value)
                        metrics.extend(recursive_create_metric(child, new_parent_labels, depth+1))
                    return metrics
            all_metrics.extend(recursive_create_metric(metric_node, {}, 0))
        else:
            metric_value = metric_node
            all_metrics.append(Metric.create_metric_with_metadata(
                name=name_prefix + metric_name,
                value=metric_value,
            ))
    return all_metrics
