import random
import numpy as np
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, TQDMProgressBar
from pytorch_lightning.tuner.tuning import Tuner
from deep_chess_playground.data_loading.data_module_factory import DataModuleFactory
from deep_chess_playground.lightning_modules.lightning_module_factory import LightningModuleFactory
from deep_chess_playground.utils import parse_configuration_file, read_json


def main(args):
    # Read the configuration file
    config = read_json(config_path=args.conf)
    train_config = config["training"]

    # Set random seed for reproducibility
    random_seed = config["random_seed"]
    random.seed(random_seed)
    np.random.seed(random_seed)
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed_all(random_seed)

    # Set printing precision for readability
    np.set_printoptions(formatter={"float": lambda x: "{0:0.2f}".format(x)})

    # Create the data module
    data_module = DataModuleFactory.create(config=train_config["data_module"])

    # Create and print the module
    module = LightningModuleFactory.build_module(config=train_config["module"])
    print(f"Model summary:\n{module}")
    print(f"Number of trainable parameters: {sum(p.numel() for p in module.parameters() if p.requires_grad)}")

    # Create some useful callbacks
    early_stopper = EarlyStopping(monitor=train_config["monitor"], patience=train_config["patience"])
    progress_bar = TQDMProgressBar()
    callbacks_list = [early_stopper, progress_bar]

    # Create trainer
    trainer = pl.Trainer(accelerator="gpu",
                         max_epochs=train_config["max_epochs"],
                         callbacks=callbacks_list)

    # Find hyperparameters automatically
    tuner = Tuner(trainer)

    # Find maximum batch size
    tuner.scale_batch_size(module, data_module)

    # Find good learning rate
    lr_finder = tuner.lr_find(module, data_module)

    # Get the suggestion
    suggestion = lr_finder.suggestion()

    # Plot and print the suggestion
    fig = lr_finder.plot(suggest=True)
    fig.show()
    print(f"Suggestion = {suggestion}")

    # Pick point based on plot, or get suggestion
    module.hparams.lr = suggestion

    # Train module
    trainer.fit(module, data_module, ckpt_path=train_config["checkpoint_path"])


if __name__ == "__main__":
    args = parse_configuration_file(description="Training configuration.")
    main(args)
