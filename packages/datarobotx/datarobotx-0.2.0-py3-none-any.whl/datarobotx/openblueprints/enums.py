#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Dict

COLUMN_SELECTORS: Dict[str, str] = {
    "NUM": "make_column_selector(dtype_include=numpy.number)",
    "CAT": "make_column_selector(dtype_include='category')",
    "TXT": "make_column_selector(dtype_include=object)",
    "COUNT_DICT": "make_column_selector(dtype_include=object)",
    "DATE": "make_column_selector(dtype_include=['datetime', 'timedelta'])",
    "DATE_DURATION": "make_column_selector(dtype_include=['datetime.timedelta'])",
    "TARGET_ONLY": "make_column_selector()",
    "GEO": '["GEO_INPUT_COLUMN_NAME"]',
}

PASSTHROUGH_STRING = '"passthrough"'

COPYRIGHT_STRING = """#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
"""
