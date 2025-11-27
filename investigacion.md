
## 1. Características Fundamentales de la Integración (Requerimiento 1)

### Integración con Motores de Base de Datos
Django actúa como una capa de abstracción de alto nivel entre el código Python y el motor de base de datos. Esto permite desarrollar la aplicación agnóstica del motor subyacente. Aunque Django soporta SQLite por defecto, en este proyecto se configuró una conexión robusta con **PostgreSQL** utilizando el adaptador binario `psycopg2`.

La configuración se gestiona centralizadamente en `settings.py`, donde se definen las credenciales y el motor:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iqs_db',
        'USER': 'postgres',
        'PASSWORD': '***',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

  

El ORM de Django

Django maneja las operaciones mediante su ORM (Object-Relational Mapping). Este sistema mapea clases de Python a tablas de base de datos, atributos a columnas e instancias a filas. Esto elimina la necesidad de escribir SQL repetitivo para operaciones CRUD básicas, aumentando la seguridad contra inyecciones SQL y la velocidad de desarrollo.
2. Modelo de Acceso a Datos: Entidades No Relacionadas (Requerimiento 2)

Para resolver la problemática de gestión de insumos básicos del laboratorio, se implementó una entidad independiente que no requiere claves foráneas para existir.

    Modelo: MaterialSospechoso

    Función: Gestionar el inventario de la bodega ("Ectoplasma", "Uranio") de forma aislada a los experimentos o personal.

    Implementación: Se definieron campos con opciones limitadas (choices) para controlar la integridad de los datos (niveles de peligro).

code Python

    
class MaterialSospechoso(models.Model):
    nombre = models.CharField(max_length=100)
    nivel_peligro = models.CharField(choices=PELIGROSIDAD, ...)
    es_ilegal = models.BooleanField(default=True)
    stock_gramos = models.DecimalField(...)

  

3. Implementación de Relaciones entre Entidades (Requerimiento 3)

El núcleo del sistema "I.C.C." modela una realidad compleja mediante los tres tipos de relaciones relacionales soportadas por Django:
A. Relación Uno a Muchos (1:N) - ForeignKey

Se estableció que un Científico puede tener múltiples Esbirros a su cargo, pero un esbirro responde a un único líder.

    Código: cientifico = models.ForeignKey(Cientifico, ...) en el modelo Esbirro.

    Uso: Permite acceder a cientifico.esbirros.all() para listar el personal a cargo.

B. Relación Muchos a Muchos (N:N) - ManyToManyField

Un Invento se compone de múltiples Componentes, y un componente puede ser reutilizado en varios inventos.

    Solución Avanzada: Se utilizó una Tabla Intermedia (Receta) mediante el argumento through='Receta'.

    Motivo: Era necesario almacenar no solo qué componente se usa, sino la cantidad requerida para cada invento específico.

C. Relación Uno a Uno (1:1) - OneToOneField

Cada Invento posee un único Protocolo de Autodestrucción exclusivo.

    Código: invento = models.OneToOneField(Invento, ...) en el modelo ProtocoloAutodestruccion.

    Uso: Garantiza que no existan protocolos huérfanos ni inventos con múltiples botones de autodestrucción.

4. Manejo de Migraciones (Requerimiento 4)

Las migraciones son el sistema de control de versiones para el esquema de la base de datos. Durante el desarrollo del proyecto, este mecanismo fue vital para la evolución del software.

Caso Práctico de Propagación de Cambios:

    Problema: Inicialmente, el modelo Esbirro no tenía el atributo físico tiene_joroba.

    Modificación: Se agregó el campo models.BooleanField(default=True) en models.py.

    Generación: Se ejecutó python manage.py makemigrations, creando un archivo de instrucciones Python.

    Aplicación: Se ejecutó python manage.py migrate, lo que tradujo las instrucciones a SQL (ALTER TABLE ... ADD COLUMN) y actualizó la base de datos PostgreSQL sin perder la data existente.

5. Consultas de Filtrado y Consultas Personalizadas (Requerimiento 5)

En el "Centro de Mando" (Dashboard), se implementaron consultas avanzadas para la toma de decisiones:

    Filtrado (filter): Se recuperan inventos de alto riesgo.

        Invento.objects.filter(probabilidad_exito__lt=20)

    Exclusión (exclude): Se descartan inventos que son demasiado seguros.

        Invento.objects.exclude(probabilidad_exito__gt=80)

    Agregación y Anotaciones (annotate): Se calcula dinámicamente la cantidad de esbirros por científico, evitando el problema de N+1 consultas.

        Cientifico.objects.annotate(num_esbirros=Count('esbirros'))

    SQL Crudo (raw): Se implementó un log de auditoría utilizando SQL directo para demostración de flexibilidad.

        Invento.objects.raw('SELECT * FROM laboratorio_invento ...')

6. Arquitectura MVC/MVT y Operaciones CRUD (Requerimiento 6)

La aplicación sigue el patrón arquitectónico de Django MVT (Model-View-Template), equivalente al MVC tradicional:

    Model (Datos): Definición de Cientifico, Invento, etc. en models.py.

    View (Controlador): Lógica de negocio en views.py. Se implementaron vistas funcionales para realizar CRUD completo (Crear, Leer, Actualizar, Eliminar) en Inventos, Científicos, Esbirros y Materiales.

    Template (Vista): Interfaz de usuario en HTML/Bootstrap.

Destacado: Para la creación de Inventos complejos (Relación N:N), se utilizó inlineformset_factory junto con transaction.atomic(), permitiendo guardar el invento y sus componentes en una sola transacción segura.
7. Aplicaciones Preinstaladas (Requerimiento 7)

El proyecto integra las aplicaciones nativas de Django para funcionalidad robusta:

    django.contrib.admin:

        Uso: Gestión interna del sistema. Se personalizó utilizando TabularInline y StackedInline para permitir editar Esbirros y Protocolos directamente desde las fichas de Científicos e Inventos.

    django.contrib.auth:

        Uso: Sistema de seguridad. Se protegió el acceso a las operaciones de escritura (Crear/Editar/Borrar) mediante el decorador @login_required y se implementaron las vistas de Login/Logout.

    django.contrib.messages:

        Uso: Feedback al usuario. Se implementaron notificaciones "Toast" (Alertas verdes/rojas) tras completar operaciones CRUD exitosas o fallidas.

    django.contrib.staticfiles:

        Uso: Gestión de recursos. Permite servir archivos CSS, JS y las imágenes subidas por los usuarios (Media) para las fotos de los inventos y científicos.