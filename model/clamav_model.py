import subprocess
import os
from datetime import datetime
from pathlib import Path
import queue


class ClamAVModel:
    def __init__(self):

        # Inicializa el directorio de historial / Initialize the history directory
        base_dir = Path.home() / "ClamAVTkinter"
        base_dir.mkdir(exist_ok=True)
        self.history_dir = base_dir / "ClamAV_History"
        self.history_dir.mkdir(exist_ok=True)
        self.infected_files_dir = base_dir / "Infected_Files"
        self.infected_files_dir.mkdir(exist_ok=True)

        # Inicializa la cola de resultados / Initialize the result queue
        self.result_queue = queue.Queue()
        self.version_info = {"version": "", "db_date": None}

    """
    def is_clamav_installed(self):
        try:
            subprocess.run(["clamscan", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError:
            return False
    """
    
    def run_scan_thread(self, path, recursive=False, remove_threats=False, move_to_quarantine=False, bell=True):
        """Ejecuta un escaneo en un hilo y lo pone en una cola / Runs a scan in a thread and puts it in a queue"""
        args = ['clamscan'] # Comando de ClamAV / ClamAV command

        if recursive:
            args.append('-r')

        if remove_threats:
            args.append('--remove')

        if bell:
            args.append('--bell')

        if move_to_quarantine:
            args.append(f'--move={self.infected_files_dir}')

        if remove_threats and move_to_quarantine:
            raise ValueError("No se puede usar '--remove' y '--move' al mismo tiempo.")
        
        args.append(path) # Agrega la ruta al final de los argumentos / Adds the path at the end of the arguments
        print(f"Running scan with args: {args}")
        try:
            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.result_queue.put(result)
        except Exception as e:
            self.result_queue.put(e)

    def save_scan_result(self, result):
        """Guarda el resultado del escaneo en un archivo / Saves the scan result to a file"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}.txt"
        filepath = self.history_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Standard output:\n")
            f.write(result.stdout)
            f.write(f"\nError output:\n")
            f.write(result.stderr)

        return filepath

    def get_history_files(self):
        """Retorna la lista de archivos de historial / Returns the list of history files"""
        return sorted([f for f in os.listdir(self.history_dir)], reverse=True)

    def read_history_file(self, filename):
        """Lee un archivo de historial / Reads a history file"""
        filepath = self.history_dir / filename
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def update_database(self):
        """Actualiza la base de datos de ClamAV / Updates the ClamAV database"""
        result = subprocess.run(["pkexec", "freshclam"], capture_output=True, text=True)
        return result

    def get_version(self):
        """Obtiene la versión de ClamAV y la fecha de la base de datos / Gets the ClamAV version and database date"""
        try:
            result = subprocess.run(["clamscan", "--version"], capture_output=True, text=True)
            
            if result.returncode == 0:
                first_line = result.stdout.strip().split("\n")[0]
                parts = first_line.split("/")
                if len(parts) >= 3:
                    version = parts[0].replace("ClamAV", "").strip()
                    version_date_str = parts[2].strip()
                    date_version = datetime.strptime(version_date_str, "%a %b %d %H:%M:%S %Y")
                    
                    self.version_info = {
                        "version": version,
                        "db_date": date_version,
                        "current_date": datetime.now()
                    }
                    return self.version_info
                else:
                    return {"error": "Unexpected version format"}
            else:
                return {"error": "Failed to fetch ClamAV version"}
        except Exception as e:
            return {"error": str(e)}
