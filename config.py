import os

from omegaconf import OmegaConf, DictConfig
from pathlib import Path

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
config_path = os.path.join(current_dir_path, "config.yaml")

class Config(object):
    _config = None

    def __new__(cls, *args, **kwargs):
        if not cls._config:
            config_file_path = config_path
            project_config = OmegaConf.load(config_file_path) if os.path.exists(config_file_path) else {}

            cls._config = DictConfig({**project_config})

        return cls._config


config = Config()  # 加载获取配置信息
