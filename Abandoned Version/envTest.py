#1、测试Pytorch 2.1.0
import torch
print(torch.__version__)
#2.1.0

#2、测试CUDA 10.1
import torch
print(torch.cuda.is_available())
# True

from torch_geometric.data import Data

edge_index = torch.tensor([[0, 1, 1, 2],
                           [1, 0, 2, 1]], dtype=torch.long)
x = torch.tensor([[-1], [0], [1]], dtype=torch.float)

data = Data(x=x, edge_index=edge_index)
print(data)
# Data(x=[3, 1], edge_index=[2, 4])
