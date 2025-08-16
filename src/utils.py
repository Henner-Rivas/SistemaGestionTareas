"""
Módulo de utilidades para el Sistema de Gestión de Tareas.

Este módulo contiene funciones de ayuda para formatear fechas,
validar datos, y mostrar información de manera ordenada.
"""

from datetime import datetime
from typing import List, Optional


def format_date(date: datetime) -> str:
    """
    Formatea una fecha para mostrar de manera legible.
    
    Args:
        date (datetime): Fecha a formatear
        
    Returns:
        str: Fecha formateada como YYYY-MM-DD
    """
    return date.strftime("%Y-%m-%d")


def format_datetime(date: datetime) -> str:
    """
    Formatea una fecha y hora para mostrar de manera legible.
    
    Args:
        date (datetime): Fecha y hora a formatear
        
    Returns:
        str: Fecha y hora formateada como YYYY-MM-DD HH:MM
    """
    return date.strftime("%Y-%m-%d %H:%M")


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Convierte una cadena de fecha en objeto datetime.
    
    Args:
        date_str (str): Cadena de fecha en formato YYYY-MM-DD
        
    Returns:
        Optional[datetime]: Objeto datetime si es válido, None en caso contrario
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        try:
            # Intentar formato con hora
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None


def validate_status(status: str) -> bool:
    """
    Valida que el estado de la tarea sea válido.
    
    Args:
        status (str): Estado a validar
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    valid_statuses = ["pendiente", "en_progreso", "completada"]
    return status.lower() in valid_statuses


def get_status_icon(status: str) -> str:
    """
    Obtiene el icono correspondiente al estado de la tarea.
    
    Args:
        status (str): Estado de la tarea
        
    Returns:
        str: Icono correspondiente al estado
    """
    icons = {
        "pendiente": "⏳",
        "en_progreso": "🔄",
        "completada": "✅"
    }
    return icons.get(status.lower(), "❓")


def get_priority_color(days_until_due: int) -> str:
    """
    Obtiene el color de prioridad basado en los días hasta vencimiento.
    
    Args:
        days_until_due (int): Días hasta el vencimiento
        
    Returns:
        str: Indicador de prioridad
    """
    if days_until_due < 0:
        return "🔴"  # Vencida
    elif days_until_due <= 1:
        return "🟠"  # Urgente
    elif days_until_due <= 3:
        return "🟡"  # Próxima
    else:
        return "🟢"  # Normal


def display_tasks_table(tasks: List) -> None:
    """
    Muestra las tareas en formato de tabla simple.
    
    Args:
        tasks (List[Task]): Lista de tareas a mostrar
    """
    if not tasks:
        print("📝 No hay tareas para mostrar.")
        return
    
    print(f"\n{'ID':<4} {'Estado':<12} {'Nombre':<25} {'Descripción':<30} {'Vencimiento':<15}")
    print("-" * 90)
    
    now = datetime.now()
    
    for task in tasks:
        # Calcular días hasta vencimiento
        days_until = (task.due_date - now).days
        priority_icon = get_priority_color(days_until)
        
        # Truncar descripción si es muy larga
        description = task.description
        if len(description) > 27:
            description = description[:27] + "..."
        
        # Truncar nombre si es muy largo
        name = task.name
        if len(name) > 22:
            name = name[:22] + "..."
        
        status_display = f"{get_status_icon(task.status)} {task.status}"
        
        print(f"{task.id:<4} {status_display:<12} {name:<25} {description:<30} {format_date(task.due_date):<15} {priority_icon}")


def display_task_details(task) -> None:
    """
    Muestra los detalles completos de una tarea.
    
    Args:
        task (Task): Tarea a mostrar
    """
    print(f"\n📋 DETALLES DE LA TAREA #{task.id}")
    print("=" * 40)
    print(f"Nombre: {task.name}")
    print(f"Descripción: {task.description}")
    print(f"Estado: {get_status_icon(task.status)} {task.status}")
    print(f"Fecha de vencimiento: {format_date(task.due_date)}")
    print(f"Fecha de creación: {format_datetime(task.created_at)}")
    
    # Calcular días hasta vencimiento
    now = datetime.now()
    days_until = (task.due_date - now).days
    
    if days_until < 0:
        print(f"⚠️  VENCIDA hace {abs(days_until)} día(s)")
    elif days_until == 0:
        print("⚠️  VENCE HOY")
    elif days_until == 1:
        print("🟠 Vence mañana")
    else:
        print(f"📅 Vence en {days_until} día(s)")


def validate_task_input(name: str, description: str = "") -> bool:
    """
    Valida los datos de entrada para una tarea.
    
    Args:
        name (str): Nombre de la tarea
        description (str): Descripción de la tarea
        
    Returns:
        bool: True si los datos son válidos
    """
    if not name or not name.strip():
        print("❌ El nombre de la tarea no puede estar vacío.")
        return False
    
    if len(name.strip()) > 100:
        print("❌ El nombre de la tarea no puede tener más de 100 caracteres.")
        return False
    
    if len(description) > 500:
        print("❌ La descripción no puede tener más de 500 caracteres.")
        return False
    
    return True


def confirm_action(message: str) -> bool:
    """
    Solicita confirmación del usuario para una acción.
    
    Args:
        message (str): Mensaje a mostrar
        
    Returns:
        bool: True si el usuario confirma, False en caso contrario
    """
    response = input(f"{message} (s/N): ").strip().lower()
    return response == 's' or response == 'si'


def print_header(title: str) -> None:
    """
    Imprime un encabezado formateado.
    
    Args:
        title (str): Título del encabezado
    """
    print(f"\n{title}")
    print("=" * len(title))


def print_section(title: str) -> None:
    """
    Imprime un título de sección formateado.
    
    Args:
        title (str): Título de la sección
    """
    print(f"\n{title}")
    print("-" * len(title))
