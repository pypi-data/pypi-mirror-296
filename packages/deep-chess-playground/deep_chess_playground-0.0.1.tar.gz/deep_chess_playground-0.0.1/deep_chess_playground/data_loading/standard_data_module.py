from typing import Dict, Any
import pytorch_lightning as pl


class StandardDataModule(pl.LightningDataModule):
    @staticmethod
    def create(config):
        pass


class DataModule(pl.LightningDataModule):
    def __init__(self, train_config: Dict[str, Any] = None, test_config: Dict[str, Any] = None, batch_size: int = 16):
        """
        Args:
            train_config: Configuration dictionary for the training dataset.
                For expected keys and their meaning, see the documentation of the `CsvDataset` class.
                Additional key:
                    - 'val_split': Proportion of the training data to use for validation. Defaults to 0.2.
            test_config: Configuration dictionary for the test dataset.
                Expected keys are the same as for the train_config except 'val_split' argument.
            batch_size: Batch size. Defaults to 16.
        """
        super().__init__()
        self._train_config = train_config
        self._test_config = test_config
        self._batch_size = batch_size
        self._train_dataset, self._val_dataset, self._test_dataset = None, None, None
        self.setup()

    def setup(self, stage=None):
        if stage in (None, 'fit') and self._train_config is not None:
            val_split = self._train_config.pop('val_split', 0.2)
            dataset = CsvDataset(**self._train_config)
            train_length = int(len(dataset) * (1 - val_split))
            self._train_dataset, self._val_dataset = random_split(dataset, [train_length, len(dataset) - train_length])
        if stage in (None, 'test') and self._test_config is not None:
            self._test_dataset = CsvDataset(**self._test_config)

    def train_dataloader(self):
        return DataLoader(self._train_dataset, self._batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self._val_dataset, self._batch_size, shuffle=False)

    def test_dataloader(self):
        return DataLoader(self._test_dataset, self._batch_size, shuffle=False)
