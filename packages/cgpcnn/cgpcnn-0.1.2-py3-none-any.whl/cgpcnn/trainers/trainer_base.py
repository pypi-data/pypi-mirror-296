import torch
import os
import mlflow
import mlflow.pytorch
from abc import ABC, abstractmethod


class TrainerBase(ABC):
    def __init__(self, data_loader, logger, early_stopping, patience, mlflow_enabled, experiment_name, ml_flow_folder_path, verbose, device):
        self.data_loader = data_loader
        self.logger = logger
        self.early_stopping = early_stopping
        self.patience = patience
        self.mlflow_enabled = mlflow_enabled
        self.experiment_name = experiment_name
        self.ml_flow_folder_path = ml_flow_folder_path
        self.verbose = verbose
        self.device = device

        if self.mlflow_enabled:
            self.init_mlflow()

    def init_mlflow(self) -> None:
        encoded_uri = '/'.join(mlflow.get_tracking_uri().split("/")[:-1] + [self.ml_flow_folder_path])
        mlflow.set_tracking_uri(encoded_uri)
        mlflow.set_experiment(self.experiment_name)
        self.logger.info(f"MLflow configured with tracking URI: {encoded_uri} and experiment name: {self.experiment_name}")

    def save_model(self, model, name, result_folder_path):
        model_path = os.path.join(result_folder_path, f'{name}.pth')
        torch.save(model.state_dict(), model_path)
        self.logger.info(f"Model saved to {model_path}")

        if self.mlflow_enabled:
            mlflow.pytorch.log_model(model, 'model')

    @abstractmethod
    def train(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for training the model.
        """
        pass

    @abstractmethod
    def validate(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for validating the model during training.
        """
        pass

    @abstractmethod
    def test(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for evaluating the model.
        """
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for making predictions on a batch of images.
        """
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for calling the object directly.
        """
        pass
