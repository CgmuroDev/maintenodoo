README - Módulo de Seguimiento de Mantenimiento de Equipos

Descripción:

Este módulo de Odoo ha sido desarrollado para gestionar el mantenimiento preventivo de equipos industriales, proporcionando una visión clara del estado de los equipos, la planificación de mantenimientos y la generación de reportes.

Funcionalidades:

Modelos de Datos:
Equipo:
Gestión de información de equipos (nombre, categoría, fecha de instalación, etc.).
Generación automática de secuencias para el nombre del equipo (EQ/0001).
Control del estado del equipo (activo, inactivo, en reparación).
Mantenimiento Preventivo:
Planificación y registro de mantenimientos preventivos.
Asignación de técnicos y registro de fechas de ejecución.
Vistas Personalizadas:
Equipo:
Vista Kanban con código de colores para el estado del equipo.
Vista Gráfico de barras para la cantidad de equipos por categoría.
Mantenimiento:
Vista Calendario para visualizar mantenimientos programados.
Automatización:
Cron Jobs:
Notificación diaria de mantenimientos programados para el día siguiente.
Reportes PDF:
Generación de reportes con la lista de equipos, su último mantenimiento y estado.
Seguridad:
Grupo de seguridad "Técnico de Mantenimiento" con permisos restringidos.
Restricciones y Validaciones:
Restricción para no archivar equipos en estado "en reparación".
Validación para que la fecha de programación del mantenimiento sea igual o posterior a la fecha actual.
Manejo de errores
Se ha implementado el manejo de errores para las restricciones y validaciones, para que el usuario sea informado de forma clara, cuando existe un error en la información ingresada.
Requerimientos Técnicos:

Odoo (versión compatible).
Conocimientos de desarrollo de módulos en Odoo.
Instalación:

Coloca el directorio del módulo en el directorio de addons de tu instalación de Odoo.
Actualiza la lista de módulos en Odoo.
Instala el módulo "Seguimiento de Mantenimiento de Equipos".
Uso:

Crea registros de equipos y mantenimientos preventivos.
Utiliza las vistas Kanban, Gráfico y Calendario para visualizar la información.
Genera reportes PDF desde el menú de reportes.
Verifica que el cron job se ejecute correctamente.
Gestiona los permisos de acceso a través del grupo de seguridad "Técnico de Mantenimiento".
Modelos:

Modelo: equipo.py
Campos: name, categoria, fecha_instalacion, ultimo_mantenimiento, estado, responsable_id.
Restricción: No se puede archivar si estado es "en reparación".
Modelo: mantenimiento_preventivo.py
Campos: equipo_id, fecha_programada, fecha_ejecucion, tecnico_id, notas.
Restricción: fecha_programada debe ser >= fecha actual.
Vistas:

Vista Kanban:
Colores: rojo para "en reparación", verde para "activo".
Vista Gráfico:
Gráfico de barras: cantidad de equipos por categoría.
Vista Calendario:
Mantenimientos programados por mes.
Automatización:

Cron Job:
Notifica mantenimientos programados para el día siguiente.
Reportes:

Reporte PDF:
Lista de equipos, último mantenimiento y estado.
Seguridad:

Grupo: "Técnico de Mantenimiento".
Permisos: Ver/editar mantenimientos asignados.
Consideraciones adicionales:

Asegúrate de configurar correctamente las relaciones entre modelos.
Personaliza las vistas y reportes según tus necesidades.
Implementa pruebas unitarias para asegurar la calidad del módulo.
