from pydantic import BaseModel
import toml
from rich import print


class ServerConfig(BaseModel):
    host: str
    port: int


class DownstreamConfig(BaseModel):
    host: str
    port: int


class Config(BaseModel):
    server: ServerConfig
    downstream: DownstreamConfig


def load_config(config_path: str) -> Config:
    try:
        with open(config_path, "r") as config_file:
            config_dict = toml.load(config_file)
        return Config(**config_dict)
    except Exception as e:
        print(f"[bold red]Error loading config:[/bold red] {str(e)}")
        raise
