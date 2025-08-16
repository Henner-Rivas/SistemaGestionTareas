"""
Pruebas para TaskManager
"""

import pytest
import os
import tempfile
from src.task_manager import TaskManager
from src.task import TaskStatus, TaskPriority

class TestTaskManager:
    
    @pytest.fixture
    def temp_file(self):
        """Crea un archivo temporal para las pruebas"""
        temp_fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(temp_fd)
        yield temp_path
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    def test_add_task(self, temp_file):
        """Prueba añadir una tarea"""
        manager = TaskManager(temp_file)
        task = manager.add_task("Test Task", "Description", TaskPriority.ALTA)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert len(manager.get_all_tasks()) == 1
    
    def test_get_task(self, temp_file):
        """Prueba obtener una tarea por ID"""
        manager = TaskManager(temp_file)
        task = manager.add_task("Test Task")
        
        retrieved_task = manager.get_task(task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
        
        # Prueba con ID inexistente
        assert manager.get_task(999) is None
    
    def test_delete_task(self, temp_file):
        """Prueba eliminar una tarea"""
        manager = TaskManager(temp_file)
        task = manager.add_task("Test Task")
        
        assert manager.delete_task(task.id) == True
        assert len(manager.get_all_tasks()) == 0
        assert manager.delete_task(999) == False
    
    def test_update_task_status(self, temp_file):
        """Prueba actualizar el estado de una tarea"""
        manager = TaskManager(temp_file)
        task = manager.add_task("Test Task")
        
        assert manager.update_task_status(task.id, TaskStatus.COMPLETADA) == True
        updated_task = manager.get_task(task.id)
        assert updated_task.status == TaskStatus.COMPLETADA
        
        assert manager.update_task_status(999, TaskStatus.COMPLETADA) == False
    
    def test_search_tasks(self, temp_file):
        """Prueba la búsqueda de tareas"""
        manager = TaskManager(temp_file)
        manager.add_task("Python Task", "Learn Python")
        manager.add_task("Java Task", "Learn Java")
        manager.add_task("Web Development", "HTML and CSS")
        
        python_tasks = manager.search_tasks("Python")
        assert len(python_tasks) == 1
        assert python_tasks[0].title == "Python Task"
        
        learn_tasks = manager.search_tasks("Learn")
        assert len(learn_tasks) == 2
    
    def test_get_stats(self, temp_file):
        """Prueba las estadísticas"""
        manager = TaskManager(temp_file)
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")
        
        manager.update_task_status(task1.id, TaskStatus.COMPLETADA)
        manager.update_task_status(task2.id, TaskStatus.EN_PROGRESO)
        
        stats = manager.get_stats()
        assert stats['total'] == 3
        assert stats['completed'] == 1
        assert stats['in_progress'] == 1
        assert stats['pending'] == 1
        assert stats['completion_rate'] == pytest.approx(33.33, rel=1e-2)
    
    def test_save_and_load(self, temp_file):
        """Prueba guardar y cargar tareas"""
        # Crear y guardar tareas
        manager1 = TaskManager(temp_file)
        task = manager1.add_task("Test Task", "Description")
        manager1.update_task_status(task.id, TaskStatus.COMPLETADA)
        
        # Cargar en una nueva instancia
        manager2 = TaskManager(temp_file)
        loaded_tasks = manager2.get_all_tasks()
        
        assert len(loaded_tasks) == 1
        assert loaded_tasks[0].title == "Test Task"
        assert loaded_tasks[0].status == TaskStatus.COMPLETADA
