import os
import requests
import json
import torch
import shutil
from torchvision import transforms
from multiprocessing import Pool, cpu_count
from requests.exceptions import ConnectionError, ReadTimeout, TooManyRedirects, MissingSchema, InvalidURL
import pandas as pd
from src.utils.singleton import Singleton


class ImageNetScraper(metaclass=Singleton):
    def __init__(self, input_filepath, split_proportions, image_size, class_list, images_per_class, multiprocessing_workers, logger):
        self.images_per_class = images_per_class
        self.class_list = class_list
        self.multiprocessing_workers = multiprocessing_workers if multiprocessing_workers else cpu_count()
        self.logger = logger

        self.class_info_dict = self.load_classes_from_json()
        self.class_info_df = self.load_classes_from_csv()

        self.input_filepath = input_filepath
        self.split_proportions = split_proportions
        self.image_size = image_size
        self.class_names = self.class_info_df[self.class_info_df['synid'].isin(self.class_list)].set_index('synid')['class_name'].to_dict()

        self.transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor()
        ])

    def load_classes_from_json(self):
        json_filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'resources', 'imagenet_class_info.json')
        with open(json_filepath) as file:
            return json.load(file)

    def load_classes_from_csv(self):
        csv_filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'resources', 'classes_in_imagenet.csv')
        return pd.read_csv(csv_filepath)

    def get_image(self, img_url, class_name, class_images_counter):
        response = requests.get(img_url, timeout=1)
        if 'image' not in response.headers.get('content-type', ''):
            self.logger.error("Not an image")
            raise ValueError("Not an image")
        img_content = response.content
        if len(img_content) < 1000:
            self.logger.error("Image too small")
            raise ValueError("Image too small")
        img_file_path = os.path.join(self.input_filepath, f'{class_name}_{class_images_counter}.png')
        with open(img_file_path, 'wb') as img_f:
            img_f.write(img_content)
        self.logger.info(f"Saved image {img_file_path}")

    def download_images(self, urls, class_name):
        class_images_counter = 0
        for url in urls:
            if class_images_counter >= self.images_per_class:
                self.logger.info(f"Reached the limit of {self.images_per_class} images for class {class_name}.")
                break
            try:
                class_images_counter += 1
                self.get_image(url, class_name, class_images_counter)
            except (ConnectionError, ReadTimeout, TooManyRedirects, MissingSchema, InvalidURL, ValueError) as e:
                self.logger.error(f"Failed to download image: {e}")
                class_images_counter -= 1
        self.logger.info(f"Downloaded images for class {class_name}.")

    def fetch_image_urls(self, wnid):
        url = f'http://www.image-net.org/api/imagenet.synset.geturls?wnid={wnid}'
        response = requests.get(url)
        return [url.decode('utf-8') for url in response.content.splitlines()]

    def scrape_class(self, class_wnid):
        class_name = self.class_info_dict[class_wnid]["class_name"]
        img_urls = self.fetch_image_urls(class_wnid)
        self.logger.info(f'Starting download for class "{class_name}" with a limit of {self.images_per_class} images.')
        self.download_images(img_urls, class_name)

    def run(self):
        with Pool(self.multiprocessing_workers) as pool:
            pool.map(self.scrape_class, self.class_list)

    def load_and_split_data(self):
        self.logger.info("Starting to run scraper to download images.")

        self.train_path = os.path.join(self.input_filepath, 'train')
        self.valid_path = os.path.join(self.input_filepath, 'valid')
        self.test_path = os.path.join(self.input_filepath, 'test')

        os.makedirs(self.train_path, exist_ok=True)
        os.makedirs(self.valid_path, exist_ok=True)
        os.makedirs(self.test_path, exist_ok=True)

        self.logger.info("Created directories")

        self.run()

        images = [os.path.join(self.input_filepath, file) for file in os.listdir(self.input_filepath) if file.endswith(('.png', '.jpg', '.jpeg'))]
        total_images = len(images)
        self.logger.info(f"Found {total_images} images for processing.")

        train_size = int(total_images * self.split_proportions[0])
        valid_size = int(total_images * self.split_proportions[1])

        torch.manual_seed(0)
        shuffled_indices = torch.randperm(total_images)

        for class_name in self.class_names.values():
            os.makedirs(os.path.join(self.train_path, class_name), exist_ok=True)
            os.makedirs(os.path.join(self.valid_path, class_name), exist_ok=True)
            os.makedirs(os.path.join(self.test_path, class_name), exist_ok=True)

        for idx in shuffled_indices[:train_size]:
            image_path = images[idx]
            class_name = os.path.basename(image_path).split('_')[0]
            dest_path = os.path.join(self.train_path, class_name, os.path.basename(image_path))
            shutil.move(image_path, dest_path)
            self.logger.info(f"Moved {image_path} to {dest_path}")

        for idx in shuffled_indices[train_size:train_size + valid_size]:
            image_path = images[idx]
            class_name = os.path.basename(image_path).split('_')[0]
            dest_path = os.path.join(self.valid_path, class_name, os.path.basename(image_path))
            shutil.move(image_path, dest_path)
            self.logger.info(f"Moved {image_path} to {dest_path}")

        for idx in shuffled_indices[train_size + valid_size:]:
            image_path = images[idx]
            class_name = os.path.basename(image_path).split('_')[0]
            dest_path = os.path.join(self.test_path, class_name, os.path.basename(image_path))
            shutil.move(image_path, dest_path)
            self.logger.info(f"Moved {image_path} to {dest_path}")

        for class_name in self.class_names.values():
            train_class_path = os.path.join(self.train_path, class_name)
            valid_class_path = os.path.join(self.valid_path, class_name)
            test_class_path = os.path.join(self.test_path, class_name)

            if os.path.exists(train_class_path) and len(os.listdir(train_class_path)) == 0:
                os.rmdir(train_class_path)

            if os.path.exists(valid_class_path) and len(os.listdir(valid_class_path)) == 0:
                os.rmdir(valid_class_path)
                self.logger.info(f"Removed empty directory {valid_class_path}")

            if os.path.exists(test_class_path) and len(os.listdir(test_class_path)) == 0:
                os.rmdir(test_class_path)

    def clear_directories(self):
        directory = self.input_filepath
        if os.path.exists(directory):
            shutil.rmtree(directory)
            os.makedirs(directory, exist_ok=True)
            self.logger.info(f"Cleared and reset directory {directory}")
