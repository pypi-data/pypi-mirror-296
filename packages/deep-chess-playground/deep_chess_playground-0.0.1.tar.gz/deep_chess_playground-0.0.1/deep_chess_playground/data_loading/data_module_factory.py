from deep_chess_playground.data_loading.standard_data_module import StandardDataModule


class DataModuleFactory:
    @staticmethod
    def create(config: dict[str, str]):
        data_module_type = config["type"]
        if data_module_type == "StandardDataModule":
            return StandardDataModule.create(config)
        # elif data_module_type == "SomeOtherDataModule":
        #    ...
        else:
            raise ValueError(f"Unknown data module type: {data_module_type}")
