from deep_chess_playground.data_loading.data_module_factory import FCNDataModuleFactory
from deep_chess_playground.data_loading.data_module_factory import CNNDataModuleFactory
from deep_chess_playground.data_loading.data_module_factory import TransformerDataModuleFactory


class DataModuleFactory:
    @staticmethod
    def create(config: dict[str, str]):
        data_module_architecture = config["architecture"]
        if data_module_architecture == "fcn":
            return FCNDataModuleFactory.create(config)
        elif data_module_architecture == "cnn":
            return CNNDataModuleFactory.create(config)
        elif data_module_architecture == "transformer":
            return TransformerDataModuleFactory.create(config)
