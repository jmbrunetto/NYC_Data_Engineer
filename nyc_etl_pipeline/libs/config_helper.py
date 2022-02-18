"""config_helper"""
import os
from pyhocon import ConfigFactory


class ConfigHelper:
    """ConfigHelper"""

    def __init__(self, service_name: str):
        env_var = f"{service_name.upper()}_CONFIG_PATH"
        possible_config_locations = [
            os.path.join(service_name, 'conf', 'instance.conf')
        ]

        if env_var in os.environ:
            config_file = os.getenv(env_var)
        else:
            for config_file in possible_config_locations:
                if os.path.exists(config_file):
                    config_file = config_file
                    break

        if not config_file:
            raise ValueError("Configuration file not found!")

        self.config = ConfigFactory.parse_file(config_file)
