"""
Author: fengye7 zcj2518529668@163.com
Date: 2025-02-22 15:43:20
LastEditors: fengye7 zcj2518529668@163.com
LastEditTime: 2025-02-22 15:43:32
FilePath: \\GraduationDesign\\model\\nodes.py
nodeType: 

Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
"""

# model/definitions/nodes.py
from typing import List

from numpy import double
from model.definitions.common import CommonNode


class Interface(CommonNode):
    def __init__(self, id: str, name: str, nodeType: str, serviceName: str):
        super().__init__(id, name, nodeType)
        self.serviceName = serviceName  # 所属服务
        self.upstream: List[Interface] = []  # 上游接口
        self.downstream: List[Interface] = []  # 下游接口


class Service(CommonNode):
    def __init__(
        self, id: str, name: str, nodeType: str, system: "System", originalName: str
    ):
        super().__init__(id, name, nodeType)
        self.system = system  # 所属系统
        self.originalName = originalName

        self.healthCore: double = 0.0
        self.errorRate: double = 0.0
        self.responseTime: double = 0.0
        self.throughputCount: double = 0.0

        self.interfaces: dict[str, Interface] = {}


class System(CommonNode):
    def __init__(self, id: str, name: str, nodeType: str = ""):
        super().__init__(id, name, nodeType)
        self.healthCore: double = 0.0
        self.errorRate: double = 0.0
        self.responseTime: double = 0.0
        self.throughputCount: double = 0.0

        self.services: dict[str, Service] = {}


class Story(CommonNode):
    def __init__(
        self,
        id: str,
        name: str,
        nodeType: str,
        systemName: System,
        interfaces: List[Interface],
    ):
        super().__init__(id, name, nodeType)
        self.systemName = systemName  # 所属系统
        self.interfaces: List[Interface] = interfaces
        self.tasks: List[Task] = []


class Requirement(CommonNode):
    def __init__(self, id: str, name: str, nodeType: str, systemName: str):
        super().__init__(id, name, nodeType)
        self.systemName = systemName  # 所属系统
        self.stories: List[Story] = []


class Task(CommonNode):
    STATUS_CHOICES = ["todo", "in_progress", "done"]

    def __init__(self, id: str, name: str, nodeType: str, storyId: str):
        super().__init__(id, name, nodeType, storyId)
        self.storyId = storyId  # 所属故事


class TestReport(CommonNode):
    def __init__(self, id: str, name: str, nodeType: str = ""):
        super().__init__(id, name, nodeType)
