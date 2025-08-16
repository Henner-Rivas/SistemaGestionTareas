"""
Módulo que define la clase TaskManager para el Sistema de Gestión de Tareas.

Esta clase gestiona todas las operaciones relacionadas con las tareas,
incluyendo creación, actualización, eliminación, filtrado y persistencia.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .task import Task


class TaskManager:
    """
    Gestiona todas las operaciones relacionadas con las tareas.
    
    Attributes:
        tasks (list): Lista de todas las tareas
        next_id (int): Próximo ID disponible
        data_file (str): Archivo donde se guardan las tareas
    """
    
    def __init__(self, data_file: str = "tasks.json"):
        """
        Inicializa el gestor de tareas.
        
        Args:
            data_file (str): Nombre del archivo de datos
        """
        self.tasks: List[Task] = []
        self.next_id = 1
        self.data_file = data_file
        self.load_from_file()
    
    
    def create_task(self, name: str, description: str = "", 
                   due_date: datetime = None, status: str = "pendiente") -> Task:
        """
        Crea una nueva tarea.
        
        Args:
            name (str): Nombre de la tarea
            description (str): Descripción de la tarea
            due_date (datetime): Fecha de vencimiento
            status (str): Estado inicial de la tarea
            
        Returns:
            Task: La tarea creada
            
        Raises:
            ValueError: Si el nombre está vacío
        """
        if not name.strip():
            raise ValueError("El nombre de la tarea no puede estar vacío")
        
        task = Task(
            id=self.next_id,
            name=name.strip(),
            description=description.strip(),
            due_date=due_date or datetime.now(),
            status=status
        )
        
        self.tasks.append(task)
        self.next_id += 1
        self.save_to_file()
        
        return task
    
    def update_task(self, task_id: int, name: str = None, description: str = None,
                   due_date: datetime = None, status: str = None) -> bool:
        """
        Actualiza una tarea existente.
        
        Args:
            task_id (int): ID de la tarea a actualizar
            name (str): Nuevo nombre
            description (str): Nueva descripción
            due_date (datetime): Nueva fecha de vencimiento
            status (str): Nuevo estado
            
        Returns:
            bool: True si se actualizó correctamente, False si no se encontró
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.update(name=name, description=description, 
                       due_date=due_date, status=status)
            self.save_to_file()
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """
        Elimina una tarea.
        
        Args:
            task_id (int): ID de la tarea a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_to_file()
            return True
        return False
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id (int): ID de la tarea
            
        Returns:
            Optional[Task]: La tarea si existe, None en caso contrario
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def list_tasks(self) -> List[Task]:
        """
        Lista todas las tareas.
        
        Returns:
            List[Task]: Lista de todas las tareas
        """
        return self.tasks.copy()
    
    def filter_tasks(self, status: str = None, due_date_from: datetime = None,
                    due_date_to: datetime = None, name_contains: str = None) -> List[Task]:
        """
        Filtra tareas por criterios específicos.
        
        Args:
            status (str): Filtrar por estado
            due_date_from (datetime): Fecha de vencimiento desde
            due_date_to (datetime): Fecha de vencimiento hasta
            name_contains (str): Texto que debe contener el nombre
            
        Returns:
            List[Task]: Lista de tareas filtradas
        """
        filtered_tasks = self.tasks.copy()
        
        if status:
            filtered_tasks = [task for task in filtered_tasks if task.status == status]
        
        if due_date_from:
            filtered_tasks = [task for task in filtered_tasks 
                            if task.due_date >= due_date_from]
        
        if due_date_to:
            filtered_tasks = [task for task in filtered_tasks 
                            if task.due_date <= due_date_to]
        
        if name_contains:
            filtered_tasks = [task for task in filtered_tasks 
                            if name_contains.lower() in task.name.lower()]
        
        return filtered_tasks
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Obtiene todas las tareas con un estado específico.
        
        Args:
            status (str): Estado de las tareas a buscar
            
        Returns:
            List[Task]: Lista de tareas con el estado especificado
        """
        return self.filter_tasks(status=status)
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        Obtiene todas las tareas vencidas.
        
        Returns:
            List[Task]: Lista de tareas vencidas
        """
        now = datetime.now()
        return [task for task in self.tasks 
                if task.due_date < now and task.status != "completada"]
    
    def get_task_statistics(self) -> Dict[str, int]:
        """
        Obtiene estadísticas de las tareas.
        
        Returns:
            Dict[str, int]: Diccionario con estadísticas
        """
        stats = {
            "total": len(self.tasks),
            "pendiente": 0,
            "en_progreso": 0,
            "completada": 0,
            "vencidas": len(self.get_overdue_tasks())
        }
        
        for task in self.tasks:
            stats[task.status] += 1
        
        return stats
    
    def save_to_file(self, filename: str = None) -> bool:
        """
        Guarda las tareas en un archivo JSON.
        
        Args:
            filename (str): Nombre del archivo (opcional)
            
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            file_to_use = filename or self.data_file
            data = {
                "next_id": self.next_id,
                "tasks": [task.to_dict() for task in self.tasks]
            }
            
            with open(file_to_use, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return False
    
    def load_from_file(self, filename: str = None) -> bool:
        """
        Carga las tareas desde un archivo JSON.
        
        Args:
            filename (str): Nombre del archivo (opcional)
            
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            file_to_use = filename or self.data_file
            
            if not os.path.exists(file_to_use):
                return True  # Archivo no existe, no es error
            
            with open(file_to_use, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.next_id = data.get("next_id", 1)
            self.tasks = []
            
            for task_data in data.get("tasks", []):
                task = Task.from_dict(task_data)
                self.tasks.append(task)
                # Actualizar next_id si es necesario
                if task.id >= self.next_id:
                    self.next_id = task.id + 1
            
            return True
        except Exception as e:
            print(f"Error al cargar archivo: {e}")
            return False
    
    def clear_all_tasks(self) -> bool:
        """
        Elimina todas las tareas.
        
        Returns:
            bool: True si se eliminaron correctamente
        """
        self.tasks.clear()
        self.next_id = 1
        self.save_to_file()
        return True
    
    def search_tasks(self, query: str) -> List[Task]:
        """
        Busca tareas por nombre o descripción.
        
        Args:
            query (str): Texto a buscar
            
        Returns:
            List[Task]: Lista de tareas que coinciden con la búsqueda
        """
        query = query.lower()
        return [task for task in self.tasks 
                if query in task.name.lower() or query in task.description.lower()]
    
    def __len__(self) -> int:
        """
        Devuelve el número total de tareas.
        
        Returns:
            int: Número de tareas
        """
        return len(self.tasks)
    
    def __str__(self) -> str:
        """
        Representación en cadena del gestor de tareas.
        
        Returns:
            str: Descripción del gestor
        """
        stats = self.get_task_statistics()
        return (f"TaskManager: {stats['total']} tareas "
                f"({stats['pendiente']} pendientes, "
                f"{stats['en_progreso']} en progreso, "
                f"{stats['completada']} completadas)")