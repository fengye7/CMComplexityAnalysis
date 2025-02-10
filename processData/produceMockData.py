import json
import random
import pandas as pd


def generate_mock_change_data(systems_file, components_file, requirements_file, stories_file, tasks_file, output_file):
    # 读取系统和组件信息
    with open(systems_file, 'r', encoding='utf-8') as file:
        systems = [line.strip().split('\t') for line in file.readlines()]

    with open(components_file, 'r', encoding='utf-8') as file:
        components = [line.strip().split('\t') for line in file.readlines()]

    # 读取需求、故事、任务信息
    requirements = pd.read_excel(io=requirements_file)
    stories = pd.read_excel(io=stories_file)
    tasks = pd.read_excel(io=tasks_file)

    # 构建需求到故事到任务的映射
    story_to_tasks = tasks.groupby('story_id')['task_id'].apply(list).to_dict()
    requirement_to_stories = stories.groupby('requirement_id')['story_id'].apply(list).to_dict()

    # 生成逻辑性变更数据
    changes = []
    for _, requirement in requirements.iterrows():
        requirement_id = requirement['requirement_id']
        if requirement_id not in requirement_to_stories:
            continue

        for story_id in requirement_to_stories[requirement_id]:
            if story_id not in story_to_tasks:
                continue

            for task_id in story_to_tasks[story_id]:
                system_id, system_name = random.choice(systems)
                component_id, component_name = random.choice(components)
                change = {
                    "change_id": f"CHG{random.randint(1000, 9999)}",
                    "requirement": {
                        "id": requirement_id,
                        "name": requirement['requirement_name']
                    },
                    "story": {
                        "id": story_id,
                        "name": stories[stories['story_id'] == story_id]['story_name'].values[0]
                    },
                    "task": {
                        "id": task_id,
                        "description": tasks[tasks['task_id'] == task_id]['task_description'].values[0]
                    },
                    "system": {"id": system_id, "name": system_name},
                    "component": {"id": component_id, "name": component_name},
                    "description": f"Update {component_name} in {system_name} for task {task_id}",
                    "developer": random.choice(["Alice", "Bob", "Charlie", "David"]),
                    "risk_level": random.choice(["Low", "Medium", "High"]),
                    "expected_downtime": f"{random.randint(0, 60)} minutes",
                }
                changes.append(change)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(changes, file, indent=4, ensure_ascii=False)

    print(f"Generated {len(changes)} mock change records. Output written to {output_file}.")


# 使用示例
systems_file = "unique_systems_mergeNodes.txt"  # 替换为系统文件路径
components_file = "unique_components_mergeNodes.txt"  # 替换为组件文件路径
requirements_file = "../data/需求数据.xls"  # 替换为需求文件路径
stories_file = "../data/story数据.xls"  # 替换为故事文件路径
tasks_file = "../data/task数据.xls"  # 替换为任务文件路径
output_file = "mock_changes.json"  # 输出的 JSON 文件路径
generate_mock_change_data(systems_file, components_file, requirements_file, stories_file, tasks_file, output_file)
