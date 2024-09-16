from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures
from src.utils.plotting import generate_subgraph
from typing import Optional
from src.loaders.loader_base import DataLoaderBase
import matplotlib.pyplot as plt


class CoraDataLoader(DataLoaderBase):
    class_mapping = {
        0: "Case Based",
        1: "Genetic Algorithms",
        2: "Neural Networks",
        3: "Probabilistic Methods",
        4: "Reinforcement Learning",
        5: "Rule Learning",
        6: "Theory"
    }

    def __init__(self, data_dir, logger):
        super().__init__(data_dir, logger, "CORA")
        self.data_dir: Optional[str] = data_dir
        self.logger = logger
        self.num_classes = 7

        self.dataset = None
        self.data = None

        self.load_data()

    def describe_data(self) -> None:
        self.logger.info("Data Description")
        self.logger.info("-----------------")
        self.logger.info(f"Number of nodes: {self.data.num_nodes}")
        self.logger.info(f"Number of edges: {self.data.num_edges}")
        self.logger.info(f"Number of features per node: {self.data.num_node_features}")
        self.logger.info(f"Number of classes: {self.num_classes}")
        self.print_class_mapping()

    def load_data(self):
        self.dataset = Planetoid(root=self.data_dir, name='Cora', transform=NormalizeFeatures())
        self.data = self.dataset[0]

        self.logger.info("Data loaded successfully.")

        self.describe_data()

    def print_class_mapping(self):
        self.logger.info("Class mapping (number -> field of study):")
        for class_num, field in self.class_mapping.items():
            self.logger.info(f"Class {class_num}: {field}")

    def display_sample_data(self, num_nodes=10):
        image = generate_subgraph(num_nodes)
        plt.figure(figsize=(12, 12))
        plt.imshow(image, cmap='gray')
        plt.axis('off')

        self.logger.info("Sample data displayed successfully.")
