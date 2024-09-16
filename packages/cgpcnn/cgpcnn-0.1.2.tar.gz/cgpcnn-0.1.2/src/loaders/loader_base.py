from abc import ABC, abstractmethod


class DataLoaderBase(ABC):
    def __init__(self, data_dir, logger, data_name):
        self.data_dir = data_dir
        self.logger = logger
        self.data_name = data_name

    @abstractmethod
    def load_data(self, *args, **kwargs):
        """
        Abstract method for loading data.
        """
        pass

    @abstractmethod
    def display_sample_data(self, *args, **kwargs) -> None:
        """
        Abstract method for displaying a sample of data.
        """
        pass

    @abstractmethod
    def describe_data(self) -> None:
        """
        Abstract method for describing the data.
        """
        pass
