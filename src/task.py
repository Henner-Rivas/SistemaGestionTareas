"""
Módulo que define la clase Task para el Sistema de Gestión de Tareas.

Esta clase representa una tarea individual con sus atributos y métodos
para manipular la información de la tarea.
"""

from datetime import datetime
from typing import Dict, Any


class Task:
    """
    Representa una tarea individual en el sistema.
    
    Attributes:
        id (int): Identificador único de la tarea
        name (str): Nombre de la tarea
        description (str): Descripción detallada
        due_date (datetime): Fecha de vencimiento
        status (str): Estado actual (pendiente, en_progreso, completada)
        created_at (datetime): Fecha de creación
    """
    
    VALID_STATUSES = ["pendiente", "en_progreso", "completada"]
    
    def __init__(self, id: int, name: str, description: str = "", 
                 due_date: datetime = None, status: str = "pendiente"):
        """
        Inicializa una nueva tarea.
        
        Args:
            id (int): Identificador único de la tarea
            name (str): Nombre de la tarea
            description (str): Descripción de la tarea
            due_date (datetime): Fecha de vencimiento
            status (str): Estado inicial de la tarea
            
        Raises:
            ValueError: Si el estado no es válido
        """
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Estado inválido. Estados válidos: {self.VALID_STATUSES}")
        
        self.id = id
        self.name = name
        self.description = description
        self.due_date = due_date or datetime.now()
        self.status = status
        self.created_at = datetime.now()
    
    def update(self, name: str = None, description: str = None, 
               due_date: datetime = None, status: str = None) -> None:
        """
        Actualiza los atributos de la tarea.
        
        Args:
            name (str): Nuevo nombre de la tarea
            description (str): Nueva descripción
            due_date (datetime): Nueva fecha de vencimiento
            status (str): Nuevo estado de la tarea
            
        Raises:
            ValueError: Si el estado no es válido
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        if status is not None:
            if status not in self.VALID_STATUSES:
                raise ValueError(f"Estado inválido. Estados válidos: {self.VALID_STATUSES}")
            self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la tarea a un diccionario para serialización.
        
        Returns:
            Dict[str, Any]: Diccionario con los datos de la tarea
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Crea una tarea desde un diccionario.
        
        Args:
            data (Dict[str, Any]): Diccionario con los datos de la tarea
            
        Returns:
            Task: Nueva instancia de Task
        """
        task = cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            due_date=datetime.fromisoformat(data["due_date"]),
            status=data["status"]
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        return task
    
    def __str__(self) -> str:
        """
        Representación en cadena de la tarea.
        
        Returns:
            str: Descripción legible de la tarea
        """
        return (f"Tarea #{self.id}: {self.name} "
                f"[{self.status.upper()}] - Vence: {self.due_date.strftime('%Y-%m-%d')}")
    
    def __repr__(self) -> str:
        """
        Representación técnica de la tarea.
        
        Returns:
            str: Representación técnica del objeto
        """
        return (f"Task(id={self.id}, name='{self.name}', "
                f"status='{self.status}', due_date={self.due_date})")