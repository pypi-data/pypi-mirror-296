import torch.optim as optim
import copy
import logging
from multiprocessing import Process, Queue
from src.converters.cgp2cnn import CGP2CNN
from src.blocks.cnn_blocks import DropoutRate
from src.evolutions.cnn_evolution import OptimizerType, SchedulerType
from src.utils.set_seed import set_seed, SEED
import time


def train_model_in_process(trainer, model, epoch_num, criterion, optimizer, scheduler, queue, idx, seed):
    set_seed(seed)

    logger = logging.getLogger(f'logger_process_{idx}')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    trainer.logger = logger

    trained_model, train_losses, val_losses, val_accuracies, accuracy, avg_loss, all_preds, all_targets = trainer(model, epoch_num, criterion, optimizer, scheduler)

    queue.put((idx, accuracy))


class ParallelEvaluation:
    def __init__(self, trainer, epoch_num, in_channel, n_class, imgSize, criterion, learning_rate, optimizer_type, scheduler_type, logger):
        self.epoch_num = epoch_num
        self.in_channel = in_channel
        self.n_class = n_class
        self.imgSize = imgSize
        self.trainer = trainer
        self.criterion = criterion
        self.learning_rate = learning_rate
        self.optimizer_type = optimizer_type
        self.scheduler_type = scheduler_type
        self.logger = logger
        new_logger = logging.getLogger('logger')
        new_logger.setLevel(logging.INFO)
        self.trainer.logger = new_logger
        self.trainer.data_loader.logger = new_logger

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

    def evaluate_models(self, models):
        processes = []
        results_queue = Queue()

        trainers_list = []
        for i in range(len(models)):
            cnn_trainer_copy = copy.deepcopy(self.trainer)
            cnn_trainer_copy.device = f'cuda:{i}'
            trainers_list.append(cnn_trainer_copy)

        for i, model in enumerate(models):
            criterion = copy.deepcopy(self.criterion)
            optimizer = self.configure_optimizer(model)
            scheduler = self.configure_scheduler(optimizer)

            process = Process(
                target=train_model_in_process,
                args=(trainers_list[i], model, self.epoch_num, criterion, optimizer, scheduler, results_queue, i, SEED)
            )
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        results = [None] * len(models)
        while not results_queue.empty():
            idx, accuracy = results_queue.get()
            results[idx] = accuracy

        return results

    def __call__(self, net_lists):
        start_time = time.time()
        self.logger.info(f"Starting the evaluation of {len(net_lists)} models")

        models = []
        for i in range(len(net_lists)):
            models.append(CGP2CNN(cgp=net_lists[i], in_channel=self.in_channel, n_class=self.n_class, imgSize=self.imgSize, dropout_rate=DropoutRate.NONE))

        results = self.evaluate_models(models)

        end_time = time.time()
        duration = end_time - start_time
        self.logger.info(f"Models evaluation completed in {duration:.2f} seconds")

        return results
