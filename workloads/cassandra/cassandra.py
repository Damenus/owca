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

import os
from common import *

# ----------------------------------------------------------------------------------------------------
###
# Params which can be modified by exporting environment variables.
###

# Port that Cassnadra will bind to.
cassandra_port = os.environ.get('communication_port', '9042')
# ----------------------------------------------------------------------------------------------------

volume = {"name": "shared-data"}

prep_cmd = ["sh", "-c", """
            set -x && \
            cd /prep_config && \
            cp /etc/cassandra/cassandra.yaml . && \
            cp /etc/cassandra/cassandra-env.sh .  \
            && sed -i 's/native_transport_port: 9042/native_transport_port: {cassandra_port}/' cassandra.yaml \
            && export STORAGE_PORT=$(( ( RANDOM  % 10000 )  + 20000 )) \
            && sed -i "s/storage_port: 7000/storage_port: $STORAGE_PORT/" cassandra.yaml \
            && export JMX_PORT=$(( ( RANDOM  % 10000 )  + 20000 )) \
            && sed -i "s/JMX_PORT=\"7199\"/JMX_PORT=\"$JMX_PORT\"/" cassandra-env.sh \
            && cat cassandra.yaml
            """.format(cassandra_port=cassandra_port)]

volume_prep_config = {
    "name": "shared-data",
    "mountPath": "/prep_config"}

initContainer = {
    "name": "prep-config",
    "image": image_name + ":" + image_tag,
    "securityContext": securityContext,
    "command": prep_cmd,
    "volumeMounts": [volume_prep_config]
}

initContainers.append(initContainer)
volumeMounts.append(volume_prep_config)

cmd = "cp /prep_config/cassandra.yaml /etc/cassandra && " \
      "cp /prep_config/cassandra-env.sh /etc/cassandra && " \
      "/docker-entrypoint.sh"
command.append(cmd)

json_format = json.dumps(pod)
print(json_format)

