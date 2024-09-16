import numpy as np
from src.converters.cgp2gcn import CGP2GCN


class GCNEvaluation:
    def __init__(self, trainer, logger, epoch_num, in_channel, n_class, node_feature_dim):
        self.epoch_num = epoch_num
        self.logger = logger
        self.in_channel = in_channel
        self.n_class = n_class
        self.node_feature_dim = node_feature_dim
        self.trainer = trainer

    def evaluate_model(self, net_list):
        model = CGP2GCN(net_list, in_channel=self.in_channel, n_class=self.n_class, node_feature_dim=self.node_feature_dim)
        self.logger.info("Starting training on GPU")

        trained_model, accuracy, history = self.trainer(
            model=model,
            epochs=self.epoch_num
        )

        self.logger.info(f"Finished training on GPU with accuracy: {accuracy}")
        return accuracy

    def __call__(self, net_lists):
        evaluations = np.zeros(len(net_lists))
        for i in range(len(net_lists)):
            evaluations[i] = self.evaluate_model(net_lists[i])
        return evaluations
