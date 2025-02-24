import json
from collections import defaultdict

import pandas as pd


import json
from collections import defaultdict

def collect_unique_systems_by_nodetype(input_file, output_file):
    """
    收集博瑞数据中的所有 mergeNodes 信息，并按 nodetype 分类
    :param input_file: 输入的 JSON 文件路径
    :param output_file: 输出的 TXT 文件路径
    :return: None
    """
    # 读取 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 提取 mergeNodes 中的系统信息并按 nodetype 分类
    merge_nodes = data.get("data", {}).get("mergeNodes", [])
    systems_by_nodetype = defaultdict(set)

    for node in merge_nodes:
        system_id = node.get("id")
        system_name = node.get("name")
        node_type = node.get("nodeType")
        if system_id and system_name and node_type:
            systems_by_nodetype[node_type].add((system_id, system_name))

    # 将数据写入文件，按 nodetype 分类
    with open(output_file, 'w', encoding='utf-8') as file:
        for nodetype, systems in systems_by_nodetype.items():
            file.write(f"NodeType: {nodetype}\n")
            for system_id, system_name in sorted(systems):
                file.write(f"ID: {system_id}\tName: {system_name}\n")
            file.write("\n")

    print(f"Collected unique systems categorized by nodetype. Output written to {output_file}.")


def collect_unique_components_by_nodetype(input_file, output_file):
    """
    收集组件拓扑中的所有 mergeNodes，并按 nodetype 分类
    :param input_file: 输入的 JSON 文件路径
    :param output_file: 输出的 TXT 文件路径
    :return: None
    """
    # 读取 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 提取 mergeNodes 中的组件信息并按 nodetype 分类
    merge_nodes = data.get("data", {}).get("mergeNodes", [])
    components_by_nodetype = defaultdict(set)

    for node in merge_nodes:
        component_id = node.get("id")
        component_name = node.get("name")
        node_type = node.get("nodeType")
        if component_id and component_name and node_type:
            components_by_nodetype[node_type].add((component_id, component_name))

    # 将数据写入文件，按 nodetype 分类
    with open(output_file, 'w', encoding='utf-8') as file:
        for nodetype, components in components_by_nodetype.items():
            file.write(f"NodeType: {nodetype}\n")
            for component_id, component_name in sorted(components):
                file.write(f"ID: {component_id}\tName: {component_name}\n")
            file.write("\n")

    print(f"Collected unique components categorized by nodetype. Output written to {output_file}.")


def collect_unique_systems_from_requirements(requirements_file, output_file):
    # 读取需求 Excel 文件
    requirements = pd.read_excel(requirements_file)

    # 提取"所属系统"列中的系统名称，去重
    systems = set(requirements['所属系统'].dropna().unique())

    # 按名称排序，写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for system in sorted(systems):
            file.write(f"{system}\n")

    print(f"Collected {len(systems)} unique systems. Output written to {output_file}.")


# collect_unique_systems_from_requirements("../data/需求数据.xls", "unique_requirements_systems.txt")


def collect_and_write_json_nodes(json_file_path, output_file_path):
    """
    收集博瑞数据中所有的nodes信息
    :param json_file_path:
    :param output_file_path:
    :return:
    """
    # 使用默认字典来按nodetype分类存储数据
    data_by_nodetype = defaultdict(set)

    # 从文件中读取JSON数据
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        nodes = data.get("data", {}).get("nodes", [])

        # 遍历所有节点，收集id, name, nodetype
        for node in nodes:
            node_id = node.get("id")
            node_name = node.get("name")
            node_type = node.get("nodeType")

            if node_id and node_name and node_type:
                # 按nodetype分类存储id和name
                data_by_nodetype[node_type].add((node_id, node_name))

    # 将收集的数据写入到TXT文件中
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for nodetype, values in data_by_nodetype.items():
            output_file.write(f"NodeType: {nodetype}\n")
            for node_id, node_name in values:
                output_file.write(f"ID: {node_id}, Name: {node_name}\n")
            output_file.write("\n")


# # 调用函数，指定输入JSON文件和输出TXT文件路径
# collect_unique_systems_by_nodetype('../data/博瑞数据.json', 'unique_systems_mergeNodes.txt')
# collect_unique_components_by_nodetype('../data/组件拓扑.json', 'unique_components_mergeNodes.txt')
# collect_and_write_json_nodes('../data/组件拓扑.json', 'unique_components_nodes.txt')
# # collect_and_write_json_nodes('../data/博瑞数据.json', 'unique_systems_nodes.txt')

def collect_systemList(input_file, output_file, node_type):
    """
    收集系统列表
    :param input_file: 输入的 JSON 文件路径
    :param output_file: 输出的 TXT 文件路径
    :param node_type: 'nodes' 或 'mergeNodes'
    :return: None
    """
    with open(output_file, 'w', encoding='utf-8') as w_file:
        # 从文件中读取 JSON 数据
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            nodes = data.get("data", {}).get(node_type, [])

            # 遍历所有节点，收集 id, name, nodetype
            for node in nodes:
                node_systemList = node.get("systemList", [])
                if node_systemList:
                    node_id = node.get("id", "")
                    node_name = node.get("name", "")
                    node_nodetype = node.get("nodeType", "")
                    
                    # 提取字典中的某个键值并将其转换为字符串
                    node_systemList_str = ", ".join(
                        [str(system.get('id', '')) for system in node_systemList]
                    )

                    # 写入文件
                    w_file.write(f"{node_id}\t{node_name}\t{node_nodetype}\t{node_systemList_str}\n")

# 调用函数
collect_systemList('../data/博瑞数据.json', 'unique_systems_systemList_mergeNodes.txt', 'mergeNodes')
collect_systemList('../data/博瑞数据.json', 'unique_systems_systemList_nodes.txt', 'nodes')
collect_systemList('../data/组件拓扑.json', 'unique_components_systemList_mergeNodes.txt', 'mergeNodes')
collect_systemList('../data/组件拓扑.json', 'unique_components_systemList_nodes.txt', 'nodes')
