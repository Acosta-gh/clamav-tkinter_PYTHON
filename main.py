import tkinter as tk
import ttkbootstrap as ttk

from model.clamav_model import ClamAVModel
from view.clamav_view import ClamAVView
from controller.clamav_controller import ClamAVController
from language_service.language_service import LanguageService 

def main():
    # Inicializar componentes MVC / Initialize MVC components
    #root = tk.Tk()
    root = ttk.Window(themename="flatly")

    # Cargar textos para diferentes idiomas / Load texts for different languages 
    texts = LanguageService.load_texts()
    
    # Crear el modelo, controlador y vista / Create the model, controller and view
    model = ClamAVModel()
    controller = ClamAVController(model, texts)
    view = ClamAVView(root, controller, texts)
    
    # Establecer la vista en el controlador / Set the view in the controller
    controller.set_view(view)
    
    # Iniciar la aplicación / Start the application
    root.mainloop()

if __name__ == "__main__":
    main()