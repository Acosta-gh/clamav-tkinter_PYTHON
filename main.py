import ttkbootstrap as ttk

from model.clamav_model import ClamAVModel
from model.config_model import ConfigModel

from controller.clamav_controller import ClamAVController
from controller.config_controller import ConfigController

from view.clamav_view import ClamAVView

from language_service.language_service import LanguageService 

def main():
    # Inicializar componentes MVC / Initialize MVC components
    root = ttk.Window(themename="flatly")

    # Cargar textos para diferentes idiomas / Load texts for different languages 
    texts = LanguageService.load_texts()
    
    # Crear los modelos / Create the models
    clamav_model = ClamAVModel()
    config_model = ConfigModel()

    # Crear los controladores / Create the controllers
    clamav_controller = ClamAVController(clamav_model, config_model, texts)
    config_controller = ConfigController(config_model)
    
    # Crear la vista / Create the view
    clamav_view = ClamAVView(root, clamav_controller, config_controller , texts)
    
    # Establecer la vista en el controlador / Set the view in the controller
    clamav_controller.set_view(clamav_view)
    
    # Iniciar la aplicación / Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
