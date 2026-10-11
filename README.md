# Módulo de registrar productos 

Aplicación web desarrollada en Django + Tailwind css para registrar, consultar, actualizzar y eliminar productos de una tienda piloto (referencia de 1200 registros). 

Loa datos se almacenan de forma persistente en un archivo de texto en formato JSON (`products.json`).

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

En Windows, si Python no es reconocido prueba con el lanzador (py) 
```
py --version
```
**Nota:** en los pasos siguientes se usa `python`. Si en tu equipo solo funciona `py`, reemplaza `python` por `py` **únicamente al crear el entorno virtual** (paso 2.3). Con el entorno activado, `python` ya funciona.

### 2.2 Clonar el repositorio
```
git clone https://github.com/valdir169/register_products_module.git
cd register_products_module
```


### 2.3 Crear y activar el entorno virtual
```
python -m venv venv
```
 
o, si usas el lanzador de Windows:
 
```
py -m venv venv
```

Activarlo, según la terminal que uses:
 
| Terminal | Comando |
|---|---|
| CMD (Símbolo del sistema) | `venv\Scripts\activate.bat` |
| PowerShell | `.\venv\Scripts\Activate.ps1` |
| Terminal de VS Code (usa PowerShell por defecto) | `.\venv\Scripts\Activate.ps1` |
| Linux o macOS | `source venv/bin/activate` |
 
Para comprobar que se activó, aparecerá `(venv)` al inicio de la línea de la terminal, por ejemplo:
```
(venv) C:\proyectos\mi-repo>
```

**Si PowerShell muestra el error "la ejecución de scripts está deshabilitada en este sistema":** ejecuta este comando y vuelve a activar el entorno. Solo afecta a la terminal actual:
 
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```


### 2.4 Instalar las dependencias
Con el entorno virtual activado ejecuta: 
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
