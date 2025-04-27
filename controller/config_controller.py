# Sad excuse of a controller to comply with MVC pattern
class ConfigController:
    def __init__(self, config_model):
        self.model = config_model

    def load(self):
        """Carga la configuración desde el archivo / Loads the configuration from the file"""
        return self.model.load()
    def save(self, config_update):
        """Guarda la configuración en el archivo / Saves the configuration to the file"""
        self.model.save(config_update)
    

    