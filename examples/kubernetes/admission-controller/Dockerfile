# Copyright (c) 2020 Intel Corporation
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
# limitations under the License

FROM centos:7

WORKDIR /admission-controller

RUN yum -y install python36 python-pip which make

# Prepare Python environment.
COPY Makefile Makefile
COPY requirements.txt requirements.txt
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
RUN make venv
ENV PYTHONPATH=/admission-controller

# Prepare admission-controller files
COPY wca ./wca
COPY examples/kubernetes/admission-controller/keys ./ssl/
COPY examples/kubernetes/admission-controller/config.yaml /etc/admission-controller/config.yaml
