import numpy as np
from src.converters.cgp2cnn import CGP2CNN
from src.blocks.cnn_blocks import DropoutRate
import torch.optim as optim
from enum import Enum
import time


class OptimizerType(Enum):
    ADAM = 'Adam'
    SGD = 'SGD'
    RMSPROP = 'RMSprop'


class SchedulerType(Enum):
    STEP_LR = "step_lr"
    REDUCE_LR_ON_PLATEAU = "reduce_lr_on_plateau"
    COSINE_ANNEALING = "cosine_annealing"


class CNNEvaluation:
    def __init__(self, trainer, logger, epoch_num, in_channel, n_class, imgSize, criterion, learning_rate, optimizer_type, scheduler_type):
        self.epoch_num = epoch_num
        self.logger = logger
        self.in_channel = in_channel
        self.n_class = n_class
        self.imgSize = imgSize
        self.trainer = trainer
        self.criterion = criterion
        self.learning_rate = learning_rate
        self.optimizer_type = optimizer_type
        self.scheduler_type = scheduler_type

    def configure_optimizer(self, model):
        if self.optimizer_type == OptimizerType.ADAM:
            return optim.Adam(model.parameters(), lr=self.learning_rate, betas=(0.5, 0.999))
        elif self.optimizer_type == OptimizerType.SGD:
            return optim.SGD(model.parameters(), lr=self.learning_rate, momentum=0.9)
        elif self.optimizer_type == OptimizerType.RMSPROP:
            return optim.RMSprop(model.parameters(), lr=self.learning_rate)
        else:
            raise ValueError(f"Unsupported optimizer: {self.optimizer_type}")

    def configure_scheduler(self, optimizer):
        if self.scheduler_type == SchedulerType.STEP_LR:
            return optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
        elif self.scheduler_type == SchedulerType.REDUCE_LR_ON_PLATEAU:
            return optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.1, patience=5)
        elif self.scheduler_type == SchedulerType.COSINE_ANNEALING:
            return optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
        else:
            return None

    def evaluate_model(self, model):
        self.logger.info("Starting training on GPU")

        criterion = self.criterion
        optimizer = self.configure_optimizer(model)
        scheduler = self.configure_scheduler(optimizer)

        trained_model, train_losses, val_losses, val_accuracies, accuracy, avg_loss, all_preds, all_targets = self.trainer(model, self.epoch_num, criterion, optimizer, scheduler)

        self.logger.info(f"Finished training on GPU with accuracy: {accuracy}")
        return accuracy

    def __call__(self, net_lists):
        start_time = time.time()
        self.logger.info("Starting the evaluation of multiple models")

        evaluations = np.zeros(len(net_lists))
        for i in range(len(net_lists)):
            evaluations[i] = self.evaluate_model(CGP2CNN(net_lists[i], self.in_channel, self.n_class, self.imgSize, DropoutRate.NONE))

        end_time = time.time()
        duration = end_time - start_time
        self.logger.info(f"Evaluation of all models completed in {duration:.2f} seconds")

        return evaluations
