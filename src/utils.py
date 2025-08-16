"""
Utilidades para el sistema de gestión de tareas
"""

from datetime import datetime
from typing import List
from .task import Task, TaskStatus, TaskPriority

def format_datetime(dt: datetime) -> str:
    """Formatea una fecha y hora para mostrar"""
    if dt is None:
        return "N/A"
    return dt.strftime("%d/%m/%Y %H:%M")

def format_date(dt: datetime) -> str:
    """Formatea solo la fecha"""
    if dt is None:
        return "N/A"
    return dt.strftime("%d/%m/%Y")

def get_status_color(status: TaskStatus) -> str:
    """Obtiene el color para el estado de la tarea"""
    colors = {
        TaskStatus.PENDIENTE: "yellow",
        TaskStatus.EN_PROGRESO: "blue", 
        TaskStatus.COMPLETADA: "green"
    }
    return colors.get(status, "white")

def get_priority_color(priority: TaskPriority) -> str:
    """Obtiene el color para la prioridad de la tarea"""
    colors = {
        TaskPriority.BAJA: "green",
        TaskPriority.MEDIA: "yellow",
        TaskPriority.ALTA: "red"
    }
    return colors.get(priority, "white")

def sort_tasks_by_priority(tasks: List[Task]) -> List[Task]:
    """Ordena las tareas por prioridad (alta -> media -> baja)"""
    priority_order = {
        TaskPriority.ALTA: 3,
        TaskPriority.MEDIA: 2,
        TaskPriority.BAJA: 1
    }
    return sorted(tasks, key=lambda t: priority_order[t.priority], reverse=True)

def sort_tasks_by_date(tasks: List[Task], by_created: bool = True) -> List[Task]:
    """Ordena las tareas por fecha de creación o actualización"""
    if by_created:
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    else:
        return sorted(tasks, key=lambda t: t.updated_at, reverse=True)

def filter_tasks_by_keyword(tasks: List[Task], keyword: str) -> List[Task]:
    """Filtra tareas que contengan una palabra clave"""
    keyword = keyword.lower()
    return [task for task in tasks 
            if keyword in task.title.lower() or keyword in task.description.lower()]

def get_task_summary(task: Task) -> str:
    """Obtiene un resumen corto de la tarea"""
    status_symbols = {
        TaskStatus.PENDIENTE: "⏳",
        TaskStatus.EN_PROGRESO: "🔄", 
        TaskStatus.COMPLETADA: "✅"
    }
    
    priority_symbols = {
        TaskPriority.BAJA: "🟢",
        TaskPriority.MEDIA: "🟡",
        TaskPriority.ALTA: "🔴"
    }
    
    return f"{status_symbols[task.status]} {priority_symbols[task.priority]} [{task.id}] {task.title}"
