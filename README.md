# Módulo de registrar productos 

Aplicación web desarrollada en Django + Tailwind css para registrar, consultar, actualizzar y eliminar productos de una tienda piloto (referencia de 1200 registros). 

Loa datos se alamcenan de forma persistente en un archivo de texto en formato JSON (`products.json`).

## 1. Requisitos
- Python 3.9 o superior (probado en 3.9)
- Git
- Acceso a una teminal(CMD, PowerShell o terminal de VS Code)


## 2. Instalación y Ejecución

### 2.1 Comprobar si está instalado python y git
```
python --version
git --version
```


### 2.2 Clonar el repositorio
```
git clone ....
cd ef
```


### 2.3 Crear y activar el entorno virtual
```
python -m venv venv
```

Si utiliza CMD (Simbolo del sistema)
```
venv\Scripts\activate.bat
```

Si utiliza Powershell
```
.\venv\Scripts\Activate.ps1
```

Si utiliza la terminal de VSCode
```
.\venv\Scripts\Activate.ps1
```

Para comprobar que se actuvó correctamente, aparecerá (venv) al inicio de la linea de la terminal, por ejemplo:
```
(venv) C:\proyectos\mi-tienda>
```


### 2.4 Instalar las dependencias
Con el entorno virtual activado ejecura: 
```
python -m pip install -r requirements.txt 
```


### 2.5 Preparar la base de datos de Django
```
python manage.py migrate
```
Solo crea las tablas internas de Django (`db.sqlite3`). Los productos no se guardarán ahí.


### 2.6 Cargar los datos de prueba (Opcional)
Si necesitas generar los productos de prueba y todavía no cuentas con los datos, ejecuta:
```
python manage.py seed_products

```
Si los datos están en `products.json` se puede omitir este paso.


### 2.7 Iniciar el servidor
```
python manage.py runserver
```

Abrir en el navegador: <http://127.0.0.1:8000>


### 2.8 Actualizar dependencias (Si es necesario)
Con el entorno activo
```
python -m pip freeze > requirements.txt
```


## 3. ¿Cómo volver a ejecutar el proyecto?
No necesita repetir toda la instalación. Debe hacer lo siguiente:

1. Abrir una terminal en la carpeta del proyecto.
2. Activar el entorno virtual.
3. Ejecutar el servidor.

```
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

Cuando termine puede detener el servidor con Ctrl + C y salir del entorno virtual con:
```
deactivate
```