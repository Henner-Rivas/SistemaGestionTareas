"""
TaskManager - Lógica principal para gestionar tareas
"""

import json
import os
from datetime import datetime
from typing import List, Optional
from .task import Task, TaskStatus, TaskPriority

class TaskManager:
    """Gestor principal de tareas"""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Carga las tareas desde el archivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error al cargar tareas: {e}")
                self.tasks = []
                self.next_id = 1
    
    def save_tasks(self):
        """Guarda las tareas en el archivo JSON"""
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'next_id': self.next_id
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar tareas: {e}")
    
    def add_task(self, title: str, description: str = "", 
                 priority: TaskPriority = TaskPriority.MEDIA) -> Task:
        """Añade una nueva tarea"""
        task = Task(title, description, priority)
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por su ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Obtiene todas las tareas"""
        return self.tasks.copy()
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Obtiene tareas filtradas por estado"""
        return [task for task in self.tasks if task.status == status]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Obtiene tareas filtradas por prioridad"""
        return [task for task in self.tasks if task.priority == priority]
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> bool:
        """Actualiza el estado de una tarea"""
        task = self.get_task(task_id)
        if task:
            if status == TaskStatus.COMPLETADA:
                task.mark_completed()
            elif status == TaskStatus.EN_PROGRESO:
                task.mark_in_progress()
            else:
                task.status = status
                task.updated_at = datetime.now()
            self.save_tasks()
            return True
        return False
    
    def update_task_priority(self, task_id: int, priority: TaskPriority) -> bool:
        """Actualiza la prioridad de una tarea"""
        task = self.get_task(task_id)
        if task:
            task.update_priority(priority)
            self.save_tasks()
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Elimina una tarea"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
    
    def search_tasks(self, query: str) -> List[Task]:
        """Busca tareas por título o descripción"""
        query = query.lower()
        return [task for task in self.tasks 
                if query in task.title.lower() or query in task.description.lower()]
    
    def get_stats(self) -> dict:
        """Obtiene estadísticas de las tareas"""
        total = len(self.tasks)
        completed = len(self.get_tasks_by_status(TaskStatus.COMPLETADA))
        in_progress = len(self.get_tasks_by_status(TaskStatus.EN_PROGRESO))
        pending = len(self.get_tasks_by_status(TaskStatus.PENDIENTE))
        
        return {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
