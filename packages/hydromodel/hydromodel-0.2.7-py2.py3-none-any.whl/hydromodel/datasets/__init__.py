"""
Author: Wenyu Ouyang
Date: 2024-08-14 16:34:32
LastEditTime: 2024-08-15 12:01:25
LastEditors: Wenyu Ouyang
Description: Some common functions and variables for datasets.
FilePath: \hydromodel\hydromodel\datasets\__init__.py
Copyright (c) 2023-2024 Wenyu Ouyang. All rights reserved.
"""

from hydrodataset import Camels
from hydrodatasource.reader.data_source import SelfMadeHydroDataset

PRCP_NAME = "prcp(mm/day)"
PET_NAME = "pet(mm/day)"
ET_NAME = "et(mm/day)"
FLOW_NAME = "flow(m^3/s)"
NODE_FLOW_NAME = "node1_flow(m^3/s)"
AREA_NAME = "area(km^2)"
TIME_NAME = "time"
POSSIBLE_TIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S",  # 完整的日期和时间
    "%Y-%m-%d",  # 只有日期
    "%d/%m/%Y",  # 不同的日期格式
    "%m/%d/%Y %H:%M",  # 月/日/年 小时:分钟
    "%d/%m/%Y %H:%M",  # 日/月/年 小时:分钟
    # ... 可以根据需要添加更多格式 ...
]
ID_NAME = "id"
NAME_NAME = "name"


def remove_unit_from_name(name_with_unit):
    """
    Remove the unit from a variable name.

    Parameters
    ----------
    name_with_unit : str
        The name of the variable including its unit, e.g., "prcp(mm/day)".

    Returns
    -------
    str
        The name of the variable without the unit, e.g., "prcp".
    """
    return name_with_unit.split("(")[0]


def get_unit_from_name(name_with_unit):
    """
    Extract the unit from a variable name.

    Parameters
    ----------
    name_with_unit : str
        The name of the variable including its unit, e.g., "prcp(mm/day)".

    Returns
    -------
    str
        The unit of the variable, e.g., "mm/day".
    """
    return name_with_unit.split("(")[1].strip(")") if "(" in name_with_unit else ""


datasource_dict = {
    "camels": Camels,
    "selfmadehydrodataset": SelfMadeHydroDataset,
}

datasource_vars_dict = {
    # all vars are in the sequence of [pr, pet, flow] with different names
    "camels": ["prcp", "PET", "streamflow"],
    "selfmadehydrodataset": [
        "total_precipitation_hourly",
        "potential_evaporation_hourly",
        "streamflow",
    ],
}
