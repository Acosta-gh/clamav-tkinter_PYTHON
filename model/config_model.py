import json

class ConfigModel:
    def __init__(self, config_path):
        self.config_path = config_path
        self.default_config = {
            "recursive": 1,
            "kill": 0,
            "lang": "en"
        }

    def load(self):
        """Carga el archivo de configuración / Loads the configuration file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = self.default_config
            self.save(config)
        except json.JSONDecodeError:
            config = self.default_config
            self.save(config)
        return config

    def save(self, config_update):
        """Actualiza solo las claves especificadas en el archivo de configuración / Updates only the specified keys in the configuration file"""
        try:
            with open(self.config_path, 'r') as f:
                current_config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            current_config = self.default_config.copy()

        current_config.update(config_update)

        with open(self.config_path, 'w') as f:
            json.dump(current_config, f, indent=4)
