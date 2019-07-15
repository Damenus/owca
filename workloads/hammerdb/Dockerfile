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


# Building rpc-perf.
FROM centos:7 AS hammerdb

RUN yum update -y
RUN yum install -y wget

RUN wget -O /HammerDB-3.2.tar.gz https://sourceforge.net/projects/hammerdb/files/HammerDB/HammerDB-3.2/HammerDB-3.2-Linux.tar.gz/download
RUN tar -zxvf HammerDB-3.2.tar.gz
WORKDIR /HammerDB-3.2
ENTRYPOINT ./hammerdbcli
