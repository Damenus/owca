# Copyright (C) 2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
#
#
# SPDX-License-Identifier: Apache-2.0

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

    return url


def _fetch_metrics(url):
    response = get(url)
    response.raise_for_status()
    return response.json()


@pytest.mark.parametrize('workload_instance, env_uniq_id', [
    ('cassandra_stress--default--34--9142', '34'),
    ('redis_rpc_perf--default--34--6789', '34'),
    ('twemcache_mutilate--default--34--11211', '34'),
    ('cassandra_ycsb--default--34--9042', '34'),
    ('specjbb--default--34--42000', '34'),
    ('stress_ng--default--34--0', '34'),
    ('twemcache_rpc_perf--default--34--11211', '34')
])
def test_wca_metrics_kubernetes(workload_instance, env_uniq_id):
    assert 'PROMETHEUS' in os.environ, 'prometheus host to connect'
    assert 'BUILD_NUMBER' in os.environ
    assert 'BUILD_COMMIT' in os.environ

    prometheus = os.environ['PROMETHEUS']
    build_number = int(os.environ['BUILD_NUMBER'])
    build_commit = os.environ['BUILD_COMMIT']

    tags = dict(build_number=build_number,
                build_commit=build_commit,
                workload_instance=workload_instance,
                env_uniq_id=env_uniq_id)

    logging.info('build number = %r', build_number)
    prometheus_query = _build_prometheus_url(prometheus, '',
                                             tags, 1800, time())
    metrics = _fetch_metrics(prometheus_query)
    assert len(metrics) > 0


@pytest.mark.parametrize('workload_instance, env_uniq_id', [
    ('stress_ng--default--14--0', '14'),
])
def test_wca_metrics_mesos(workload_instance, env_uniq_id):
    assert 'PROMETHEUS' in os.environ, 'prometheus host to connect'
    assert 'BUILD_NUMBER' in os.environ
    assert 'BUILD_COMMIT' in os.environ

    prometheus = os.environ['PROMETHEUS']
    build_number = int(os.environ['BUILD_NUMBER'])
    build_commit = os.environ['BUILD_COMMIT']

    tags = dict(build_number=build_number,
                build_commit=build_commit,
                workload_instance=workload_instance,
                env_uniq_id=env_uniq_id)

    logging.info('build number = %r', build_number)
    prometheus_query = _build_prometheus_url(prometheus,
                                             tags, 1800, time())
    metrics = _fetch_metrics(prometheus_query)
    assert len(metrics) > 0
