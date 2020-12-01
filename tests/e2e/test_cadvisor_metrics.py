from requests import get
from time import time

import logging
import os
import pytest


_PROMETHEUS_QUERY_PATH = "/api/v1/query"
_PROMETHEUS_QUERY_RANGE_PATH = "/api/v1/query_range"
_PROMETHEUS_URL_TPL = '{prometheus}{path}?query={name}'
_PROMETHEUS_TIME_TPL = '&start={start}&end={end}&step=1s'
_PROMETHEUS_TAG_TPL = '{key}="{value}"'


def _build_prometheus_url(prometheus, name, tags=None, window_size=None, event_time=None):
    tags = tags or dict()
    path = _PROMETHEUS_QUERY_PATH
    time_range = ''

    # Some variables need to be overwritten for range queries.
    if window_size and event_time:
        offset = window_size / 2
        time_range = _PROMETHEUS_TIME_TPL.format(
            start=event_time - offset,
            end=event_time + offset)
        path = _PROMETHEUS_QUERY_RANGE_PATH

    url = _PROMETHEUS_URL_TPL.format(
        prometheus=prometheus,
        path=path,
        name=name,
    )

    # Prepare additional tags for query.
    query_tags = []
    for k, v in tags.items():
        query_tags.append(_PROMETHEUS_TAG_TPL.format(key=k, value=v))
    query_tags_str = ','.join(query_tags)

    # Build final URL from all the components.
    url = ''.join([url, "{", query_tags_str, "}", time_range])
    logging.info('Prometheus query: %s', ''.join([url, "{", query_tags_str, "}"]))

    return url


def _fetch_metrics(url):
    response = get(url)
    response.raise_for_status()
    return response.json()


def test_cadvisor(workload_name, metrics):
    # app wss, mem bandwith, cos z offcore, czy jest up cpu, upmem cap, mbw flat
    metrics = ['app_wss',
               'app_mem',
               #'pod_memory_rw_ratio'
               ]
    workload_name = 'redis-memtier-small'

    prometheus = 'http://100.64.176.35:30900'
    tags = dict(app=workload_name)

    for metric in metrics:
        metric_query = _build_prometheus_url(prometheus, metric,
                                             tags, 1800, time())
        fetched_metric = _fetch_metrics(metric_query)
        assert len(fetched_metric['data']['result']) > 0, \
            'queried prometheus for {} metrics produced by workload ' \
            '{} and did not received any'.format(metric, workload_name)


if __name__ == '__main__':
    test_cadvisor("", "")
