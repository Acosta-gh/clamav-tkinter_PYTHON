
### 🇬🇧 English 

# 🛡️ YAGC (Yet Another GUI for ClamAV)

YAGC is a graphical user interface (GUI) designed to simplify the use of ClamAV, an open-source antivirus software. This application is inspired by projects such as ClamWin and ClamTk, offering users a more accessible and visual experience for quickly and easily performing antivirus scans on their systems.

## 🌟 Features

-   **Scan files or directories:** Select a file or folder to scan for viruses.
    
-   **Scan history:** Saves the results of each scan and allows you to view them later.
    
-   **Database update:** Updates the virus database using `freshclam`.
    
-   **ClamAV version detection:** Checks the installed version and the date of the last update.
    
## 🛠️ Requirements

-   Python 3.7+
    
-   ClamAV installed

-   GNU/Linux     

## 🛠️ Installation Guide 

1.  Clone this repository by opening a terminal and running the following commands:
    
```
git clone https://github.com/Acosta-gh/clamav-tkinter_PYTHON.git
cd clamav-tkinter
```

2. Create a virtual environment
It's a good practice to isolate your project dependencies using a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies (if needed):
    
Make sure you have `ttkbootstrap` installed. On Ubuntu/Debian, you can install it with:
```
pip install ttkbootstrap
```

4. You also need to have ClamAV installed:

```
sudo apt update
sudo apt install clamav clamav-daemon
```

5. Run the application

To open the graphical interface:

1. **Run the program**  
   Inside the terminal, type:
   ```
   python3 main.py
   ```

## Screenshots
![Image](https://github.com/user-attachments/assets/10a0fb3d-f318-441b-a127-47ce1decee50)

![Image](https://github.com/user-attachments/assets/12b176d7-35e8-439f-bf6f-b12b722eb85d)

![Image](https://github.com/user-attachments/assets/fe0d56e1-5fb8-4424-87a7-03f7a9b792c5)

![Image](https://github.com/user-attachments/assets/d69f013e-d5cd-437e-a664-3fedbdb64553)

![Image](https://github.com/user-attachments/assets/502a5fed-0c3f-41c7-bb91-de716407cc35)

## 📝 Tasks to be done
- [ ] Improve and optimize the code (High priority)
- [x] Switch from `ttk` to `tkbootstrap` (Medium priority)
- [ ] Continue implementing options after switching to `tkbootstrap` (Medium priority)
- [ ] Create an executable with `AppImage` (Low priority)
- [ ] Port the app to `GTK 3` (No priority)

Icon credit: <a href="https://pixabay.com/users/openicons-28911/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">OpenIcons</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">Pixabay</a>


### 🇪🇸 Español

# 🛡️ YAGC (En desarrollo)

YAGC es una interfaz gráfica de usuario (GUI) diseñada para facilitar el uso de ClamAV, un software antivirus de código abierto. Esta aplicación está inspirada en proyectos como ClamWin y ClamTk, y ofrece una experiencia más accesible y visual para los usuarios que desean realizar escaneos antivirus en sus sistemas de forma rápida y sencilla.

## 🌟 Características

-   **Escanear archivos o directorios:** Selecciona un archivo o carpeta para escanear en busca de virus.
    
-   **Historial de escaneos:** Guarda los resultados de cada escaneo y permite verlos posteriormente.
    
-   **Actualización de la base de datos:** Actualiza la base de datos de virus usando `freshclam`.
    
-   **Detección de versión de ClamAV:** Verifica la versión instalada y la fecha de la última actualización.
    

## 🛠️ Requisitos

-   Python 3.7+
    
-   ClamAV instalado

-   GNU/Linux    

En Ubuntu/Debian, puedes instalar ClamAV con:

```
sudo apt update
sudo apt install clamav clamav-daemon
```

## 🛠️ Guía de Instalación

1. Clona este repositorio abriendo una terminal y ejecutando los siguientes comandos:

```
git clone https://github.com/Acosta-gh/clamav-tkinter_PYTHON.git
cd clamav-tkinter
```

2. Crear un entorno virtual
Es una buena práctica aislar las dependencias de tu proyecto utilizando un entorno virtual:
```
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias (si es necesario):

Asegúrate de tener `tkinter` instalado. En Ubuntu/Debian, puedes instalarlo con:

```
sudo apt install python3-tk
```

4. También necesitas tener ClamAV instalado:

```
sudo apt update
sudo apt install clamav clamav-daemon
```

5. Ejecuta la aplicación

Para abrir la interfaz gráfica:

1. **Ejecuta el programa**  
   Dentro de la terminal, escribe:
   ```
   python3 main.py
   ```

## Imagenes
![Image](https://github.com/user-attachments/assets/bb599918-1d52-4537-bb00-ac41cdca3a81)

![Image](https://github.com/user-attachments/assets/6a678025-3f61-4de7-88d7-4c645e59c271)

![Image](https://github.com/user-attachments/assets/d92560dc-5c04-4234-977d-ab4c53e4ffdc)

![Image](https://github.com/user-attachments/assets/ba98efa9-e766-4538-a510-c69e7224e645)

![Image](https://github.com/user-attachments/assets/4eecd471-0bda-409a-ae42-9aef48f4cfc7)


## 📝 Tareas por hacer
- [ ] Mejorar y optimizar el código (Prioridad alta)
- [x] Cambiar de `ttk` a `tkbootstrap` (Prioridad media)
- [ ] Seguir implementando opciones después de cambiar a `tkbootstrap` (Prioridad media)
- [ ] Crear un ejecutable con `AppImage` (Prioridad baja)
- [ ] Portear la aplicación a `GTK 3` (Prioridad nula)

Crédito del icono: <a href="https://pixabay.com/users/openicons-28911/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">OpenIcons</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">Pixabay</a>
