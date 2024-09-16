import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, SAGEConv, GraphConv, global_max_pool, global_mean_pool
from enum import Enum


class DropoutRate(Enum):
    NONE = 0
    RATE_25 = 0.25
    RATE_50 = 0.5
    RATE_75 = 0.75


class GCNConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, dropout_rate=DropoutRate.NONE):
        super(GCNConvBlock, self).__init__()
        self.conv = GCNConv(in_channels, out_channels)
        self.batch_norm = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.dropout = nn.Dropout(dropout_rate.value)

    def forward(self, x, edge_index):
        x = self.conv(x, edge_index)
        x = self.batch_norm(x)
        x = self.relu(x)
        x = self.dropout(x)
        return x


class GCNSum(nn.Module):
    def __init__(self, in_channels_x1, in_channels_x2, out_channels):
        super(GCNSum, self).__init__()
        self.linear_x1 = nn.Linear(in_channels_x1, out_channels)
        self.linear_x2 = nn.Linear(in_channels_x2, out_channels)

    def forward(self, x1, x2):
        x1 = self.linear_x1(x1)
        x2 = self.linear_x2(x2)
        return x1 + x2


class GCNConcat(nn.Module):
    def __init__(self):
        super(GCNConcat, self).__init__()

    def forward(self, x1, x2):
        return torch.cat([x1, x2], dim=1)


class GATBlock(nn.Module):
    def __init__(self, in_channels, out_channels, heads=1, dropout_rate=DropoutRate.NONE):
        super(GATBlock, self).__init__()
        self.conv = GATConv(in_channels, out_channels, heads=heads, dropout=dropout_rate.value)
        self.dropout_rate = dropout_rate.value

    def forward(self, x, edge_index):
        x = self.conv(x, edge_index)
        x = F.elu(x)
        x = F.dropout(x, p=self.dropout_rate, training=self.training)
        return x


class SAGEBlock(nn.Module):
    def __init__(self, in_channels, out_channels, dropout_rate=DropoutRate.NONE):
        super(SAGEBlock, self).__init__()
        self.conv = SAGEConv(in_channels, out_channels)
        self.dropout_rate = dropout_rate.value

    def forward(self, x, edge_index):
        x = self.conv(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout_rate, training=self.training)
        return x


class GraphConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, dropout_rate=DropoutRate.NONE):
        super(GraphConvBlock, self).__init__()
        self.conv = GraphConv(in_channels, out_channels)
        self.dropout_rate = dropout_rate.value

    def forward(self, x, edge_index):
        x = self.conv(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout_rate, training=self.training)
        return x


class GlobalMaxPool(nn.Module):
    def forward(self, x, batch):
        return global_max_pool(x, batch)


class GlobalMeanPool(nn.Module):
    def forward(self, x, batch):
        return global_mean_pool(x, batch)
