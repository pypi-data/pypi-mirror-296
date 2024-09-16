from deep_chess_playground.pytorch_modules.fcn.simple_fcn import SimpleFCN
from deep_chess_playground.pytorch_modules.transformer.simple_transformer import SimpleTransformer


class PyTorchModuleFactory:
    @staticmethod
    def build_module(config: dict[str, str]):
        module_category = config.pop("category").lower()

        # fcn
        if module_category == "SimpleFCN":
            module = PyTorchModuleFactory.build_simple_fcn(config)

        # cnn
        elif module_category == "SimpleCNN":
            module = PyTorchModuleFactory.build_simple_cnn(config)

        # transformer
        elif module_category == "SimpleTransformer":
            module = PyTorchModuleFactory.build_simple_transformer(config)

        else:
            raise ValueError("Invalid configuration - no valid PyTorch module category found.")

        return module

    @staticmethod
    def build_simple_fcn(config):
        return SimpleFCN(input_size=config["input_size"], hidden_size=config["hidden_size"], output_size=config["output_size"])

    @staticmethod
    def build_simple_cnn(config):
        return SimpleCNN(input_size=config["input_size"], hidden_size=config["hidden_size"],
                         output_size=config["output_size"])

    @staticmethod
    def build_simple_transformer(config):
        return SimpleTransformer(input_size=config["input_size"],
                                 hidden_size=config["hidden_size"],
                                 num_layers=config["num_layers"],
                                 num_heads=config["num_heads"],
                                 output_size=config["output_size"])
