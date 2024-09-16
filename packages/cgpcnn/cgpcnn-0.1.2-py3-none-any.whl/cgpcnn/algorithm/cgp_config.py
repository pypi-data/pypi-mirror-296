import numpy as np


class CgpConfig:
    def __init__(self, rows, cols, level_back, min_active_num, max_active_num, func_type, func_in_num):
        self.input_num = 1

        self.func_type = func_type
        self.func_in_num = func_in_num

        self.out_num = 1
        self.out_type = ['full']
        self.out_in_num = [1]

        self.rows = rows
        self.cols = cols
        self.node_num = rows * cols
        self.level_back = level_back
        self.min_active_num = min_active_num
        self.max_active_num = max_active_num

        self.func_type_num = len(self.func_type)
        self.out_type_num = len(self.out_type)
        self.max_in_num = max(np.max(self.func_in_num), np.max(self.out_in_num))
