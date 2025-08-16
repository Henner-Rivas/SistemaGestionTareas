"""
Pruebas para la clase Task
"""

import pytest
from datetime import datetime
from src.task import Task, TaskStatus, TaskPriority

class TestTask:
    
    def test_task_creation(self):
        """Prueba la creación de una tarea"""
        task = Task("Test Task", "Test Description", TaskPriority.ALTA)
        
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == TaskPriority.ALTA
        assert task.status == TaskStatus.PENDIENTE
        assert task.id is None
        assert isinstance(task.created_at, datetime)
        assert task.completed_at is None
    
    def test_mark_completed(self):
        """Prueba marcar una tarea como completada"""
        task = Task("Test Task")
        task.mark_completed()
        
        assert task.status == TaskStatus.COMPLETADA
        assert task.completed_at is not None
        assert isinstance(task.completed_at, datetime)
    
    def test_mark_in_progress(self):
        """Prueba marcar una tarea como en progreso"""
        task = Task("Test Task")
        task.mark_in_progress()
        
        assert task.status == TaskStatus.EN_PROGRESO
    
    def test_update_priority(self):
        """Prueba actualizar la prioridad de una tarea"""
        task = Task("Test Task", priority=TaskPriority.BAJA)
        task.update_priority(TaskPriority.ALTA)
        
        assert task.priority == TaskPriority.ALTA
    
    def test_to_dict(self):
        """Prueba la conversión a diccionario"""
        task = Task("Test Task", "Description", TaskPriority.MEDIA)
        task.id = 1
        
        data = task.to_dict()
        
        assert data['id'] == 1
        assert data['title'] == "Test Task"
        assert data['description'] == "Description"
        assert data['priority'] == "media"
        assert data['status'] == "pendiente"
    
    def test_from_dict(self):
        """Prueba la creación desde diccionario"""
        data = {
            'id': 1,
            'title': "Test Task",
            'description': "Description",
            'priority': "alta",
            'status': "completada",
            'created_at': "2023-01-01T10:00:00",
            'updated_at': "2023-01-01T11:00:00",
            'due_date': None,
            'completed_at': "2023-01-01T12:00:00"
        }
        
        task = Task.from_dict(data)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.priority == TaskPriority.ALTA
        assert task.status == TaskStatus.COMPLETADA
