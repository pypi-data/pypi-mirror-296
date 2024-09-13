# coding=utf-8
# Copyright (c) 2023-2024 Huawei Technologies Co., Ltd.
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

import logging


def get_logger():
    llm_logger = logging.getLogger("msit_convert_logger")
    llm_logger.propagate = False
    llm_logger.setLevel(logging.INFO)
    if not llm_logger.handlers:
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s-pid: %(process)d-[%(levelname)s]-%(name)s-%(message)s')
        stream_handler.setFormatter(formatter)
        llm_logger.addHandler(stream_handler)
    return llm_logger


logger = get_logger()


LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "fatal": logging.FATAL,
    "notset": logging.NOTSET,
    "critical": logging.CRITICAL
}


def set_log_level(level="info"):
    if level.lower() in LOG_LEVELS:
        logger.setLevel(LOG_LEVELS.get(level.lower()))
    else:
        logger.warning("Set %s log level failed.", level)
