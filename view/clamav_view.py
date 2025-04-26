import os

import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from tkinter import messagebox
#from tkinter.filedialog import askopenfilename, askdirectory
#from datetime import datetime
from tkinter import PhotoImage
from pathlib import Path
from model.config_model import ConfigModel


class ClamAVView:
    def __init__(self, root, controller, texts):
        self.root = root
        self.controller = controller
        
        # Ruta al archivo de configuración
        self.path_config_file = Path.home() / "ClamAVTkinter" / ".config.json"
        self.path_config_file.parent.mkdir(
            parents=True, exist_ok=True)  # Crear directorio si no existe

        # Crear archivo vacío si no existe (opcional)
        self.path_config_file.touch(exist_ok=True)

        self.config = ConfigModel(self.path_config_file)

        # Cargar la configuración / Load the configuration
        self.lang = self.config.load()["lang"]
        self.texts = texts

        # Cargar el icono / Load the icon
        #self.script_dir = os.path.dirname(os.path.realpath(__file__))
        #self.parent_dir = os.path.dirname(self.script_dir)
        #self.icon_path = os.path.join(self.parent_dir, "shield.png")
        self.icon_path = Path(__file__).resolve().parent.parent / "shield.png"

        try:
            self.icon_image = PhotoImage(file=self.icon_path)
            self.root.iconphoto(True, self.icon_image)
        except Exception as e:
            print(f"Error loading the icon: {e}")

        # Variables de configuración / Configuration variables
        self.checkbox_var_recursive = tk.IntVar(
            value=self.config.load()["recursive"])
        self.combobox_var = tk.IntVar(value=self.config.load()["action"])
        self.bell_var = tk.IntVar(value=self.config.load()["bell"])

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario principal / Sets up the main user interface"""
        self.root.title(self.texts[self.lang]['app_title'])
        self.root.resizable(False, False)
        self.center_window()
        self.create_menu()
        self.create_tabs()
        self.create_buttons()
        self.create_checkboxes()
        self.create_comboboxes()

        # self.controller.get_version()  # No descomentar, esto se realiza en el método set_view del controlador / This is done in the set_view method of the controller

    def center_window(self, window=None, marginx=100, marginy=100):
        """Centra una ventana en la pantalla / Centers a window on the screen"""
        if window is None:
            window = self.root
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"+{x-marginx}+{y-marginy}")

    def create_menu(self):
        """Crea la barra de menú / Creates the menu bar"""
        if hasattr(self, "menu_bar"):
            self.menu_bar.destroy()

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.language_menu.add_command(
            label=self.texts[self.lang]["language_menu1"],
            command=lambda: self.controller.change_lang("en")
        )
        self.language_menu.add_command(
            label=self.texts[self.lang]["language_menu2"],
            command=lambda: self.controller.change_lang("es")
        )

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(
            label=self.texts[self.lang]["help_menu1"],
            command=lambda: self.controller.view_about()
        )

        self.menu_bar.add_cascade(
            label=self.texts[self.lang]["menu_bar1"],
            menu=self.language_menu
        )
        self.menu_bar.add_cascade(
            label=self.texts[self.lang]["menu_bar2"],
            menu=self.help_menu
        )

    def create_tabs(self):
        """Crea las pestañas de la aplicación / Creates the tabs of the application"""
        self.tabs_notebook = ttk.Notebook(self.root, bootstyle="default")
        self.tabs_notebook.pack(fill="both", expand=True, pady=10, padx=5)

        self.scan_frame = ttk.Frame(self.tabs_notebook)
        self.history_frame = ttk.Frame(self.tabs_notebook)
        self.update_frame = ttk.Frame(self.tabs_notebook)
        self.config_frame = ttk.Frame(self.tabs_notebook)

        self.tabs_notebook.add(
            self.scan_frame, text=self.texts[self.lang]["tab1"])
        self.tabs_notebook.add(
            self.history_frame, text=self.texts[self.lang]["tab2"])
        self.tabs_notebook.add(
            self.update_frame, text=self.texts[self.lang]["tab3"])
        self.tabs_notebook.add(
            self.config_frame, text=self.texts[self.lang]["tab4"])

    def create_buttons(self):
        """Crea los botones de la interfaz / Creates the buttons of the interface"""
        self.button_scan_a_file = ttk.Button(
            self.scan_frame,
            text=self.texts[self.lang]["button_label1"],
            command=self.controller.scan_a_file
        )
        self.button_scan_a_directory = ttk.Button(
            self.scan_frame,
            text=self.texts[self.lang]["button_label2"],
            command=self.controller.scan_a_directory
        )
        self.button_view_history = ttk.Button(
            self.history_frame,
            text=self.texts[self.lang]["button_label3"],
            command=self.controller.view_history
        )
        self.button_update_database = ttk.Button(
            self.update_frame,
            text=self.texts[self.lang]["button_label4"],
            command=self.controller.update_database
        )
        self.button_save_config = ttk.Button(
            self.config_frame,
            text=self.texts[self.lang]["button_label5"],
            command=lambda: (
                self.config.save(
                    {
                        "recursive": self.checkbox_var_recursive.get(),
                        "action": self.combobox_var.get(),
                    }
                ),
                self.button_save_config.config(
                    text=self.texts[self.lang]['changes_saved']),
                self.root.after(2000, lambda: self.button_save_config.config(
                    text=self.texts[self.lang]['button_label5']))
            )
        )

        self.button_scan_a_file.pack(fill="x", pady=10, padx=10)
        self.button_scan_a_directory.pack(fill="x", pady=5, padx=10)
        self.button_view_history.pack(fill="x", pady=10, padx=10)
        self.button_update_database.pack(fill="x", padx=10, pady=10)
        self.label_version = ttk.Label(self.update_frame, text="", wraplength=280)
        self.label_version.pack(padx=10, pady=10)

    def create_checkboxes(self):
        """Crea los checkboxes de configuración / Creates the configuration checkboxes"""
        self.checkbox_recursive = ttk.Checkbutton(
            self.config_frame,
            text=self.texts[self.lang]['checkbox_label1'],
            variable=self.checkbox_var_recursive,
            bootstyle="square-toggle"
        )
        self.checkbox_bell = tk.Checkbutton(
            self.config_frame,
            text=self.texts[self.lang]['checkbox_label3'],
            variable=self.bell_var
        )
        self.checkbox_recursive.pack(pady=15, padx=15, anchor="w")
        #self.checkbox_bell.pack(pady=(0, 10), padx=5, anchor="w") 
        # Parece que el argumento --bell no funciona en la versión actual de ClamAV / It seems that the --bell argument does not work in the current version of ClamAV

        
    def create_comboboxes(self):
        ## 0 = No hacer nada / 0 = Do nothing 1 = Mover a carpeta designada / 1 = Move to designated folder 2 = Eliminar / 2 = Remove
        self.combobox_options = [self.texts[self.lang]['combox_label1'],
                        self.texts[self.lang]['combox_label2'],
                        self.texts[self.lang]['combox_label3']]
        self.combobox = ttk.Combobox(
            self.config_frame, values=self.combobox_options, state="readonly")

        # Obtener el valor entero actual de combobox_var (0, 1 o 2) / Get the current integer value of combobox_var (0, 1, or 2)
        current_value = self.combobox_var.get()
        self.combobox.set(self.combobox_options[current_value])

        def on_combobox_select(event):
            # Obtener el valor seleccionado como cadena / Get the selected value as a string
            selected_string = self.combobox.get()
            # Obtener el índice del valor seleccionado / Get the index of the selected value
            selected_index = self.combobox_options.index(selected_string)
            # Actualizar el valor de combobox_var / Update the value of combobox_var
            if selected_index == 2:
                messagebox.showwarning(
                    title=self.texts[self.lang]["warning_title"], 
                    message=self.texts[self.lang]['delete_disclaimer']
                )
                
            self.combobox_var.set(selected_index)

        # Vincular el evento de selección / Bind the selection event
        self.combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        self.combobox_label = ttk.Label(
            self.config_frame,
            text=self.texts[self.lang]['config_options_label'],
        )

        self.combobox_label.pack(pady=1, padx=15, anchor="w")
        self.combobox.pack(fill='x', expand=True, pady=5, padx=15)
        self.button_save_config.pack(pady=(15, 15), padx=5)

    def update_texts(self):
        """Actualiza los textos de la interfaz al cambiar el idioma / Updates the texts of the interface when changing the language"""
        self.root.title(self.texts[self.lang]['app_title'])

        self.tabs_notebook.tab(0, text=self.texts[self.lang]["tab1"])
        self.tabs_notebook.tab(1, text=self.texts[self.lang]["tab2"])
        self.tabs_notebook.tab(2, text=self.texts[self.lang]["tab3"])
        self.tabs_notebook.tab(3, text=self.texts[self.lang]["tab4"])

        self.button_scan_a_file.config(
            text=self.texts[self.lang]["button_label1"])
        self.button_scan_a_directory.config(
            text=self.texts[self.lang]["button_label2"])
        self.button_view_history.config(
            text=self.texts[self.lang]["button_label3"])
        self.button_update_database.config(
            text=self.texts[self.lang]["button_label4"])
        self.button_save_config.config(
            text=self.texts[self.lang]["button_label5"])
        self.checkbox_recursive.config(
            text=self.texts[self.lang]["checkbox_label1"])
        self.combobox_label.config(
            text=self.texts[self.lang]["config_options_label"])
        
        self.combobox_options = [self.texts[self.lang]['combox_label1'],
                        self.texts[self.lang]['combox_label2'],
                        self.texts[self.lang]['combox_label3']]
        self.combobox['values'] = self.combobox_options
        self.combobox.set(self.combobox_options[self.combobox_var.get()])

        self.create_menu()

    def show_scan_window(self, path):
        """Muestra una ventana con una barra de progreso durante el escaneo / Shows a window with a progress bar during the scan"""
        newWindow = tk.Toplevel(self.root)
        newWindow.title(self.texts[self.lang]['scan'])
        self.center_window(newWindow, 200, 150)

        label_loading = ttk.Label(
            newWindow,
            text=f"{self.texts[self.lang]['scan']} {path}",
            justify="left",
            wraplength=280
        )
        label_loading.pack(padx=10, pady=10)

        progressbar = ttk.Progressbar(newWindow, mode="indeterminate")
        progressbar.pack(fill=tk.X, padx=10, pady=10)
        progressbar.start(10)

        return newWindow, progressbar, label_loading

    def show_scan_results(self, newWindow, result, filepath):
        """Muestra los resultados del escaneo / Shows the scan results"""

        if not newWindow.winfo_exists():
            print("The scan window does not exist.")
            return
    
        newWindow.title(self.texts[self.lang]['scan_complete'])
        self.center_window(newWindow, 500, 250)

        text_square = tk.Text(newWindow, wrap=tk.WORD,
                              font=("Courier New", 12))
        text_square.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if isinstance(result, Exception):
            text_square.insert(
                tk.END, f"{self.texts[self.lang]['error_message']}:\n{str(result)}")
        else:
            text_square.insert(tk.END, f"{self.texts[self.lang]['stdout']}:\n")
            text_square.insert(tk.END, result.stdout)
            text_square.insert(
                tk.END, f"\n{self.texts[self.lang]['stderr']}:\n")
            text_square.insert(tk.END, result.stderr)

        try:
            text_square.config(state="disabled")
        except tk.TclError as e:
            print(f"Error configuring text widget: {e}")

        messagebox.showinfo(
            self.texts[self.lang]['scan_complete'],
            f"{self.texts[self.lang]['result_saved']} {filepath}"
        )

    def show_about_window(self, version):
        """Muestra la ventana Acerca de / Shows the About window"""
        about_window = tk.Toplevel(self.root)
        about_window.title(self.texts[self.lang]['about_title'])
        about_window.resizable(False, False)
        self.center_window(about_window)

        try:
            about_image_original = tk.PhotoImage(file=self.icon_path)
            about_image = about_image_original.subsample(5, 5)

            image_label = tk.Label(about_window, image=about_image)
            # ¡Importante! Mantener la referencia a la imagen. / Important! Keep the reference to the image.
            image_label.image = about_image
            image_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading the icon: {e}")

        label_version = tk.Label(
            about_window, text=f"{self.texts[self.lang]['version']} {version}")
        label_about = tk.Label(
            about_window,
            text=self.texts[self.lang]['about'],
            wraplength=280
        )
        label_version.pack(padx=10, pady=10)
        label_about.pack(pady=10, padx=10)

    def show_history_window(self, history_files):
        """Muestra la ventana con el historial de escaneos / Shows the window with the scan history"""
        if not history_files:
            messagebox.showinfo(
                "Historial", self.texts[self.lang]['no_history_files'])
            return None

        history_window = tk.Toplevel(self.root)
        history_window.title(self.texts[self.lang]['history_title'])
        self.center_window(history_window, 200, 100)

        listbox = tk.Listbox(history_window, font=("Courier New", 12))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for file in history_files:
            listbox.insert(tk.END, file)

        open_button = ttk.Button(
            history_window,
            text=self.texts[self.lang]['open_result'],
            command=lambda: self.controller.open_history_file(listbox)
        )
        open_button.pack(pady=10)

        listbox.bind('<Double-Button-1>',
                     lambda e: self.controller.open_history_file(listbox))

        return history_window, listbox

    def show_history_file_content(self, selected_file, content):
        """Muestra el contenido de un archivo de historial / Shows the content of a history file"""
        result_window = tk.Toplevel(self.root)
        result_window.title(
            f"{self.texts[self.lang]['history_title']}: {selected_file}")
        self.center_window(result_window, 100, 200)

        text_square = tk.Text(result_window, wrap=tk.WORD,
                              font=("Courier New", 12))
        text_square.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_square.insert(tk.END, content)
        text_square.config(state="disabled")

    def update_version_label(self, text):
        """Actualiza la etiqueta de versión / Updates the version label"""
        self.label_version["text"] = text

    def set_update_button_state(self, is_up_to_date):
        """Actualiza el estado del botón de actualización de base de datos / Updates the database update button state"""
        if is_up_to_date:
            self.button_update_database.config(state="disabled")
            self.button_update_database["text"] = self.texts[self.lang]['database_updated']
        else:
            self.button_update_database.config(state="normal")
