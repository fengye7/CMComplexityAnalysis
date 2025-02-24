import json
import random

def load_data(input_file):
    # 读取输入 JSON 文件并返回数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_interfaces(data):
    # 提取所有接口 ID 和名称
    interfaces = []
    for category in data.values():
        for system in category:
            for service in system['services']:
                for interface in service['interfaces']:
                    interfaces.append({
                        'id': interface['id'],
                        'name': interface['name']
                    })
    return interfaces

def generate_mock_relations(interfaces, num_relations):
    """
    生成指定数量的 mock 关系，确保没有重复或自引用关系，并添加重要性属性。

    参数：
    interfaces (list): 接口列表，每个接口应包含 'id' 字段。
    num_relations (int): 要生成的关系数量。

    返回：
    list: 包含关系和重要性属性的字典列表。
    """
    relations = set()
    while len(relations) < num_relations:
        from_interface = random.choice(interfaces)
        to_interface = random.choice(interfaces)
        if from_interface['id'] != to_interface['id']:
            relation = (from_interface['id'], to_interface['id'])
            relations.add(relation)

    # 生成关系并添加 requestCount 属性
    return [{'from': f, 'to': t, 'requestCount': random.randint(1, 500)} for f, t in relations]

def save_relations(output_file, relations):
    # 将生成的关系保存到输出 JSON 文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(relations, f, ensure_ascii=False, indent=2)

def main():
    # 输入 JSON 文件名
    input_file = 'mock_structure.json'
    # 输出 JSON 文件名
    output_file = 'mock_relations.json'
    # 要生成的关系数量
    num_relations = 500

    # 加载数据
    data = load_data(input_file)
    # 提取接口信息
    interfaces = extract_interfaces(data)
    # 生成 mock 关系
    relations = generate_mock_relations(interfaces, num_relations)
    # 保存关系到输出文件
    save_relations(output_file, relations)
    print(f"Mock 关系已生成并保存到 {output_file}")

if __name__ == "__main__":
    main()
