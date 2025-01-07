import json

import pandas as pd


def collect_unique_systems(input_file, output_file):
    # 读取 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 提取 mergeNodes 中的系统信息
    merge_nodes = data.get("data", {}).get("mergeNodes", [])
    systems = set()

    for node in merge_nodes:
        if node.get("nodeType") == "system":
            system_id = node.get("id")
            system_name = node.get("name")
            if system_id and system_name:
                systems.add((system_id, system_name))

    # 按 id 排序，写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for system_id, system_name in sorted(systems):
            file.write(f"{system_id}\t{system_name}\n")

    print(f"Collected {len(systems)} unique systems. Output written to {output_file}.")


# input_file = "../data/博瑞数据.json"  # 替换为你的 JSON 文件路径
# output_file = "unique_systems.txt"  # 输出的 txt 文件路径
# collect_unique_systems(input_file, output_file)


def collect_unique_components(input_file, output_file):
    # 读取 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 提取 mergeNodes 中的组件信息
    merge_nodes = data.get("data", {}).get("mergeNodes", [])
    components = set()

    for node in merge_nodes:
        component_id = node.get("id")
        component_name = node.get("name")
        if component_id and component_name:
            components.add((component_id, component_name))

    # 按 id 排序，写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for component_id, component_name in sorted(components):
            file.write(f"{component_id}\t{component_name}\n")

    print(f"Collected {len(components)} unique components. Output written to {output_file}.")


# input_file = "../data/组件拓扑.json"  # 替换为你的 JSON 文件路径
# output_file = "unique_components.txt"  # 输出的 txt 文件路径
# collect_unique_components(input_file, output_file)


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


collect_unique_systems_from_requirements("../data/需求数据.xls", "unique_requirements_systems.txt")
