import time
import torch
from src.trainers.trainer_base import TrainerBase
import matplotlib.pyplot as plt
import os


class GCNTrainer(TrainerBase):
    def __init__(self, data_loader, logger, learning_rate, optimizer_type, criterion, early_stopping, patience, verbose, mlflow_enabled, experiment_name, ml_flow_folder_path, device):
        super().__init__(data_loader, logger, learning_rate, optimizer_type, criterion, early_stopping, patience, mlflow_enabled, experiment_name, ml_flow_folder_path, verbose, device)

    def train(self, model, epochs):
        model.train()

        best_loss = float('inf')
        patience_counter = 0

        train_losses = []
        val_losses = []
        val_accuracies = []

        criterion = self.criterion.to(self.device)
        optimizer = self.configure_optimizer(model)

        start_train = time.time()

        self.logger.info(f"Training for {epochs} epochs.")

        for epoch in range(epochs):
            model.train()
            optimizer.zero_grad()

            out = model(self.data_loader.data.x.to(self.device), self.data_loader.data.edge_index.to(self.device))
            loss = criterion(out[self.data_loader.data.train_mask], self.data_loader.data.y[self.data_loader.data.train_mask].to(self.device))
            loss.backward()
            optimizer.step()

            train_losses.append(loss.item())

            if self.verbose:
                accuracy, val_loss = self.evaluate(model)
                val_losses.append(val_loss)
                val_accuracies.append(accuracy)
                self.logger.info(f'Epoch [{epoch+1}/{epochs}], Train Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {accuracy:.4f}')

            if self.early_stopping:
                if loss.item() < best_loss:
                    best_loss = loss.item()
                    patience_counter = 0
                else:
                    patience_counter += 1
                    self.logger.info(f"Patience counter: {patience_counter}/{self.patience}")
                    if patience_counter >= self.patience:
                        self.logger.info(f"Early stopping triggered at epoch {epoch + 1}")
                        break

        end_train = time.time()
        self.logger.info(f"Training completed in {end_train - start_train:.2f} seconds.")

        return model, train_losses, val_losses, val_accuracies

    def evaluate(self, model):
        model.eval()
        total_loss = 0
        criterion = self.criterion.to(self.device)
        start_eval = time.time()
        with torch.no_grad():
            out = model(self.data_loader.data.x.to(self.device), self.data_loader.data.edge_index.to(self.device))
            loss = criterion(out[self.data_loader.data.test_mask], self.data_loader.data.y[self.data_loader.data.test_mask].to(self.device))
            total_loss += loss.item()
            pred = out.argmax(dim=1)
            test_correct = pred[self.data_loader.data.test_mask] == self.data_loader.data.y[self.data_loader.data.test_mask].to(self.device)
            accuracy = int(test_correct.sum()) / int(self.data_loader.data.test_mask.sum())
        end_eval = time.time()
        self.logger.info(f"Evaluation completed in {end_eval - start_eval:.2f} seconds")
        return accuracy, total_loss

    def predict(self, model, x, edge_index):
        model = model.to(self.device)
        model.eval()

        with torch.no_grad():
            out = model(x.to(self.device), edge_index.to(self.device))
            predicted = out.argmax(dim=1)

        return predicted.cpu().numpy()

    def __call__(self, model, epochs):
        model = model.to(self.device)
        trained_model, train_losses, val_losses, val_accuracies = self.train(model, epochs)
        accuracy, total_loss = self.evaluate(trained_model)

        return trained_model, accuracy, total_loss, train_losses, val_losses, val_accuracies

    def save_model_and_results(self, model, name, result_folder_path, train_losses, val_losses, val_accuracies):
        self.save_model(model, name, result_folder_path)

        plt.figure(figsize=(10, 5))
        plt.plot(train_losses, label='Train Loss')
        plt.plot(val_losses, label='Validation Loss')
        plt.title(f'Train vs Validation Loss for {name}')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig(os.path.join(result_folder_path, f'{name}_train_val_loss.png'))
        plt.close()

        plt.figure(figsize=(10, 5))
        plt.plot(val_accuracies, label='Validation Accuracy')
        plt.title(f'Validation Accuracy for {name}')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.savefig(os.path.join(result_folder_path, f'{name}_val_accuracy.png'))
        plt.close()

        self.logger.info(f"Model and results saved to {result_folder_path}")
