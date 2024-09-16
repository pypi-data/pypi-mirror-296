import logging
import os
import sys
import torch
from datetime import datetime
from src.utils.singleton import Singleton


class Logger(logging.Logger, metaclass=Singleton):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def __init__(self, name, log_directory, log_file=None, level=logging.INFO):
        super().__init__(name, level)

        if log_file is None:
            log_file = f'log_file_{Logger.current_time}.log'

        self.log_file = log_file

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.addHandler(ch)

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        fh = logging.FileHandler(os.path.join(log_directory, log_file))
        fh.setFormatter(formatter)
        self.addHandler(fh)

        self.info(f'Session start at {Logger.current_time}')
        self.info(f'Session start in {os.path.abspath(os.getcwd())}')

        self.initialize_logging_info()

    def initialize_logging_info(self):
        """Log system and environment information."""
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.info(f"Session started on {device}")
        self.info(f"Number of available CPUs: {os.cpu_count()}")
        self.info(f"Number of available GPUs: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            self.info(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        self.info(f"Python Version: {sys.version}")
        self.info(f"CUDNN Version: {torch.backends.cudnn.version()}")
        self.info(f"PyTorch Version: {torch.__version__}")
