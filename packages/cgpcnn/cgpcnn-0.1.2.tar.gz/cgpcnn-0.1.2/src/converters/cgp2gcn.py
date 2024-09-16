import torch.nn as nn
import sys
from src.blocks.gcn_blocks import GCNConvBlock, GCNConcat, GCNSum, GlobalMaxPool, GlobalMeanPool, GATBlock, SAGEBlock, GraphConvBlock, DropoutRate


class CGP2GCN(nn.Module):
    def __init__(self, cgp, in_channel, n_class, node_feature_dim, dropout_rate=DropoutRate.NONE):
        super(CGP2GCN, self).__init__()
        self.cgp = cgp
        self.channel_num = [None for _ in range(500)]
        self.size = [None for _ in range(500)]
        self.channel_num[0] = in_channel
        self.size[0] = node_feature_dim
        self.encode = nn.ModuleList()
        self.n_class = n_class
        self.dropout_rate = dropout_rate
        self._build_network()

    def _build_network(self):
        for i, gene in enumerate(self.cgp):
            if len(gene) == 3:
                name, in1, in2 = gene
            elif len(gene) == 2:
                name, in1 = gene
                in2 = None
            else:
                raise ValueError(f"Unexpected number of elements in gene: {gene}")

            if name == 'input':
                continue
            elif name == 'full':
                self._add_full_layer(i, in1)
            elif name in ['Max_Pool', 'Avg_Pool']:
                self._add_pooling_layer(i, in1, name)
            elif name == 'GCNConcat':
                self._add_concat_layer(i, in1, in2)
            elif name == 'GCNSum':
                self._add_sum_layer(i, in1, in2)
            else:
                self._add_block_layer(i, name, in1)

    def _add_full_layer(self, i, in1):
        in_features = self.channel_num[in1]
        self.encode.append(nn.Linear(in_features, self.n_class))

    def _add_pooling_layer(self, i, in1, name):
        self.channel_num[i] = self.channel_num[in1]
        self.size[i] = self.size[in1]
        if name == 'Max_Pool':
            self.encode.append(GlobalMaxPool())
        else:
            self.encode.append(GlobalMeanPool())

    def _add_concat_layer(self, i, in1, in2):
        if in2 is None:
            raise ValueError(f"Concat operation requires two input indices, got: {in1}")
        self.channel_num[i] = self.channel_num[in1] + self.channel_num[in2]
        self.size[i] = self.size[min(in1, in2, key=lambda x: self.size[x])]
        self.encode.append(GCNConcat())

    def _add_sum_layer(self, i, in1, in2):
        if in2 is None:
            raise ValueError(f"Sum operation requires two input indices, got: {in1}")
        out_channels = max(self.channel_num[in1], self.channel_num[in2])
        self.channel_num[i] = out_channels
        self.size[i] = self.size[min(in1, in2, key=lambda x: self.size[x])]
        self.encode.append(GCNSum(self.channel_num[in1], self.channel_num[in2], out_channels))

    def _add_block_layer(self, i, name, in1):
        try:
            down, func, out_size = name.split('_')
            out_size = int(out_size)
        except ValueError:
            raise ValueError(f"Invalid format for operation name: {name}")

        if down == 'S':
            if func == 'GCNConvBlock':
                self.channel_num[i] = out_size
                self.size[i] = self.size[in1]
                self.encode.append(GCNConvBlock(self.channel_num[in1], out_size, dropout_rate=self.dropout_rate))
            elif func == 'GATBlock':
                self.channel_num[i] = out_size
                self.size[i] = self.size[in1]
                self.encode.append(GATBlock(self.channel_num[in1], out_size, dropout_rate=self.dropout_rate))
            elif func == 'SAGEBlock':
                self.channel_num[i] = out_size
                self.size[i] = self.size[in1]
                self.encode.append(SAGEBlock(self.channel_num[in1], out_size, dropout_rate=self.dropout_rate))
            elif func == 'GraphConvBlock':
                self.channel_num[i] = out_size
                self.size[i] = self.size[in1]
                self.encode.append(GraphConvBlock(self.channel_num[in1], out_size, dropout_rate=self.dropout_rate))
            else:
                raise ValueError(f"Unsupported block type: {func}")
        else:
            raise ValueError(f"Unsupported operation: {down}")

    def forward(self, x, edge_index, batch=None):
        outputs = [None for _ in range(len(self.cgp))]
        outputs[0] = x

        for i, layer in enumerate(self.encode):
            if isinstance(layer, (GCNConvBlock, GATBlock, SAGEBlock, GraphConvBlock)):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]], edge_index)
            elif isinstance(layer, nn.Linear):
                tmp = outputs[self.cgp[i + 1][1]].view(outputs[self.cgp[i + 1][1]].size(0), -1)
                outputs[i + 1] = layer(tmp)
            elif isinstance(layer, (GlobalMaxPool, GlobalMeanPool)):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]], batch)
            elif isinstance(layer, GCNConcat):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]], outputs[self.cgp[i + 1][2]])
            elif isinstance(layer, GCNSum):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]], outputs[self.cgp[i + 1][2]])
            else:
                sys.exit("Error in forward pass of CGP2GCN")

        return outputs[-1]
