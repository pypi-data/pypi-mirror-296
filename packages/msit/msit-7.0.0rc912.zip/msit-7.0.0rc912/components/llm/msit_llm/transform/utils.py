# Copyright (c) 2024-2024 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import stat
from msit_llm.common.log import logger
from collections import namedtuple

_SCENARIOS = ["torch_to_float_atb", "float_atb_to_quant_atb", "torch_to_float_python_atb"]
SCENARIOS = namedtuple("SCENARIOS", _SCENARIOS)(*_SCENARIOS)


def get_transform_scenario(source_path, to_python=False):
    if os.path.isfile(source_path) and source_path.endswith(".cpp"):  # Single cpp input
        return SCENARIOS.float_atb_to_quant_atb

    try:
        from transformers.configuration_utils import PretrainedConfig

        _ = PretrainedConfig.get_config_dict(source_path)
        return SCENARIOS.torch_to_float_python_atb if to_python else SCENARIOS.torch_to_float_atb
    except Exception:
        pass  # Not an error

    if os.path.isdir(source_path) and any([ii.endswith(".cpp") for ii in os.listdir(source_path)]):
        return SCENARIOS.float_atb_to_quant_atb
    else:
        return None


def write_file(save_path, string):
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    modes = stat.S_IWUSR | stat.S_IRUSR
    with os.fdopen(os.open(save_path, flags, modes), 'w') as ff:
        ff.write(string)