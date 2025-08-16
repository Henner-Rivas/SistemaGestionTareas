"""
Clase Task para representar una tarea
"""

from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"

class TaskPriority(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"

class Task:
    """Representa una tarea en el sistema de gestión"""
    
    def __init__(self, 
                 title: str, 
                 description: str = "", 
                 priority: TaskPriority = TaskPriority.MEDIA,
                 due_date: Optional[datetime] = None):
        self.id = None  # Se asignará por el TaskManager
        self.title = title
        self.description = description
        self.priority = priority
        self.status = TaskStatus.PENDIENTE
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.due_date = due_date
        self.completed_at = None
    
    def mark_completed(self):
        """Marca la tarea como completada"""
        self.status = TaskStatus.COMPLETADA
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def mark_in_progress(self):
        """Marca la tarea como en progreso"""
        self.status = TaskStatus.EN_PROGRESO
        self.updated_at = datetime.now()
    
    def update_priority(self, priority: TaskPriority):
        """Actualiza la prioridad de la tarea"""
        self.priority = priority
        self.updated_at = datetime.now()
    
    def update_description(self, description: str):
        """Actualiza la descripción de la tarea"""
        self.description = description
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convierte la tarea a diccionario para serialización"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una tarea desde un diccionario"""
        task = cls(
            title=data['title'],
            description=data['description'],
            priority=TaskPriority(data['priority'])
        )
        task.id = data['id']
        task.status = TaskStatus(data['status'])
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.updated_at = datetime.fromisoformat(data['updated_at'])
        if data['due_date']:
            task.due_date = datetime.fromisoformat(data['due_date'])
        if data['completed_at']:
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        return task
    
    def __str__(self):
        status_emoji = {
            TaskStatus.PENDIENTE: "⏳",
            TaskStatus.EN_PROGRESO: "🔄",
            TaskStatus.COMPLETADA: "✅"
        }
        priority_emoji = {
            TaskPriority.BAJA: "🟢",
            TaskPriority.MEDIA: "🟡",
            TaskPriority.ALTA: "🔴"
        }
        
        return f"{status_emoji[self.status]} {priority_emoji[self.priority]} [{self.id}] {self.title}"
