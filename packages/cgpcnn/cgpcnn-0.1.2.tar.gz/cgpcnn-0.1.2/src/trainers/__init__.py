# src/trainers/__init__.py

from .cnn_trainer import CNNTrainer
from .gcn_trainer import GCNTrainer
from .trainer_base import TrainerBase

__all__ = ['CNNTrainer', 'GCNTrainer', 'TrainerBase']
