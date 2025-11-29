# 🛠️ Registro de Depuración, Refactorización y Mejoras

Este documento detalla las intervenciones técnicas realizadas sobre el proyecto **"Sistema I.C.C. (Instituto de Ciencia Cuestionable)"**. El objetivo ha sido transformar un prototipo funcional en una aplicación robusta, segura y con una experiencia de usuario (UX) inmersiva.

## 1. Arquitectura y Configuración del Proyecto
*   **Implementación de Namespaces:** Se configuró `app_name = 'laboratorio'` en `urls.py` para aislar las rutas de la aplicación. Esto previene colisiones de nombres con otras apps y sigue las mejores prácticas de Django.
    *   *Acción:* Refactorización masiva de templates y vistas para usar la sintaxis `laboratorio:nombre_vista`.
*   **Corrección de Redirecciones:** Ajuste de `LOGIN_REDIRECT_URL` en `settings.py` para coincidir con el nuevo espacio de nombres.
*   **Script de Poblado Unificado:** Se consolidaron varios scripts de carga de datos en uno solo (`poblar_lab.py`), permitiendo generar un entorno de pruebas completo (Científicos, Componentes, Materiales, Inventos y Esbirros) con una sola ejecución.

## 2. Base de Datos y ORM (Optimización)
*   **Solución al problema N+1:** Se optimizó la vista del dashboard (`lista_inventos`) implementando `.prefetch_related('componentes')`. Esto reduce drásticamente las consultas a la base de datos al traer los inventos y sus relaciones Many-to-Many en una sola operación eficiente.
*   **Integridad de Datos:** Se aplicó la restricción `class Meta: unique_together` en el modelo intermedio `Receta`.
    *   *Resultado:* Ahora es imposible a nivel de base de datos asignar el mismo componente dos veces al mismo invento, previniendo duplicidad lógica.
*   **Eliminación de Raw SQL:** Se reemplazaron las consultas SQL crudas inseguras por métodos del ORM (`.order_by()`, `.filter()`), mejorando la seguridad contra inyecciones SQL y la portabilidad del código.
*   **Gestión de Archivos Media:** Implementación de funciones con `uuid` en `models.py` para renombrar archivos subidos, evitando sobrescritura de imágenes con el mismo nombre.

## 3. Lógica de Negocio y Backend
*   **Corrección de Bugs Lógicos:** Se solucionó un error en la vista `detalle_cientifico` donde no se enviaba el contexto de los esbirros al template, lo que causaba que la lista apareciera vacía.
*   **Integración Backend-Frontend (JSON):** Se implementó una lógica en `views.py` para serializar nombres de componentes y materiales reales de la base de datos y pasarlos como JSON al frontend. Esto alimenta el "Simulador de Mezclas" con datos vivos.
*   **Transacciones Atómicas:** Uso de `transaction.atomic()` en los formularios de creación/edición de inventos para asegurar la integridad de los datos entre el modelo padre y sus formsets hijos.

## 4. Interfaz de Usuario (UI) y Experiencia (UX)
*   **Identidad Visual (Cyberpunk/Sci-Fi):**
    *   Implementación de un tema oscuro personalizado con variables CSS (`--neon-green`, `--neon-purple`).
    *   Efectos visuales avanzados: **Scanlines** (efecto CRT), **Glitch** en títulos y **Shake** (temblor de pantalla) para feedback de errores o eliminaciones.
    *   Efecto **"Glow Radiactivo"** en todos los botones al interactuar (hover).
*   **Simulador Interactivo:** Desarrollo de un minijuego en JavaScript en la página de inicio que permite a los usuarios interactuar con el sistema sin estar logueados, aumentando el dinamismo.
*   **Formularios Dinámicos:** Configuración de `max_num=5` en los *Formsets* de ingredientes para mejorar la usabilidad y limitar la carga excesiva de datos.
*   **Feedback Visual:**
    *   Barras de progreso con colores semánticos (Rojo/Amarillo/Verde) según la probabilidad de éxito o lealtad.
    *   Corrección de estilos en etiquetas para visualización correcta de unidades (ej: gramos en minúscula).

## 5. Pruebas y Validación
*   Se realizaron pruebas manuales de flujo completo (CRUD) para asegurar que las nuevas restricciones de base de datos y validaciones de formularios (`clean()`) funcionan correctamente.
*   Verificación de manejo de errores 404 y 500 controlados.