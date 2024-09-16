from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from src.utils.plotting import generate_image_grid
import torchvision.datasets as datasets
import os
from src.loaders.loader_base import DataLoaderBase
import numpy as np
import matplotlib.pyplot as plt


class ImageNetDataLoader(DataLoaderBase):
    def __init__(self, data_dir, batch_size, shuffle, logger, imgSize, scraper):
        super().__init__(data_dir, logger, "ImageNet")

        self.train_loader = None
        self.val_loader = None
        self.test_loader = None

        self.batch_size = batch_size
        self.shuffle = shuffle

        self.transform = transforms.Compose([
            transforms.Resize(imgSize),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ])

        self.scraper = scraper

    def display_sample_data(self, data, num_samples):
        images, labels = next(iter(data))

        images = images.numpy().transpose((0, 2, 3, 1))
        images = images * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.456, 0.406])

        image = generate_image_grid(images=images[:num_samples], cls_true=labels[:num_samples], label_names=self.class_names, title="Sample MNIST Images")
        plt.figure(figsize=(12, 12))
        plt.imshow(image, cmap='gray')
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

    def load_data(self):
        train_dataset = datasets.ImageFolder(os.path.join(self.data_dir, 'train'), transform=self.transform)
        val_dataset = datasets.ImageFolder(os.path.join(self.data_dir, 'valid'), transform=self.transform)
        test_dataset = datasets.ImageFolder(os.path.join(self.data_dir, 'test'), transform=self.transform)

        self.train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=self.shuffle)
        self.val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)
        self.test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)

        self.logger.info("Data loaded successfully.")

        return self.train_loader, self.val_loader, self.test_loader
