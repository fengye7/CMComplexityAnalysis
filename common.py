import json
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import torch.nn.functional as F


# Step 1: 解析 JSON 数据
def parse_json_to_graph(json_data):
    nodes = json_data['mergeNodes']
    edges = json_data['mergeEdges']

    # 节点特征矩阵（特征: healthScore, throughputRate, responseTime）
    node_features = []
    node_ids = {}  # 节点ID映射到索引
    for idx, node in enumerate(nodes):
        node_ids[node['id']] = idx
        metric = node['metricInfo']
        node_features.append([
            metric.get('healthScore', 0),
            metric.get('throughputRate', 0),
            metric.get('responseTime', 0)
        ])

    # 边索引矩阵
    edge_index = []
    edge_weights = []
    for edge in edges:
        from_idx = node_ids[edge['from']]
        to_idx = node_ids[edge['to']]
        edge_index.append([from_idx, to_idx])
        edge_weights.append(edge.get('requestCount', 1))  # 边权重为 requestCount

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()  # 转置为 (2, num_edges)
    edge_weights = torch.tensor(edge_weights, dtype=torch.float)
    node_features = torch.tensor(node_features, dtype=torch.float)

    return Data(x=node_features, edge_index=edge_index, edge_attr=edge_weights)
