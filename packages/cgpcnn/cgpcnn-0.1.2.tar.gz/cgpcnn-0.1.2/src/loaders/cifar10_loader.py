from torch.utils.data import DataLoader, Subset, random_split
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np
import torch
from src.utils.plotting import generate_image_grid
from src.loaders.loader_base import DataLoaderBase
import matplotlib.pyplot as plt


class CIFAR10DataLoader(DataLoaderBase):
    def __init__(self, data_dir, batch_size, shuffle, logger):
        super().__init__(data_dir, logger, "CIFAR-10")

        self.train_loader = None
        self.val_loader = None
        self.test_loader = None

        self.batch_size = batch_size
        self.shuffle = shuffle
        self.logger = logger
        self.class_names = ['airplane',
                            'automobile',
                            'bird',
                            'cat',
                            'deer',
                            'dog',
                            'frog',
                            'horse',
                            'ship',
                            'truck']

        self.transform_train = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(32, padding=4),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])

        self.transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        self.load_all_data()
        # self.load_data(split_train_val_proportion=[1.0, 0.0], train_size=None, test_size=None)

    def display_sample_data(self, data, num_samples):
        images, labels = next(iter(data))

        images = images.numpy().transpose((0, 2, 3, 1))
        images = images * 0.5 + 0.5

        image = generate_image_grid(images=images[:num_samples], cls_true=labels[:num_samples], label_names=self.class_names, title="Sample CIFAR-10 Images")
        plt.figure(figsize=(12, 12))
        plt.imshow(image)
        plt.axis('off')

        self.logger.info("Sample data displayed successfully.")

    def describe_data(self):
        self.logger.info("Data Description")
        self.logger.info("-----------------")
        if self.train_loader is not None:
            self.logger.info(f"Train Data: Number of samples: {len(self.train_loader.dataset)}")
        if self.val_loader is not None:
            self.logger.info(f"Validation Data: Number of samples: {len(self.val_loader.dataset)}")
        if self.test_loader is not None:
            self.logger.info(f"Test Data: Number of samples: {len(self.test_loader.dataset)}")

    def load_data(self, split_train_val_proportion, train_size, test_size):
        if sum(split_train_val_proportion) != 1.0:
            raise ValueError("Proportions must sum to 1.0")

        train_dataset = datasets.CIFAR10(root=self.data_dir, train=True, download=True, transform=self.transform_test)
        test_dataset = datasets.CIFAR10(root=self.data_dir, train=False, download=True, transform=self.transform_test)

        train_size_full = int(split_train_val_proportion[0] * len(train_dataset))
        val_size = len(train_dataset) - train_size_full

        train_subset, val_subset = random_split(train_dataset, [train_size_full, val_size])

        if train_size is not None and train_size < train_size_full:
            train_indices = np.random.choice(len(train_subset), train_size, replace=False)
            train_subset = Subset(train_subset, train_indices)
            train_subset.dataset.classes = self.class_names

        if test_size is not None and test_size < len(test_dataset):
            test_indices = np.random.choice(len(test_dataset), test_size, replace=False)
            test_dataset = Subset(test_dataset, test_indices)
            test_dataset.dataset.classes = self.class_names

        self.train_loader = DataLoader(train_subset, batch_size=self.batch_size, shuffle=self.shuffle)
        self.val_loader = DataLoader(val_subset, batch_size=self.batch_size, shuffle=False)
        self.test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)

        self.logger.info("Data loaded successfully.")
        self.describe_data()

    def load_all_data(self):
        train = datasets.CIFAR10(root=self.data_dir, train=True, download=True, transform=self.transform_train)
        trainloader = torch.utils.data.DataLoader(train, batch_size=128, shuffle=True)

        test = datasets.CIFAR10(root=self.data_dir, train=True, download=True, transform=self.transform_train)
        testloader = torch.utils.data.DataLoader(test, batch_size=128, shuffle=False)

        self.train_loader = trainloader
        self.val_loader = None
        self.test_loader = testloader

        self.logger.info("Data loaded successfully.")
        self.describe_data()
