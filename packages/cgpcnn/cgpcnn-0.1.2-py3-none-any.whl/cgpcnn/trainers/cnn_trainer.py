import time
import torch
import os
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from src.trainers.trainer_base import TrainerBase


class CNNTrainer(TrainerBase):
    def __init__(self, data_loader, logger, channel, imgSize, early_stopping, patience, batchsize, verbose, mlflow_enabled, experiment_name, ml_flow_folder_path, device):
        super().__init__(data_loader, logger, early_stopping, patience, mlflow_enabled, experiment_name, ml_flow_folder_path, verbose, device)

        self.channel = channel
        self.imgSize = imgSize
        self.batchsize = batchsize

    def train(self, model, epochs, criterion, optimizer, scheduler):
        model.train()

        best_loss = float('inf')
        patience_counter = 0

        train_losses = []
        val_losses = []
        val_accuracies = []

        start_train = time.time()

        self.logger.info(f"Training for {epochs} epochs.")

        for epoch in range(epochs):
            losses = []
            running_loss = 0.0
            for batch_idx, (images, labels) in enumerate(self.data_loader.train_loader):
                images, labels = images.to(self.device), labels.to(self.device)
                optimizer.zero_grad()

                outputs = model(images)
                loss = criterion(outputs, labels)
                losses.append(loss.item())

                loss.backward()
                optimizer.step()

                running_loss += loss.item()

                if batch_idx % 100 == 0 and batch_idx > 0:
                    self.logger.info(f'Loss [{epoch+1}, {batch_idx}] (epoch, minibatch): {running_loss / 100}') if self.verbose else None
                    running_loss = 0.0

            avg_loss = sum(losses) / len(losses)

            if self.verbose:
                val_accuracy, val_loss, _, _ = self.test(model, criterion)
                val_losses.append(val_loss)
                val_accuracies.append(val_accuracy)
                self.logger.info(f'Epoch [{epoch+1}/{epochs}] - Train Loss: {avg_loss:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy * 100:.2f}%')

            if scheduler is not None:
                scheduler.step(avg_loss)
                self.logger.info(f"Final hyperparameters: Learning rate: {optimizer.param_groups[0]['lr']}, Momentum: {optimizer.param_groups[0].get('momentum', 'N/A')}, Weight decay: {optimizer.param_groups[0]['weight_decay']}")

            train_losses.append(avg_loss)

            if self.early_stopping:
                if val_loss < best_loss:
                    best_loss = val_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= self.patience:
                        self.logger.info(f"Early stopping triggered at epoch {epoch + 1}")
                        break

        end_train = time.time()

        self.logger.info(f"Training completed in {end_train - start_train:.2f} seconds.")

        return model, train_losses, val_losses, val_accuracies

    def validate(self, model, criterion):
        model.eval()

        total = 0
        correct = 0
        total_loss = 0

        start_eval = time.time()

        with torch.no_grad():
            for images, labels in self.data_loader.val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                total_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        end_eval = time.time()
        avg_loss = total_loss / len(self.data_loader.val_loader)
        accuracy = correct / total

        self.logger.info(f"Validate completed in {end_eval - start_eval:.2f} seconds, with accuracy: {accuracy * 100:.2f}%")

        return accuracy, avg_loss

    def test(self, model, criterion):
        model.eval()

        total = 0
        correct = 0
        total_loss = 0

        all_preds = []
        all_targets = []

        start_eval = time.time()

        with torch.no_grad():
            for images, labels in self.data_loader.test_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                total_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                all_preds.extend(predicted.cpu().numpy())
                all_targets.extend(labels.cpu().numpy())
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        end_eval = time.time()
        avg_loss = total_loss / len(self.data_loader.test_loader)
        accuracy = correct / total

        self.logger.info(f"Test completed in {end_eval - start_eval:.2f} seconds, with accuracy: {accuracy * 100:.2f}%")

        return accuracy, avg_loss, all_preds, all_targets

    def predict(self, model, images):
        model = model.to(self.device)
        model.eval()

        images = images.to(self.device)

        with torch.no_grad():
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

        return predicted.cpu().numpy()

    def __call__(self, model, epochs, criterion, optimizer, scheduler):
        model = model.to(self.device)
        trained_model, train_losses, val_losses, val_accuracies = self.train(model, epochs, criterion, optimizer, scheduler)
        accuracy, avg_loss, all_preds, all_targets = self.test(trained_model, criterion)

        return trained_model, train_losses, val_losses, val_accuracies, accuracy, avg_loss, all_preds, all_targets

    def save_model_and_results(self, model, name, result_folder_path, accuracy, train_losses, val_losses, val_accuracies, all_preds, all_targets):
        self.save_model(model, name, result_folder_path)

        cm = confusion_matrix(all_targets, all_preds)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=self.data_loader.test_loader.dataset.classes, yticklabels=self.data_loader.test_loader.dataset.classes)
        title = f'Confusion Matrix for {name}\nAccuracy: {accuracy * 100:.2f}%'
        plt.title(title)
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig(os.path.join(result_folder_path, f'{name}_confusion_matrix.png'))
        plt.close()

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
