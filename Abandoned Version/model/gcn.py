import json
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import torch.nn.functional as F


# Step 1: 解析 JSON 数据
def parse_json_to_graph(json_data):
    nodes = json_data["data"]['mergeNodes'] + json_data["data"]['nodes']
    edges = json_data["data"]['mergeEdges']

    # 节点特征矩阵（特征: healthScore, throughputRate, responseTime）
    node_features = []
    node_ids = {}  # 节点ID映射到索引
    for idx, node in enumerate(nodes):
        node_ids[node['id']] = idx
        metric = node['metricInfo']
        node_features.append([
            metric.get('healthScore', 0) or 0,
            metric.get('throughputRate', 0) or 0,
            metric.get('responseTime', 0) or 0
        ])

    # 边索引矩阵
    edge_index = []
    edge_weights = []
    for edge in edges:
        from_idx = node_ids[edge['from']]
        to_idx = node_ids[edge['to']]
        edge_index.append([from_idx, to_idx])
        edge_weights.append(edge.get('requestCount', 1) or 0)  # 边权重为 requestCount

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()  # 转置为 (2, num_edges)
    edge_weights = torch.tensor(edge_weights, dtype=torch.float)
    node_features = torch.tensor(node_features, dtype=torch.float)

    return Data(x=node_features, edge_index=edge_index, edge_attr=edge_weights)


# 示例 JSON 数据（替换为你的实际数据）
with open('../data/博瑞数据.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

graph_data = parse_json_to_graph(json_data)


# Step 2: 定义 GCN 模型
class GCNModel(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GCNModel, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, x, edge_index, edge_weight=None):
        x = self.conv1(x, edge_index, edge_weight=edge_weight)
        x = F.relu(x)
        x = self.conv2(x, edge_index, edge_weight=edge_weight)
        return F.log_softmax(x, dim=1)


# Step 3: 训练模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GCNModel(input_dim=3, hidden_dim=16, output_dim=3).to(device)  # 输入维度3, 输出3类分类
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
    print(f'Epoch {epoch + 1}, Loss: {loss.item():.4f}')

# Step 4: 测试模型
model.eval()
_, pred = model(data.x, data.edge_index, data.edge_attr).max(dim=1)
print("Predictions:", pred)
