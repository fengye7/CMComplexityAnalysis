from model.definitions.nodes import (
    Interface,
    Requirement,
    Service,
    System,
    Story,
    Task,
    TestReport,
)
import json
from typing import Tuple, List
from utils import *


def get_nodes_data(
    file_path: str = "data/nodes.json",
) -> Tuple[List[System], List[Service], List[Interface]]:
    """从JSON文件读取节点数据并构建对象关系"""
    systems = []
    services = []
    interfaces = []

    system_relations_path = SYSTEM_RELATIONS_PATH
    service_relations_path = SERVICE_RELATIONS_PATH

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # 先创建所有系统
            system_map = {
                s["id"]: System(id=s["id"], name=s["name"], nodeType="system")
                for s in data.get("systems", [])
            }
            systems = list(system_map.values())

            # 创建服务并关联系统
            service_map = {}
            for svc in data.get("services", []):
                system = system_map.get(svc["system_id"])
                if not system:
                    continue

                service = Service(
                    id=svc["id"],
                    name=svc["name"],
                    nodeType="service",
                    system=system,
                    originalName=svc.get("original_name", ""),
                )
                service_map[svc["id"]] = service
                services.append(service)

                # 关联系统-服务
                system.services[service.id] = service

            # 创建接口并建立调用关系
            interface_map = {}
            for itf in data.get("interfaces", []):
                service = service_map.get(itf["service_id"])
                if not service:
                    continue

                interface = Interface(
                    id=itf["id"],
                    name=itf["name"],
                    nodeType="interface",
                    serviceName=service.name,
                )
                interface.service = service
                interface_map[itf["id"]] = interface
                interfaces.append(interface)

                # 关联服务-接口
                service.interfaces[interface.id] = interface

            # 建立接口调用关系
            for itf in data.get("interfaces", []):
                interface = interface_map.get(itf["id"])
                if not interface:
                    continue

                # 处理上游接口
                for upstream_id in itf.get("upstream", []):
                    if upstream_interface := interface_map.get(upstream_id):
                        interface.upstream.append(upstream_interface)

                # 处理下游接口
                for downstream_id in itf.get("downstream", []):
                    if downstream_interface := interface_map.get(downstream_id):
                        interface.downstream.append(downstream_interface)

    except FileNotFoundError:
        print(f"Warning: Data file {file_path} not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")

    return systems, services, interfaces
