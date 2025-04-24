import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from datetime import datetime
from tkinter import PhotoImage
import os
import json
from model.config_model import ConfigModel


class ClamAVView:
    def __init__(self, root, controller, texts):
        self.root = root
        self.controller = controller

        # Cargar el archivo de configuración / Load the configuration file
        path_current_file = os.path.dirname(__file__)
        project_root = os.path.dirname(path_current_file)
        self.path_config_file = os.path.join(project_root, ".config.json")
        self.config = ConfigModel(self.path_config_file)

        # Cargar la configuración / Load the configuration
        self.lang = self.config.load()["lang"]
        self.texts = texts

        # Cargar el icono / Load the icon
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.parent_dir = os.path.dirname(self.script_dir)
        self.icon_path = os.path.join(self.parent_dir, "shield.png")

        try:
            self.icon_image = PhotoImage(file=self.icon_path)
            self.root.iconphoto(True, self.icon_image)
        except Exception as e:
            print(f"Error loading the icon: {e}")

        # Variables de configuración / Configuration variables
        self.checkbox_var_recursive = tk.IntVar(
            value=self.config.load()["recursive"])
        self.checkbox_var_kill = tk.IntVar(value=self.config.load()["kill"])

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
        # self.controller.get_version()  # Esto se realiza en el método set_view del controlador / This is done in the set_view method of the controller

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
        self.tabs_notebook = ttk.Notebook(self.root)
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
        self.button_scan_a_file.pack(fill="x", pady=10, padx=10)

        self.button_scan_a_directory = ttk.Button(
            self.scan_frame,
            text=self.texts[self.lang]["button_label2"],
            command=self.controller.scan_a_directory
        )
        self.button_scan_a_directory.pack(fill="x", pady=5, padx=10)

        self.button_view_history = ttk.Button(
            self.history_frame,
            text=self.texts[self.lang]["button_label3"],
            command=self.controller.view_history
        )
        self.button_view_history.pack(fill="x", pady=10, padx=10)

        self.button_update_database = ttk.Button(
            self.update_frame,
            text=self.texts[self.lang]["button_label4"],
            command=self.controller.update_database
        )
        self.button_update_database.pack(fill="x", padx=10, pady=10)

        # Botón para guardar la configuración / Button to save the configuration
        self.button_save_config = ttk.Button(
            self.config_frame,
            text=self.texts[self.lang]["button_label5"],
            command=lambda: (
                self.config.save(
                    {
                        "recursive": self.checkbox_var_recursive.get(),
                        "kill": self.checkbox_var_kill.get()
                    }
                ),
                self.button_save_config.config(text=self.texts[self.lang]['changes_saved']),
                self.root.after(2000, lambda: self.button_save_config.config(text=self.texts[self.lang]['button_label5']))
            )
        )

        self.label_version = ttk.Label(
            self.update_frame, text="", wraplength=280)
        self.label_version.pack(padx=10, pady=10)

    def create_checkboxes(self):
        """Crea los checkboxes de configuración / Creates the configuration checkboxes"""
        self.checkbox_recursive = tk.Checkbutton(
            self.config_frame,
            text=self.texts[self.lang]['recursive_search'],
            variable=self.checkbox_var_recursive
        )
        self.checkbox_kill = tk.Checkbutton(
            self.config_frame,
            text=self.texts[self.lang]['delete_threats'],
            variable=self.checkbox_var_kill
        )

        self.checkbox_recursive.pack(pady=5, padx=5, anchor="w")
        self.checkbox_kill.pack(pady=5, padx=5, anchor="w")
        self.button_save_config.pack(fill="x", padx=10, pady=10)

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
        self.checkbox_kill.config(
            text=self.texts[self.lang]["checkbox_label2"])

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
        about_window.title("About")
        self.center_window(about_window)

        try:
            about_image_original = tk.PhotoImage(file=self.icon_path)
            about_image = about_image_original.subsample(3, 3)

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
