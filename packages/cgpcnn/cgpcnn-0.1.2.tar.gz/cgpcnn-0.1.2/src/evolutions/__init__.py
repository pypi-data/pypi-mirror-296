from .cnn_evolution import CNNEvaluation, OptimizerType, SchedulerType
from .gcn_evolution import GCNEvaluation
from .parallel_evaluation import ParallelEvaluation

__all__ = ['CNNEvaluation', 'GCNEvaluation', 'ParallelEvaluation', 'OptimizerType', 'SchedulerType']
