from functools import lru_cache
import networkx as nx
from typing import Dict, List, Set, Optional
from model.definitions.nodes import (
    Interface,
    Requirement,
    Service,
    System,
    Story,
    Task,
    TestReport,
)


class TopologyGraph:
    def __init__(self):
        # 核心拓扑结构
        self.system_graph = nx.DiGraph()  # 系统级拓扑（包含需求数据）
        self.service_dependency_graph = nx.DiGraph()  # 服务级依赖
        self.interface_call_graph = nx.MultiDiGraph()  # 接口级调用

        # 对象存储仓库
        self.systems: Dict[str, System] = {}
        self.services: Dict[str, Service] = {}
        self.interfaces: Dict[str, Interface] = {}
        self.requirements: Dict[str, Requirement] = {}
        self.stories: Dict[str, Story] = {}
        self.tasks: Dict[str, Task] = {}
        self.test_reports: Dict[str, TestReport] = {}

    # ------------------ 基础架构构建方法 ------------------
    def add_system(self, system: System):
        """添加系统节点，初始化健康指标"""
        self.systems[system.id] = system
        self.system_graph.add_node(
            system.id,
            type="system",
            obj=system,
            metrics={
                "healthScore": system.healthCore,
                "errorRate": system.errorRate,
                "responseTime": system.responseTime,
                "throughput": system.throughputCount,
            },
            services=[],
            requirements=[],
        )

    def add_service(self, service: Service):
        """添加服务节点并建立系统-服务包含关系"""
        if service.system.id not in self.systems:
            raise ValueError(f"Parent system {service.system.id} not found")

        self.services[service.id] = service
        self.service_dependency_graph.add_node(
            service.id,
            type="service",
            obj=service,
            system=service.system.id,
            interfaces=[],
            metrics={
                "healthScore": service.healthCore,
                "errorRate": service.errorRate,
                "responseTime": service.responseTime,
                "throughput": service.throughputCount,
            },
        )

        # 更新系统包含关系
        self.system_graph.nodes[service.system.id]["services"].append(service.id)
        self.system_graph.add_edge(
            service.system.id, service.id, rel_type="contains", label="contains_service"
        )

    def add_interface(self, interface: Interface):
        """添加接口节点并处理调用关系"""
        service = interface.service
        if service.id not in self.services:
            raise ValueError(f"Parent service {service.id} not found")

        self.interfaces[interface.id] = interface
        self.interface_call_graph.add_node(
            interface.id,
            type="interface",
            obj=interface,
            service=service.id,
            system=service.system.id,
            call_chains=[],
        )

        # 更新服务接口列表
        self.service_dependency_graph.nodes[service.id]["interfaces"].append(
            interface.id
        )
        self.service_dependency_graph.add_edge(
            service.id, interface.id, rel_type="exposes", label="exposes_interface"
        )

        # 处理调用关系
        self._process_interface_relations(interface)

    def _process_interface_relations(self, interface: Interface):
        """处理接口上下游调用关系"""
        current_service = interface.service

        # 处理上游调用（被哪些接口调用）
        for caller in interface.upstream:
            self._add_call_relation(
                caller, interface, direction="upstream", source_type="interface"
            )

            # 记录跨服务依赖
            if caller.service.id != current_service.id:
                self._add_service_dependency(
                    source_service=caller.service,
                    target_service=current_service,
                    via_interface=interface.id,
                )

        # 处理下游调用（调用哪些接口）
        for callee in interface.downstream:
            self._add_call_relation(
                interface, callee, direction="downstream", source_type="interface"
            )

            # 记录跨服务依赖
            if callee.service.id != current_service.id:
                self._add_service_dependency(
                    source_service=current_service,
                    target_service=callee.service,
                    via_interface=interface.id,
                )

    def _add_call_relation(
        self, source: Interface, target: Interface, direction: str, source_type: str
    ):
        """添加接口调用关系到调用图"""
        is_internal = source.service.id == target.service.id
        self.interface_call_graph.add_edge(
            source.id,
            target.id,
            rel_type="call",
            direction=direction,
            internal=is_internal,
            label=f"{'internal' if is_internal else 'external'}_call",
            call_type=source_type,
        )

        # 记录调用链
        self.interface_call_graph.nodes[source.id]["call_chains"].append(target.id)
        self.interface_call_graph.nodes[target.id]["call_chains"].append(source.id)

    def _add_service_dependency(
        self, source_service: Service, target_service: Service, via_interface: str
    ):
        """记录服务间依赖关系"""
        if not self.service_dependency_graph.has_edge(
            source_service.id, target_service.id
        ):
            self.service_dependency_graph.add_edge(
                source_service.id,
                target_service.id,
                rel_type="depends_on",
                via_interface=via_interface,
                label="service_dependency",
            )

    # ------------------ 需求链路管理 ------------------
    def add_requirement(self, requirement: Requirement):
        """添加完整需求链路（Requirement->Story->Task）"""
        self.requirements[requirement.id] = requirement
        self.system_graph.add_node(
            requirement.id,
            type="requirement",
            obj=requirement,
            system=requirement.systemName,
            stories=[],
        )

        # 关联到所属系统
        if requirement.systemName in self.systems:
            self.system_graph.nodes[requirement.systemName]["requirements"].append(
                requirement.id
            )
            self.system_graph.add_edge(
                requirement.systemName,
                requirement.id,
                rel_type="has_requirement",
                label="system_requirement",
            )

        # 添加关联故事
        for story in requirement.stories:
            self.add_story(story, requirement.id)

    def add_story(self, story: Story, requirement_id: str):
        """添加用户故事及其关联"""
        self.stories[story.id] = story
        self.system_graph.add_node(
            story.id,
            type="story",
            obj=story,
            system=story.systemName.id,
            interfaces=[itf.id for itf in story.interfaces],
            tasks=[],
        )

        # 建立需求-故事关联
        self.system_graph.nodes[requirement_id]["stories"].append(story.id)
        self.system_graph.add_edge(
            requirement_id, story.id, rel_type="contains", label="requirement_story"
        )

        # 关联到接口
        for interface in story.interfaces:
            if interface.id in self.interfaces:
                self.interface_call_graph.nodes[interface.id]["related_stories"].append(
                    story.id
                )
                self.interface_call_graph.add_edge(
                    story.id, interface.id, rel_type="affects", label="story_interface"
                )

        # 添加任务
        for task in story.tasks:
            self.add_task(task, story.id)

    def add_task(self, task: Task, story_id: str):
        """添加开发任务及其关联"""
        self.tasks[task.id] = task
        self.system_graph.add_node(
            task.id,
            type="task",
            obj=task,
            story=story_id,
            status=task.status,
            test_report=task.test_report.id if task.test_report else None,
        )

        # 建立故事-任务关联
        self.system_graph.nodes[story_id]["tasks"].append(task.id)
        self.system_graph.add_edge(
            story_id, task.id, rel_type="contains", label="story_task"
        )

        # 关联测试报告
        if task.test_report:
            self.add_test_report(task.test_report, task.id)

    def add_test_report(self, report: TestReport, task_id: str):
        """添加测试报告关联"""
        self.test_reports[report.id] = report
        self.system_graph.add_node(
            report.id, type="test_report", obj=report, task=task_id
        )
        self.system_graph.add_edge(
            task_id, report.id, rel_type="verified_by", label="task_verification"
        )

    # ------------------ 影响分析增强 ------------------
    @lru_cache(maxsize=1024)
    def analyze_impact(self, target_id: str, max_depth: int = 3) -> Dict[str, List]:
        """增强版影响分析，支持跨层传播"""
        impact = {
            "systems": set(),
            "services": set(),
            "interfaces": set(),
            "requirements": set(),
            "stories": set(),
            "tasks": set(),
            "test_reports": set(),
        }

        # 确定初始搜索图
        if target_id in self.systems:
            graph = self.system_graph
            start_type = "system"
        elif target_id in self.services:
            graph = self.service_dependency_graph
            start_type = "service"
        elif target_id in self.interfaces:
            graph = self.interface_call_graph
            start_type = "interface"
        else:
            raise ValueError("Unsupported target type")

        visited = set()
        queue = [(target_id, 0, start_type)]

        while queue:
            node_id, depth, node_type = queue.pop(0)
            if node_id in visited or depth > max_depth:
                continue
            visited.add((node_id, node_type))

            # 根据节点类型收集影响
            self._collect_impact(node_id, node_type, impact)

            # 获取跨层关联节点
            neighbors = self._get_related_nodes(node_id, node_type)
            queue.extend(
                [
                    (n[0], depth + 1, n[1])
                    for n in neighbors
                    if (n[0], n[1]) not in visited
                ]
            )

        return {k: list(v) for k, v in impact.items()}

    def _collect_impact(self, node_id: str, node_type: str, impact: Dict[str, Set]):
        """根据节点类型收集影响范围"""
        if node_type == "system":
            impact["systems"].add(node_id)
        elif node_type == "service":
            impact["services"].add(node_id)
        elif node_type == "interface":
            impact["interfaces"].add(node_id)
            # 关联需求链路
            if node_id in self.interface_call_graph.nodes:
                for story_id in self.interface_call_graph.nodes[node_id].get(
                    "related_stories", []
                ):
                    impact["stories"].add(story_id)
        elif node_type == "requirement":
            impact["requirements"].add(node_id)
        elif node_type == "story":
            impact["stories"].add(node_id)
        elif node_type == "task":
            impact["tasks"].add(node_id)
        elif node_type == "test_report":
            impact["test_reports"].add(node_id)

    def _get_related_nodes(self, node_id: str, node_type: str) -> List[tuple]:
        """获取跨层关联节点"""
        relations = []

        # 系统级关联
        if node_type == "system":
            # 包含的服务和需求
            relations += [
                (s, "service")
                for s in self.system_graph.nodes[node_id].get("services", [])
            ]
            relations += [
                (r, "requirement")
                for r in self.system_graph.nodes[node_id].get("requirements", [])
            ]

        # 服务级关联
        elif node_type == "service":
            # 包含的接口、依赖的服务
            relations += [
                (i, "interface")
                for i in self.service_dependency_graph.nodes[node_id].get(
                    "interfaces", []
                )
            ]
            relations += [
                (s, "service")
                for s in self.service_dependency_graph.successors(node_id)
            ]
            relations += [
                (s, "service")
                for s in self.service_dependency_graph.predecessors(node_id)
            ]

        # 接口级关联
        elif node_type == "interface":
            # 调用链、所属服务、关联需求
            relations += [
                (s, "interface") for s in self.interface_call_graph.successors(node_id)
            ]
            relations += [
                (s, "interface")
                for s in self.interface_call_graph.predecessors(node_id)
            ]
            relations.append(
                (self.interface_call_graph.nodes[node_id]["service"], "service")
            )
            relations += [
                (s, "story")
                for s in self.interface_call_graph.nodes[node_id].get(
                    "related_stories", []
                )
            ]

        # 需求链路关联
        elif node_type == "requirement":
            relations += [
                (s, "story")
                for s in self.system_graph.nodes[node_id].get("stories", [])
            ]

        # 故事关联
        elif node_type == "story":
            relations += [
                (t, "task") for t in self.system_graph.nodes[node_id].get("tasks", [])
            ]
            relations.append((self.system_graph.nodes[node_id]["system"], "system"))

        # 任务关联
        elif node_type == "task":
            if self.system_graph.nodes[node_id].get("test_report"):
                relations.append(
                    (self.system_graph.nodes[node_id]["test_report"], "test_report")
                )

        return list(set(relations))  # 去重

    # ------------------ 可视化方法 ------------------
    def visualize_topology(self, graph_type: str = "service"):
        """可视化指定层级拓扑结构（TODO: 实现具体可视化逻辑）"""
        pass
