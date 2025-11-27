# 🧪 Instituto de Ciencia Cuestionable (I.C.C.)

> **Sistema de Gestión Integral para Laboratorios de Dudosa Ética**
> *Proyecto de Portafolio — Backend con Django*

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge\&logo=django\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge\&logo=postgresql\&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-563D7C?style=for-the-badge\&logo=bootstrap\&logoColor=white)

---

## 📋 Descripción del proyecto

Aplicación web desarrollada en **Django** siguiendo la arquitectura **MVT (Modelo — Vista — Template)**. Su objetivo es administrar recursos críticos de un laboratorio: inventarios (incluso materiales peligrosos), gestión de personal, y experimentos. Incluye interfaz moderna (Dark Mode), gestión de imágenes y una base de datos relacional bien estructurada.

---

## ✅ Características principales

* **Modelado de datos avanzado**

  * Entidades: `Materiales`, `Científicos`, `Esbirros`, `Inventos`, `Componentes`, `Protocolos`.
  * Relaciones 1:N: Científico → Esbirros.
  * Relaciones N:N: Inventos ↔ Componentes mediante tabla intermedia `Receta` (control de cantidades).
  * Relaciones 1:1: Protocolo de seguridad único por Invento.

* **CRUD y vistas**

  * Operaciones completas (Crear, Leer, Actualizar, Eliminar) para todos los modelos.
  * Formularios avanzados: `ModelForms` e `InlineFormsets` para editar Inventos y sus Componentes en una sola pantalla.
  * Consultas optimizadas: uso de `select_related`, `prefetch_related`, `annotate` y, cuando procede, SQL crudo para reportes.

* **Seguridad y UX**

  * Autenticación y protección de vistas (`@login_required`).
  * Mensajería (toasts) para feedback de acciones.
  * Diseño responsivo con Bootstrap 5 y tema oscuro.

---

## ⚙️ Requisitos

* Python 3.10+
* Django 5.x
* PostgreSQL 14/15/16
* Dependencias listadas en `requirements.txt`

---

## 🚀 Instalación (local)

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

```bash
# Clonar el repositorio
git clone <URL_DE_TU_REPOSITORIO>
cd iqs_project

# Crear y activar entorno virtual
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Configurar base de datos (PostgreSQL)

1. Crea la base de datos (ejemplo):

```sql
CREATE DATABASE iqs_db;
```

2. Ajusta las credenciales en `mad_science/settings.py` (variables: `DATABASES`, `USER`, `PASSWORD`, `HOST`, `PORT`).

3. Ejecuta migraciones:

```bash
python manage.py migrate
```

4. (Opcional) Cargar datos de ejemplo:

```bash
python manage.py loaddata iqs_datos.json
```

---

## ▶️ Uso del sistema

```bash
# Iniciar servidor de desarrollo
python manage.py runserver
```

Accede en el navegador: `http://127.0.0.1:8000/`

* Usuario admin: el que viene en `iqs_datos.json` o crea uno nuevo con:

```bash
python manage.py createsuperuser
```

---

## 📂 Estructura del proyecto (resumen)

```
iqs_project/
├── mad_science/            # Configuración del proyecto (settings, urls)
├── laboratorio/            # App principal
│   ├── migrations/         # Historial de migraciones
│   ├── templates/          # Plantillas HTML
│   ├── static/             # CSS, JS, imágenes
│   ├── admin.py            # Config admin
│   ├── forms.py            # Formularios y formsets
│   ├── models.py           # Modelos de datos
│   ├── urls.py             # Rutas de la app
│   └── views.py            # Lógica y controladores
├── media/                  # Archivos subidos por usuarios
├── iqs_datos.json          # Backup con datos de ejemplo
├── poblar_masivo.py        # Script para generación masiva de datos
└── manage.py               # Comandos de Django
```
