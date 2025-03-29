import toml
from rich import print

from model.config import Config


def load_config(config_path: str) -> Config:
    try:
        with open(config_path, "r") as config_file:
            config_dict = toml.load(config_file)
        return Config(**config_dict)
    except Exception as e:
        print(f"[bold red]Error loading config:[/bold red] {str(e)}")
        raise


class ConfigManager:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)

    def get_config(self) -> Config:
        return self.config

    def reload_config(self):
        self.config = self.load_config(self.config_path)
        return self.config

    def set_config(self, config: Config):
        self.config = config
        return self.config

    @staticmethod
    def load_config(config_path: str) -> Config:
        try:
            with open(config_path, "r") as config_file:
                config_dict = toml.load(config_file)
            return Config(**config_dict)
        except Exception as e:
            print(f"[bold red]Error loading config:[/bold red] {str(e)}")
            raise
