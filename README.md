# 📋 Sistema de Gestión de Tareas

Un sistema completo de gestión de tareas desarrollado en Python con interfaz de línea de comandos (CLI) interactiva.

## 🎯 Características Principales

- ✅ **Gestión Completa de Tareas**: Crear, actualizar, eliminar y listar tareas
- 🔍 **Búsqueda y Filtrado**: Buscar tareas por texto, estado, fecha y múltiples criterios
- 📊 **Estadísticas**: Ver resúmenes y estadísticas de productividad
- 💾 **Persistencia de Datos**: Almacenamiento automático en formato JSON
- 📅 **Gestión de Fechas**: Control de fechas de vencimiento y tareas vencidas
- 🔄 **Estados de Tareas**: Pendiente, En Progreso, Completada
- 💾 **Exportar/Importar**: Respaldo y migración de datos
- 🖥️ **Interfaz CLI Intuitiva**: Menú interactivo fácil de usar

## 📁 Estructura del Proyecto

```
SistemaGestionTareas/
├── src/
│   ├── __init__.py
│   ├── task.py                 # Clase Task
│   ├── task_manager.py         # Lógica principal
│   ├── cli.py                  # Interfaz de línea de comandos
│   └── utils.py                # Utilidades
├── tests/
│   ├── __init__.py
│   ├── test_task.py           # Pruebas de la clase Task
│   ├── test_task_manager.py   # Pruebas del TaskManager
│   └── test_integration.py    # Pruebas de integración
├──── README.md 
│   
├── requirements.txt
└── main.py                    # Punto de entrada
```

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Verificar Python

```bash
python --version
# o
python3 --version
```

### Paso 2: Clonar o descargar el proyecto

```bash
git clone https://github.com/tu-usuario/SistemaGestionTareas.git
cd SistemaGestionTareas
```

### Paso 3: Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

### Paso 4: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 5: Ejecutar el programa

```bash
python main.py
```

## 🎮 Uso del Sistema

### Menú Principal

Al ejecutar el programa, verás el siguiente menú:

```
🚀 Sistema de Gestión de Tareas
==================================================

📋 MENÚ PRINCIPAL
------------------------------
1. ➕ Crear nueva tarea
2. 📋 Listar todas las tareas
3. 🔍 Buscar tareas
4. ✏️  Actualizar tarea
5. ❌ Eliminar tarea
6. 📊 Ver estadísticas
7. 🔽 Filtrar tareas
8. ⚠️  Ver tareas vencidas
9. 💾 Exportar/Importar
0. 🚪 Salir
```

### Ejemplos de Uso

#### Crear una Nueva Tarea

1. Selecciona opción `1`
2. Ingresa el nombre de la tarea
3. Añade una descripción (opcional)
4. Establece fecha de vencimiento (formato: YYYY-MM-DD)
5. Selecciona el estado inicial

#### Listar Tareas

La opción `2` muestra todas las tareas en formato tabla con:
- ID de la tarea
- Estado con iconos (⏳ Pendiente, 🔄 En Progreso, ✅ Completada)
- Nombre y descripción
- Fecha de vencimiento
- Indicador de prioridad por vencimiento

#### Buscar y Filtrar

- **Búsqueda**: Busca texto en nombres y descripciones
- **Filtros**: Combina múltiples criterios:
  - Por estado
  - Por rango de fechas
  - Por texto en el nombre

#### Estadísticas

Muestra un resumen completo:
- Total de tareas
- Tareas por estado
- Tareas vencidas
- Tasa de finalización

## 🧪 Pruebas

El proyecto incluye una suite completa de pruebas:

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar pruebas específicas

```bash
# Pruebas de la clase Task
pytest tests/test_task.py

# Pruebas del TaskManager
pytest tests/test_task_manager.py

# Pruebas de integración
pytest tests/test_integration.py
```

### Ejecutar con cobertura

```bash
pytest --cov=src tests/
```

## 📊 Documentación del Código

### Clase Task

La clase `Task` representa una tarea individual:

```python
class Task:
    """
    Representa una tarea individual en el sistema.
    
    Attributes:
        id (int): Identificador único
        name (str): Nombre de la tarea
        description (str): Descripción detallada
        due_date (datetime): Fecha de vencimiento
        status (str): Estado (pendiente, en_progreso, completada)
        created_at (datetime): Fecha de creación
    """
```

**Métodos principales:**
- `__init__()`: Constructor de la tarea
- `update()`: Actualiza los atributos
- `to_dict()`: Convierte a diccionario para serialización
- `from_dict()`: Crea tarea desde diccionario

### Clase TaskManager

La clase `TaskManager` gestiona todas las operaciones:

```python
class TaskManager:
    """
    Gestiona todas las operaciones relacionadas con las tareas.
    
    Attributes:
        tasks (list): Lista de todas las tareas
        next_id (int): Próximo ID disponible
        data_file (str): Archivo de persistencia
    """
```

**Métodos principales:**
- `create_task()`: Crea nueva tarea
- `update_task()`: Actualiza tarea existente
- `delete_task()`: Elimina tarea
- `list_tasks()`: Lista todas las tareas
- `filter_tasks()`: Filtra por criterios
- `search_tasks()`: Búsqueda por texto
- `get_task_statistics()`: Obtiene estadísticas
- `save_to_file()` / `load_from_file()`: Persistencia

## 🔧 Configuración

### Archivo de Datos

Por defecto, las tareas se guardan en `tasks.json`. Puedes especificar un archivo diferente:

```python
task_manager = TaskManager(data_file="mi_archivo.json")
```

### Estados Válidos

- `pendiente`: Tarea por iniciar
- `en_progreso`: Tarea en desarrollo
- `completada`: Tarea finalizada

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -am 'Añadir nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

## 📝 Pruebas Realizadas

### ✅ Pruebas Unitarias

**test_task.py:**
- `test_task_creation`: Verifica creación correcta de tareas
- `test_task_update`: Verifica actualización de atributos
- `test_task_to_dict`: Verifica conversión a diccionario
- `test_task_from_dict`: Verifica creación desde diccionario
- `test_invalid_status`: Verifica validación de estados

**test_task_manager.py:**
- `test_create_task`: Verifica creación de tareas
- `test_update_task`: Verifica actualización de tareas
- `test_delete_task`: Verifica eliminación de tareas
- `test_list_tasks`: Verifica listado de tareas
- `test_filter_by_status`: Verifica filtrado por estado
- `test_filter_by_date`: Verifica filtrado por fecha
- `test_save_and_load`: Verifica persistencia de datos

### ✅ Pruebas de Integración

**test_integration.py:**
- `test_complete_workflow`: Prueba flujo completo del sistema
- `test_cli_integration`: Verifica integración con interfaz CLI
- `test_data_persistence`: Verifica persistencia entre sesiones
- `test_error_handling`: Verifica manejo de errores

## 📈 Rendimiento

El sistema está optimizado para:
- Crear hasta 100 tareas en menos de 1 segundo
- Búsquedas instantáneas en conjuntos de datos medianos
- Operaciones de filtrado eficientes
- Carga y guardado rápido de archivos JSON

## 🛠️ Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje principal
- **JSON**: Formato de persistencia
- **pytest**: Framework de pruebas
- **datetime**: Manejo de fechas
- **tabulate**: Formateo de tablas (opcional)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Solución de Problemas

### Error: "Módulo no encontrado"

```bash
# Asegúrate de estar en el directorio correcto
cd SistemaGestionTareas

# Instala las dependencias
pip install -r requirements.txt
```

### Error: "Python no reconocido"

- Verifica que Python esté instalado
- En algunos sistemas, usa `python3` en lugar de `python`

### Error de permisos de archivo

```bash
# En macOS/Linux, otorga permisos de ejecución
chmod +x main.py
```

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema
4. Incluye información del sistema y versión de Python

---

**¡Gracias por usar el Sistema de Gestión de Tareas! 🚀**