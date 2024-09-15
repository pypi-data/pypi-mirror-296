import torch
import torch.optim as optim
import torch.nn as nn
import json
import os
import torch.utils
from torch.utils.data import DataLoader
import torch.utils.data
from typing import Callable


class ModelTrainer:
    def __init__(self, model: nn.Module, dataset: torch.utils.data.Dataset, learning_rate: float = 0.01):
        """
        Initializes the ModelTrainer class

        :param model: The model to be trained
        :param dataset: The dataset used for training
        """
        self.model = model
        self.dataset = dataset
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        # Assuming mean squared error loss; adjust based on your task
        self.criterion = nn.MSELoss()
        self.save_path = "trained_model"
        self.load_path = "trained_model"
        self.save_model = True
        self.lowest_loss = float('inf')
        self.loss_history = []

        self.after_iteration_callback: Callable = None
        self.after_output_callback: Callable = None
        self.before_output_callback: Callable = None
        self.before_iteration_callback: Callable = None
        self.after_loss_callback: Callable = None

        self.training_iteration = -1
        self.training_inputs = None
        self.training_targets = None
        self.training_loss = float('inf')

        # Create save path if it doesn't exist
        os.makedirs(self.save_path, exist_ok=True)

    def set_learning_rate(self, learning_rate: float):
        """
        Sets a new learning rate for the optimizer without changing other settings.

        :param learning_rate: The new learning rate to set for the optimizer
        """
        # Load the previous state into the optimizer
        self.optimizer.load_state_dict(self.optimizer.state_dict())

        # Manually update the learning rate for all parameter groups
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = learning_rate

        print(f"Learning rate updated to {learning_rate}")

    def load_model(self, load_optimizer: bool = True):
        """
        Loads the model, optimizer, and loss information from the specified load path.

        :param load_optimizer: If True, loads the optimizer state along with the model
        """
        model_path = os.path.join(self.load_path, 'model.pth')
        optimizer_path = os.path.join(self.load_path, 'optimizer.pth')
        loss_path = os.path.join(self.load_path, 'loss.json')

        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path))
            print(f"Model loaded from {model_path}")

        if load_optimizer and os.path.exists(optimizer_path):
            self.optimizer.load_state_dict(torch.load(optimizer_path))
            print(f"Optimizer loaded from {optimizer_path}")

        if os.path.exists(loss_path):
            with open(loss_path, 'r') as f:
                loss_data = json.load(f)
                self.lowest_loss = loss_data.get('lowest_loss', float('inf'))
                self.loss_history = loss_data.get('loss_history', [])
                print(f"Loss data loaded from {loss_path}")

    def save_model_state(self):
        """
        Saves the model, optimizer, and loss information to the specified save path.
        """
        model_path = os.path.join(self.save_path, 'model.pth')
        optimizer_path = os.path.join(self.save_path, 'optimizer.pth')
        loss_path = os.path.join(self.save_path, 'loss.json')

        torch.save(self.model.state_dict(), model_path)
        torch.save(self.optimizer.state_dict(), optimizer_path)

        loss_data = {
            'lowest_loss': self.lowest_loss,
            'loss_history': self.loss_history
        }
        with open(loss_path, 'w') as f:
            json.dump(loss_data, f, indent=4)
        print(f"Model and optimizer saved to {self.save_path}")

    def train(self, iterations: int = 10, batch_size: int = 32, only_save_lowest: bool = True):
        """
        Trains the model for a specified number of iterations, optionally saving only the lowest loss model.

        :param iterations: Number of training iterations
        :param batch_size: Batch size for training
        :param only_save_lowest: If True, saves the model only when the loss is lower than the lowest observed loss
        """

        self.training_iteration = -1

        dataloader = DataLoader(
            self.dataset, batch_size=batch_size, shuffle=True)

        for iteration in range(iterations):
            self.training_iteration = iteration

            if self.before_iteration_callback is not None:
                self.before_iteration_callback()

            running_loss = 0.0
            for inputs, targets in dataloader:
                self.optimizer.zero_grad()

                self.training_inputs = inputs
                self.training_targets = targets

                if self.before_output_callback is not None:
                    self.before_output_callback()

                outputs = self.model(self.training_inputs)

                if self.after_output_callback is not None:
                    self.after_output_callback()

                loss = self.criterion(outputs, self.training_targets)
                loss.backward()

                self.training_loss = loss

                if self.after_loss_callback is not None:
                    self.after_loss_callback()

                self.optimizer.step()
                running_loss += self.training_loss.item()

            # Calculate average loss for this iteration
            avg_loss = running_loss / len(dataloader)
            self.loss_history.append(avg_loss)

            if self.after_iteration_callback is not None:
                self.after_iteration_callback()

            print(f"Iteration {iteration + 1}/{iterations}, Loss: {avg_loss}")

            # Save the model if save_model is enabled
            if self.save_model:
                if only_save_lowest:
                    if avg_loss < self.lowest_loss:
                        self.lowest_loss = avg_loss
                        self.save_model_state()
                else:
                    self.save_model_state()
