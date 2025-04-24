import threading
from tkinter import filedialog
import os
from model.config_model import ConfigModel
from pathlib import Path

VERSION = "0.0.5"


class ClamAVController:
    def __init__(self, model, texts):
        self.model = model
        self.texts = texts

        # Ruta al archivo de configuración en $HOME/ClamAVTkinter/.config.json / Path to the configuration file in $HOME/ClamAVTkinter/.config.json
        self.path_config_file = Path.home() / "ClamAVTkinter" / ".config.json"
        self.path_config_file.parent.mkdir(parents=True, exist_ok=True)  # Asegura que exista el directorio / Ensure the directory exists
        self.path_config_file.touch(exist_ok=True)  # Crea el archivo si no existe / Create the file if it doesn't exist

        # Cargar la configuración / Load the configuration
        self.config = ConfigModel(str(self.path_config_file))
        self.lang = self.config.load()["lang"]
        self.view = None

    def set_view(self, view):
        """Establece la referencia a la vista / Sets the reference to the view"""
        self.view = view
        self.get_version()

    def change_lang(self, lang):
        """Cambia el idioma de la aplicación / Changes the language of the application"""
        self.lang = lang
        self.view.lang = lang
        self.view.update_texts()
        self.get_version()
        self.config.save(
            {
                "lang": self.lang,
            }
        )

    def scan_a_file(self):
        """Inicia el escaneo de un archivo / Starts scanning a file"""
        path = filedialog.askopenfilename(
            title=self.texts[self.lang]['select_file'],
            filetypes=[
                (self.texts[self.lang]['all_files'], "*.*"),
                (self.texts[self.lang]['text_files'], "*.txt"),
                (self.texts[self.lang]['image_files'], "*.png *.jpg *.jpeg"),
            ],
            initialdir=os.path.expanduser("~")
        )
        if path:
            self.start_scan(path)

    def scan_a_directory(self):
        """Inicia el escaneo de un directorio / Starts scanning a directory"""
        path = filedialog.askdirectory(
            title=self.texts[self.lang]['select_directory'],
            initialdir=os.path.expanduser("~")
        )
        if path:
            self.start_scan(path)

    def start_scan(self, path):
        """Inicia el proceso de escaneo en un hilo separado / Starts the scanning process in a separate thread"""
        recursive = self.view.checkbox_var_recursive.get() == 1
        remove_threats = self.view.checkbox_var_kill.get() == 1

        scan_window, progressbar, label_loading = self.view.show_scan_window(
            path)

        # Inicia el escaneo en un hilo / Starts the scan in a thread
        threading.Thread(
            target=self.model.run_scan_thread,
            args=(path, recursive, remove_threats),
            daemon=True
        ).start()

        # Comprueba el estado del escaneo periódicamente / Checks the scan status periodically
        self.view.root.after(100, self.check_scan_status,
                             scan_window, progressbar, label_loading)

    def check_scan_status(self, scan_window, progressbar, label_loading):
        """Comprueba si el escaneo ha finalizado / Checks if the scan has finished"""
        try:
            result = self.model.result_queue.get_nowait()
        except Exception:  # queue.Empty
            self.view.root.after(100, self.check_scan_status,
                                 scan_window, progressbar, label_loading)
            return

        if progressbar.winfo_exists():
            progressbar.stop()
            progressbar.destroy()

        if label_loading.winfo_exists():
            label_loading.destroy()

        # Guarda los resultados del escaneo / Saves the scan results
        filepath = self.model.save_scan_result(
            result) if not isinstance(result, Exception) else ""

        # Muestra los resultados / Shows the results
        self.view.show_scan_results(scan_window, result, filepath)

    def view_history(self):
        """Muestra la ventana de historial / Shows the history window"""
        history_files = self.model.get_history_files()
        self.view.show_history_window(history_files)

    def open_history_file(self, listbox):
        """Abre un archivo de historial seleccionado / Opens a selected history file"""
        selected_index = listbox.curselection()
        if not selected_index:
            return

        selected_file = listbox.get(selected_index)
        content = self.model.read_history_file(selected_file)

        self.view.show_history_file_content(selected_file, content)

    def update_database(self):
        """Actualiza la base de datos de ClamAV / Updates the ClamAV database"""
        result = self.model.update_database()

        if "Failed to lock the log file" in result.stderr:
            self.view.update_version_label(
                self.texts[self.lang]['database_locked'])
        elif result.returncode != 0:
            self.view.update_version_label(
                f"{self.texts[self.lang]['database_update_error']}\n{result.stderr}")
        else:
            self.view.update_version_label(
                self.texts[self.lang]['database_updated'])

        if "Problem with internal logger" in result.stderr or result.returncode == 0:
            self.view.update_version_label(
                self.texts[self.lang]['database_up_to_date'])

    def get_version(self):
        """Obtiene la información de versión de ClamAV"""
        version_info = self.model.get_version()

        if "error" in version_info:
            self.view.update_version_label(version_info["error"])
            return

        version = version_info["version"]
        db_date = version_info["db_date"]
        current_date = version_info["current_date"]

        # Formatear fechas para comparación / Format dates for comparison
        version_date_formatted = db_date.strftime("%Y-%m-%d")
        current_date_formatted = current_date.strftime("%Y-%m-%d")

        # Actualizar la etiqueta con la información de versión / Update the label with version information
        self.view.update_version_label(
            f"{self.texts[self.lang]['version_label']} {version}\n"
            f"{self.texts[self.lang]['database_updated_on']} {db_date}"
        )

        # Actualizar el estado del botón de actualización / Update the update button state
        is_up_to_date = (current_date_formatted == version_date_formatted)
        self.view.set_update_button_state(is_up_to_date)

    def view_about(self):
        """Muestra la ventana 'Acerca de' / Shows the 'About' window"""
        self.view.show_about_window(VERSION)
