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


from io import TextIOWrapper
import logging
from typing import List, Dict

from wca.metrics import Metric, MetricType
from wrapper import wrapper_main
from wrapper.parser import readline_with_check

log = logging.getLogger(__name__)


def parse(input: TextIOWrapper, regexp: str, separator: str = None,
          labels: Dict[str, str] = {}, metric_name_prefix: str = '') -> List[Metric]:
    """Custom parse function for gauge tpm from mysql.
        87060.0
        95220.0
        93600.0
        90000.0
    """
    new_metrics = []

    new_line = readline_with_check(input)

    new_metrics.append(Metric(metric_name_prefix + 'tpm', new_line,
                              type=MetricType.GAUGE, labels=labels,
                              help="TPM (transaction per minute) from mysql"))

    return new_metrics


if __name__ == "__main__":
    wrapper_main.main(parse)
