import threading
import os
from datetime import datetime


VERSION = "0.1.25"


class ClamAVController:
    def __init__(self, clamav_model, config_model, texts):
        self.model = clamav_model # Me gustaría no usar self.model y en su defecto usar self.clamav_model, pero no quiero cambiar el nombre de todos los métodos / I would like to not use self.model and instead use self.clamav_model, but I don't want to change the name of all the methods
        self.config = config_model # Me gustaría no usar self.config y en su defecto usar self.config_model, pero no quiero cambiar el nombre de todos los métodos / I would like to not use self.config and instead use self.config_model, but I don't want to change the name of all the methods
        self.texts = texts
        self.lang = self.config.load()["lang"]
        self.view = None

    def set_view(self, view):
        """Establece la referencia a la vista / Sets the reference to the view"""
        self.view = view
        self.check_if_installed() 

        # self.check_if_clamav_installed()  
        # Debo hacer esto en set_view porque la vista se inicializa antes de que el controlador / I have to do this in set_view because the view is initialized before the controller
        # Si check_if_clamav_installed intentaba obtener la versión de clamav y fallaba significaba que clamav no estaba instalado, sin embargo self.get_version() ya lo hace por lo que no es necesario / check_if_clamav_installed was trying to get the clamav version and failed, meaning clamav was not installed, however self.get_version() already does it so it's not necessary
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

    """
    def check_if_clamav_installed(self):
        # Verifica si ClamAV está instalado / Checks if ClamAV is installed
        if not self.model.is_clamav_installed():
            self.view.show_error_message(self.texts[self.lang]['clamav_not_installed'])
            self.view.disable_buttons()
            return False
        return True
    """

    def scan_a_file(self):
        """Inicia el escaneo de un archivo / Starts scanning a file"""
        path = self.view.ask_file()
        if path:
            self.start_scan(path)

    def scan_a_directory(self):
        """Inicia el escaneo de un directorio / Starts scanning a directory"""
        path = self.view.ask_directory()
        if path:
            self.start_scan(path)

    def start_scan(self, path):
        """Inicia el proceso de escaneo en un hilo separado / Starts the scanning process in a separate thread"""
        # Recupera los valores de los checkboxes para determinar los argumentos del escaneo / Retrieves the checkbox values to determine the scan arguments
        recursive = self.view.checkbox_var_recursive.get() == 1
        bell = self.view.bell_var.get() == 1
        action = self.view.combobox_var.get()

        # Determina la acción a realizar según la opción seleccionada / Determines the action to take based on the selected option
        if (action == 0):
            remove_threats = False
            move_to_quarantine = False
        elif (action == 1):
            remove_threats = False
            move_to_quarantine = True
        elif (action == 2):
            remove_threats = True
            move_to_quarantine = False

        # Muestra la ventana de escaneo / Shows the scan window
        scan_window, progressbar, label_loading = self.view.show_scan_window(
            path)

        # Inicia el escaneo en un hilo / Starts the scan in a thread
        threading.Thread(
            target=self.model.run_scan_thread,
            args=(path, recursive, remove_threats, move_to_quarantine, bell),
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

    def check_if_installed(self):
        if(self.model.check_if_installed()):
            #self.view.update_version_label(version_info["error"])
            self.view.show_error_message(self.texts[self.lang]['clamav_not_installed'])
            self.view.disable_buttons()
            return
        
    def get_version(self):
        """Obtiene la información de versión de ClamAV"""
        version_info = self.model.get_version()

        version = version_info.get("version", "desconocida")
        db_date = version_info.get("db_date")
        current_date = version_info.get("current_date", datetime.now())

        if db_date:
            version_date_formatted = db_date.strftime("%Y-%m-%d")
            current_date_formatted = current_date.strftime("%Y-%m-%d")

            is_up_to_date = (current_date_formatted == version_date_formatted)
            db_date_str = db_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            is_up_to_date = False
            db_date_str = "fecha desconocida"

        self.view.update_version_label(
            f"{self.texts[self.lang]['version_label']} {version}\n"
            f"{self.texts[self.lang]['database_updated_on']} {db_date_str}"
)
        self.view.set_update_button_state(is_up_to_date)

    def view_about(self):
        """Muestra la ventana 'Acerca de' / Shows the 'About' window"""
        self.view.show_about_window(VERSION)
