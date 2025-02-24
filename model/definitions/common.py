"""
Author: fengye7 zcj2518529668@163.com
Date: 2025-02-22 15:54:11
LastEditors: fengye7 zcj2518529668@163.com
LastEditTime: 2025-02-22 16:17:08
FilePath: \\GraduationDesign\\model\\definitions\\common.py
Description: 

Copyright (c) 2025 by ${fengye7}, All Rights Reserved. 
"""


# model/definitions/common.py
class CommonNode:
    def __init__(self, id: str, name: str, nodeType: str = ""):
        self.id = id
        self.name = name
        self.nodeType = nodeType

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}: {self.name}>"
