import torch.nn as nn
import sys
from src.blocks.cnn_blocks import ConvBlock, ResBlock, Sum, Concat, MaxPoolingBlock, AvgPoolingBlock


class CGP2CNN(nn.Module):
    def __init__(self, cgp, in_channel, n_class, imgSize, dropout_rate):
        super(CGP2CNN, self).__init__()
        self.cgp = cgp
        self.channel_num = [None for _ in range(500)]
        self.size = [None for _ in range(500)]
        self.channel_num[0] = in_channel
        self.size[0] = imgSize
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
            elif name == 'Concat':
                self._add_concat_layer(i, in1, in2)
            elif name == 'Sum':
                self._add_sum_layer(i, in1, in2)
            else:
                self._add_block_layer(i, name, in1)

    def _add_full_layer(self, i, in1):
        self.encode.append(nn.Linear(self.channel_num[in1] * self.size[in1] * self.size[in1], self.n_class))

    def _add_pooling_layer(self, i, in1, name):
        self.channel_num[i] = self.channel_num[in1]
        self.size[i] = self.size[in1] // 2
        if name == 'Max_Pool':
            self.encode.append(MaxPoolingBlock(kernel_size=2, stride=2))
        elif name == 'Avg_Pool':
            self.encode.append(AvgPoolingBlock(kernel_size=2, stride=2))
        else:
            raise ValueError(f"Unsupported pooling type: {name}")

    def _add_concat_layer(self, i, in1, in2):
        if in2 is None:
            raise ValueError(f"Concat operation requires two input indices, got: {in1}")
        self.channel_num[i] = self.channel_num[in1] + self.channel_num[in2]
        self.size[i] = self.size[min(in1, in2, key=lambda x: self.size[x])]
        self.encode.append(Concat())

    def _add_sum_layer(self, i, in1, in2):
        if in2 is None:
            raise ValueError(f"Sum operation requires two input indices, got: {in1}")
        self.channel_num[i] = max(self.channel_num[in1], self.channel_num[in2])
        self.size[i] = self.size[min(in1, in2, key=lambda x: self.size[x])]
        self.encode.append(Sum())

    def _add_block_layer(self, i, name, in1):
        try:
            down, func, out_size, kernel = name.split('_')
            out_size, kernel = int(out_size), int(kernel)
        except ValueError:
            raise ValueError(f"Invalid format for operation name: {name}")

        if down == 'S':
            if func == 'ConvBlock':
                self.channel_num[i] = out_size
                self.size[i] = self.size[in1]
                self.encode.append(ConvBlock(self.channel_num[in1], out_size, kernel, stride=1, dropout_rate=self.dropout_rate))
            elif func == 'ResBlock':
                self.channel_num[i] = max(out_size, self.channel_num[in1])
                self.size[i] = self.size[in1]
                self.encode.append(ResBlock(self.channel_num[in1], out_size, kernel, stride=1, dropout_rate=self.dropout_rate))
            else:
                raise ValueError(f"Unsupported block type: {func}")
        else:
            raise ValueError(f"Unsupported operation: {down}")

    def forward(self, x):
        outputs = [None for _ in range(len(self.cgp))]
        outputs[0] = x
        for i, layer in enumerate(self.encode):
            if isinstance(layer, ConvBlock):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]])
            elif isinstance(layer, ResBlock):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]], outputs[self.cgp[i + 1][1]])
            elif isinstance(layer, nn.Linear):
                tmp = outputs[self.cgp[i + 1][1]].view(outputs[self.cgp[i + 1][1]].size(0), -1)
                outputs[i + 1] = layer(tmp)
            elif isinstance(layer, (MaxPoolingBlock, AvgPoolingBlock)):
                if outputs[self.cgp[i + 1][1]].size(2) > 1:
                    outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]])
                else:
                    outputs[i + 1] = outputs[self.cgp[i + 1][1]]
            elif isinstance(layer, Concat):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]], outputs[self.cgp[i + 1][2]])
            elif isinstance(layer, Sum):
                outputs[i + 1] = layer(outputs[self.cgp[i + 1][1]], outputs[self.cgp[i + 1][2]])
            else:
                sys.exit("Error in forward pass of CGP2CNN")
        return outputs[-1]
