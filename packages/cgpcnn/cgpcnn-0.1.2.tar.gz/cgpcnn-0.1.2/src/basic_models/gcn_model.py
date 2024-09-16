import torch
import torch.nn.functional as F
from torch.nn import Module, Linear
from torch_geometric.nn import GCNConv, GATConv


class SimpleGCN(Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleGCN, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)


class GCNBasicModel(Module):
    def __init__(self, input_dim, hidden_dim1, hidden_dim2, output_dim):
        super(GCNBasicModel, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim1)
        self.conv2 = GCNConv(hidden_dim1, hidden_dim2)
        self.fc = Linear(hidden_dim2, output_dim)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        return F.log_softmax(self.fc(x), dim=1)


class GATBasicModel(Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_heads=8, num_layers=3):
        super(GATBasicModel, self).__init__()
        self.layers = torch.nn.ModuleList()
        self.layers.append(GATConv(input_dim, hidden_dim, heads=num_heads))
        for _ in range(num_layers - 2):
            self.layers.append(GATConv(hidden_dim * num_heads, hidden_dim, heads=num_heads))
        self.layers.append(GATConv(hidden_dim * num_heads, output_dim, heads=1))

    def forward(self, x, edge_index):
        for layer in self.layers[:-1]:
            x = F.elu(layer(x, edge_index))
        x = self.layers[-1](x, edge_index)
        return F.log_softmax(x, dim=1)
