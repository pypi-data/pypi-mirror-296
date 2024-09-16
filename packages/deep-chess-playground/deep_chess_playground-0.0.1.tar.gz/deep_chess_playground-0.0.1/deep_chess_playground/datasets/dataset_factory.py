from deep_chess_playground.datasets.standard_dataset import StandardDataset


class DatasetFactory:
    @staticmethod
    def create(config: dict[str, str]):
        dataset_type = config["type"]
        if dataset_type == "StandardDataset":
            return StandardDataset.create(config)
        # elif data_module_type == "SomeOtherDataset":
        #    ...
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
