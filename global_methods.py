"""
Author: fengye7 zcj2518529668@163.com
Date: 2025-02-21 11:21:44
LastEditors: fengye7 zcj2518529668@163.com
LastEditTime: 2025-02-22 14:34:10
FilePath: \GraduationDesign\global_methods.py
Description: 
这是工具函数的库
主要包括 json读取，文件路径处理，数据格式处理……

Copyright (c) 2025 by ${fengye7}, All Rights Reserved. 
"""

import json
import os


def path_exists(path):
    """
    Check if the given path exists.

    :param path: The path to check.
    :return: True if the path exists, False otherwise.
    """
    return os.path.exists(path)


def load_json(file_path):
    """
    Load a JSON file.

    :param file_path: The path to the JSON file.
    :return: The loaded JSON data.
    """
    if not path_exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r") as file:
        return json.load(file)
