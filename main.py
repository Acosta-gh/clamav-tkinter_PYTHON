import tkinter as tk
from model.clamav_model import ClamAVModel
from view.clamav_view import ClamAVView
from controller.clamav_controller import ClamAVController
from language_service.language_service import LanguageService 

def main():
    # Initialize MVC components / Inicializar componentes MVC  
    root = tk.Tk()
    
    # Load texts for different languages / Cargar textos para diferentes idiomas  
    texts = LanguageService.load_texts()
    
    # Create the model, controller, and view / Crear el modelo, controlador y vista 
    model = ClamAVModel()
    controller = ClamAVController(model, texts)
    view = ClamAVView(root, controller, texts)
    
    # Set the view in the controller / Establecer la vista en el controlador  
    controller.set_view(view)
    
    # Start the application / Iniciar la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()