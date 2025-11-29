# 🧪 Instituto de Ciencia Cuestionable (I.C.C.)

> **Sistema de Gestión Integral para Laboratorios de Dudosa Ética**
> *Proyecto de Portafolio --- Backend con Django + Frontend Interactivo*

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![Cyberpunk](https://img.shields.io/badge/Theme-Cyberpunk-bc13fe?style=for-the-badge&logo=dependabot&logoColor=white)

------------------------------------------------------------------------

## 📋 Descripción del proyecto

Aplicación web desarrollada en **Django** siguiendo la arquitectura
**MVT**. Su objetivo es administrar recursos críticos de un laboratorio
"Mad Science": inventarios de materiales peligrosos, gestión de personal
(científicos y esbirros) y prototipos inestables.

El proyecto ha evolucionado de un CRUD estándar a una **experiencia
inmersiva** con una interfaz temática **Cyberpunk/Sci-Fi**,
interactividad en tiempo real mediante JavaScript y un backend
optimizado y seguro.

------------------------------------------------------------------------

## 🚀 Nuevas Características y Mejoras

### 🎨 Experiencia de Usuario (UX/UI)

-   **Identidad Visual Cyberpunk:** Tema oscuro personalizado con paleta
    de colores neón (Verde/Morado), fuentes tecnológicas (*Orbitron*,
    *Share Tech Mono*) y fondo de grilla.
-   **Efectos Visuales Avanzados:** Animaciones CSS de **Glitch** en
    títulos, efecto de **monitor CRT** (scanlines), y **Glow
    radiactivo** en botones interactivos.
-   **Simulador de Mezclas:** Minijuego en la página de inicio
    (JavaScript + JSON Django) que permite simular la creación de
    elementos utilizando datos reales de la base de datos sin necesidad
    de login.
-   **Feedback Inmersivo:** Animaciones de "Temblor de pantalla"
    (`Shake`) al eliminar registros o fallar experimentos.

### 🛠️ Arquitectura y Backend

-   **Optimización de Consultas:** Solución al problema *N+1* mediante
    `prefetch_related` y `select_related`, reduciendo drásticamente la
    carga en el dashboard.
-   **Integridad de Datos:** Restricciones `unique_together` en modelos
    intermedios para evitar duplicidad de componentes.
-   **Namespacing:** Implementación de `app_name = 'laboratorio'` para
    un enrutamiento robusto y escalable.
-   **Gestión de Archivos:** Renombrado automático de imágenes mediante
    UUID para evitar colisiones.

------------------------------------------------------------------------

## 📄 Documentación Técnica

Para ver el detalle técnico de la refactorización, depuración de errores
y mejoras de código aplicadas, consulta el archivo:\
👉 **CORRECCIONES_Y\_MEJORAS.md**

------------------------------------------------------------------------

## ⚙️ Requisitos

-   Python 3.10+\
-   Django 5.x\
-   PostgreSQL 14+\
-   Dependencias listadas en `requirements.txt`

------------------------------------------------------------------------

## 🔧 Instalación y Despliegue

Sigue estos pasos para ejecutar el proyecto con todas sus nuevas
funcionalidades.

``` bash
# 1. Clonar el repositorio
git clone <URL_DE_TU_REPOSITORIO>
cd iqs_project

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows:
.env\Scriptsctivate
# Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Configuración de Base de Datos

Crea la base en PostgreSQL:

``` sql
CREATE DATABASE iqs_db;
```

Ajusta las credenciales en `mad_science/settings.py`.

Ejecuta las migraciones:

``` bash
python manage.py migrate
```

------------------------------------------------------------------------

## 🧪 Poblado de Datos (Script Unificado)

Olvídate de cargar JSONs antiguos. Se creó un script maestro que genera
científicos, materiales, componentes, inventos y recluta esbirros
automáticamente:

``` bash
python poblar_lab.py
```

------------------------------------------------------------------------

## ▶️ Uso del sistema

``` bash
python manage.py runserver
```

Accede: http://127.0.0.1:8000/

------------------------------------------------------------------------

## 📂 Estructura del proyecto

``` text
iqs_project/
├── mad_science/
├── laboratorio/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── media/
├── poblar_lab.py
├── CORRECCIONES_Y_MEJORAS.md
└── manage.py
```
