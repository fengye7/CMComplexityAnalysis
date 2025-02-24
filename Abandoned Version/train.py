"""
Author: fengye7 zcj2518529668@163.com
Date: 2024-12-30 19:59:12
LastEditors: fengye7 zcj2518529668@163.com
LastEditTime: 2025-02-22 15:46:00
FilePath: \GraduationDesign\Abandoned Version\train.py
Description: 

Copyright (c) 2025 by ${fengye7}, All Rights Reserved. 
"""

import json
import torch

from common import parse_json_to_graph
from model.gcn import GCNModel

# 示例 JSON 数据（替换为你的实际数据）
with open("system_topology.json", "r") as f:
    json_data = json.load(f)

graph_data = parse_json_to_graph(json_data)


# Step 3: 训练模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = GCNModel(input_dim=3, hidden_dim=16, output_dim=3).to(
    device
)  # 输入维度3, 输出3类分类
data = graph_data.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
criterion = torch.nn.CrossEntropyLoss()

# 示例标签（根据任务定义标签）
data.y = torch.randint(0, 3, (data.x.size(0),)).to(device)  # 随机生成示例标签

for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index, data.edge_attr)
    loss = criterion(out, data.y)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch + 1}, Loss: {loss.item():.4f}")

# Step 4: 测试模型
model.eval()
_, pred = model(data.x, data.edge_index, data.edge_attr).max(dim=1)
print("Predictions:", pred)
