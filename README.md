
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
git clone https://github.com/tu-usuario/clamav-tkinter.git
cd clamav-tkinter
```

2.  Install dependencies (if needed):
    
Make sure you have `tkinter` installed. On Ubuntu/Debian, you can install it with:
```
sudo apt install python3-tk
```

3. You also need to have ClamAV installed:

```
sudo apt update
sudo apt install clamav clamav-daemon
```

4. Run the application

To open the graphical interface:

1. **Open a terminal**  

2. **Navigate to the project folder**  
   If you followed the steps above:
   ```
   cd ~/clamav-tkinter
   ```

3. **Run the program**  
   Inside the terminal, type:
   ```
   python3 main.py
   ```

## Screenshots
![Image](https://github.com/user-attachments/assets/af91a543-87f0-4411-a670-b4210452302e)

![Image](https://github.com/user-attachments/assets/a04a4c49-063b-42e5-acd4-17b4f46776cd)

![Image](https://github.com/user-attachments/assets/f5ccb8e2-d5c3-4e0f-9a00-562211694d3a)

![Image](https://github.com/user-attachments/assets/09942eda-4fe3-464f-adcc-77ea57ba5df4)

![Image](https://github.com/user-attachments/assets/dfb5e2d8-8416-4692-869a-cd85de794463)


## 📝 Tasks to be done
- [ ] Improve and optimize the code (High priority)
- [x] Switch from `ttk` to `tkbootstrap` (Medium priority)
- [ ] Continue implementing options after switching to `tkbootstrap` (Medium priority)
- [ ] Create an executable with `AppImage` (Low priority)
- [ ] Port the app to `GTK 3` (No priority)

Icon credit: : <a href="https://pixabay.com/users/openicons-28911/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">OpenIcons</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">Pixabay</a>


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
git clone https://github.com/tu-usuario/clamav-tkinter.git
cd clamav-tkinter
```

2. Instala las dependencias (si es necesario):

Asegúrate de tener `tkinter` instalado. En Ubuntu/Debian, puedes instalarlo con:

```
sudo apt install python3-tk
```

3. También necesitas tener ClamAV instalado:

```
sudo apt update
sudo apt install clamav clamav-daemon
```

4. Ejecuta la aplicación

Para abrir la interfaz gráfica:

1. **Abre una terminal**

2. **Navega a la carpeta del proyecto**  
   Si seguiste los pasos anteriores:
   ```
   cd ~/clamav-tkinter
   ```

3. **Ejecuta el programa**  
   Dentro de la terminal, escribe:
   ```
   python3 main.py
   ```

## Imagenes
![Image](https://github.com/user-attachments/assets/af91a543-87f0-4411-a670-b4210452302e)

![Image](https://github.com/user-attachments/assets/a04a4c49-063b-42e5-acd4-17b4f46776cd)

![Image](https://github.com/user-attachments/assets/f5ccb8e2-d5c3-4e0f-9a00-562211694d3a)

![Image](https://github.com/user-attachments/assets/09942eda-4fe3-464f-adcc-77ea57ba5df4)

![Image](https://github.com/user-attachments/assets/dfb5e2d8-8416-4692-869a-cd85de794463)


## 📝 Tareas por hacer
- [ ] Mejorar y optimizar el código (Prioridad alta)
- [x] Cambiar de `ttk` a `tkbootstrap` (Prioridad media)
- [ ] Seguir implementando opciones después de cambiar a `tkbootstrap` (Prioridad media)
- [ ] Crear un ejecutable con `AppImage` (Prioridad baja)
- [ ] Portear la aplicación a `GTK 3` (Prioridad nula)

Crédito del icono: <a href="https://pixabay.com/users/openicons-28911/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">OpenIcons</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=98528">Pixabay</a>
