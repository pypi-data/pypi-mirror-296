import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from enum import Enum


class DropoutRate(Enum):
    NONE = 0
    RATE_25 = 0.25
    RATE_50 = 0.5
    RATE_75 = 0.75


class ConvBlock(nn.Module):
    def __init__(self, in_size, out_size, kernel, stride, dropout_rate=DropoutRate.NONE):
        super(ConvBlock, self).__init__()
        pad_size = kernel // 2
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_size, out_size, kernel, stride=stride, padding=pad_size, bias=False),
            nn.BatchNorm2d(out_size),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_rate.value)
        )

    def forward(self, inputs):
        return self.conv1(inputs)


class ResBlock(nn.Module):
    def __init__(self, in_size, out_size, kernel, stride, dropout_rate=DropoutRate.NONE):
        super(ResBlock, self).__init__()
        pad_size = kernel // 2
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_size, out_size, kernel, stride=stride, padding=pad_size, bias=False),
            nn.BatchNorm2d(out_size),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_rate.value),
            nn.Conv2d(out_size, out_size, kernel, stride=stride, padding=pad_size, bias=False),
            nn.BatchNorm2d(out_size),
            nn.Dropout(dropout_rate.value)
        )
        self.relu = nn.ReLU(inplace=True)

    def forward(self, inputs1, inputs2):
        x = self.conv1(inputs1)
        in_data = [x, inputs2]
        small_ch_id, large_ch_id = (0, 1) if in_data[0].size(1) < in_data[1].size(1) else (1, 0)
        offset = int(in_data[large_ch_id].size(1) - in_data[small_ch_id].size(1))
        if offset != 0:
            tmp = in_data[large_ch_id][:, :offset, :, :].clone()
            in_data[small_ch_id] = torch.cat([in_data[small_ch_id], tmp * 0], dim=1)
        return self.relu(torch.add(in_data[0], in_data[1]))


class Sum(nn.Module):
    def __init__(self):
        super(Sum, self).__init__()

    def forward(self, inputs1, inputs2):
        in_data = [inputs1, inputs2]
        small_in_id, large_in_id = (0, 1) if in_data[0].size(2) < in_data[1].size(2) else (1, 0)
        pool_num = math.floor(in_data[large_in_id].size(2) / in_data[small_in_id].size(2))
        for _ in range(pool_num - 1):
            in_data[large_in_id] = F.max_pool2d(in_data[large_in_id], 2, 2, 0)
        small_ch_id, large_ch_id = (0, 1) if in_data[0].size(1) < in_data[1].size(1) else (1, 0)
        offset = in_data[large_ch_id].size(1) - in_data[small_ch_id].size(1)
        if offset > 0:
            tmp = in_data[large_ch_id][:, :offset, :, :].clone()
            in_data[small_ch_id] = torch.cat([in_data[small_ch_id], tmp * 0], dim=1)
        return torch.add(in_data[0], in_data[1])


class Concat(nn.Module):
    def __init__(self):
        super(Concat, self).__init__()

    def forward(self, inputs1, inputs2):
        in_data = [inputs1, inputs2]
        small_in_id, large_in_id = (0, 1) if in_data[0].size(2) < in_data[1].size(2) else (1, 0)
        pool_num = math.floor(in_data[large_in_id].size(2) / in_data[small_in_id].size(2))
        for _ in range(pool_num - 1):
            in_data[large_in_id] = F.max_pool2d(in_data[large_in_id], 2, 2, 0)
        return torch.cat([in_data[0], in_data[1]], 1)


class MaxPoolingBlock(nn.Module):
    def __init__(self, kernel_size, stride=None, padding=0):
        super(MaxPoolingBlock, self).__init__()
        self.pool = nn.MaxPool2d(kernel_size, stride=stride, padding=padding)

    def forward(self, x):
        return self.pool(x)


class AvgPoolingBlock(nn.Module):
    def __init__(self, kernel_size, stride=None, padding=0):
        super(AvgPoolingBlock, self).__init__()
        self.pool = nn.AvgPool2d(kernel_size, stride=stride, padding=padding)

    def forward(self, x):
        return self.pool(x)
