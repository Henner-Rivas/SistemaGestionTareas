"""
Pruebas unitarias para la clase TaskManager.

Este módulo contiene las pruebas para verificar el correcto funcionamiento
de la clase TaskManager y sus métodos.
"""

import pytest
import os
import tempfile
from datetime import datetime, timedelta
from src.task_manager import TaskManager
from src.task import Task


class TestTaskManager:
    """Pruebas para la clase TaskManager."""
    
    def setup_method(self):
        """Configuración antes de cada prueba."""
        # Crear archivo temporal para las pruebas
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.task_manager = TaskManager(data_file=self.temp_file.name)
    
    def teardown_method(self):
        """Limpieza después de cada prueba."""
        # Eliminar archivo temporal
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_task(self):
        """✅ test_create_task: Verifica la creación de tareas"""
        # Arrange
        name = "Tarea de prueba"
        description = "Descripción de prueba"
        due_date = datetime.now() + timedelta(days=1)
        
        # Act
        task = self.task_manager.create_task(
            name=name,
            description=description,
            due_date=due_date,
            status="pendiente"
        )
        
        # Assert
        assert task.id == 1
        assert task.name == name
        assert task.description == description
        assert task.due_date == due_date
        assert task.status == "pendiente"
        assert len(self.task_manager.list_tasks()) == 1
    
    def test_create_task_with_defaults(self):
        """Verifica la creación de tareas con valores por defecto"""
        # Act
        task = self.task_manager.create_task(name="Tarea básica")
        
        # Assert
        assert task.id == 1
        assert task.name == "Tarea básica"
        assert task.description == ""
        assert task.status == "pendiente"
        assert isinstance(task.due_date, datetime)
    
    def test_create_task_empty_name(self):
        """Verifica que no se pueden crear tareas con nombre vacío"""
        # Act & Assert
        with pytest.raises(ValueError, match="El nombre de la tarea no puede estar vacío"):
            self.task_manager.create_task(name="")
        
        with pytest.raises(ValueError, match="El nombre de la tarea no puede estar vacío"):
            self.task_manager.create_task(name="   ")  # Solo espacios
    
    def test_create_multiple_tasks(self):
        """Verifica la creación de múltiples tareas con IDs secuenciales"""
        # Act
        task1 = self.task_manager.create_task(name="Tarea 1")
        task2 = self.task_manager.create_task(name="Tarea 2")
        task3 = self.task_manager.create_task(name="Tarea 3")
        
        # Assert
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(self.task_manager.list_tasks()) == 3
    
    def test_update_task(self):
        """✅ test_update_task: Verifica la actualización de tareas"""
        # Arrange
        task = self.task_manager.create_task(name="Tarea original")
        original_id = task.id
        new_name = "Tarea actualizada"
        new_description = "Nueva descripción"
        new_status = "en_progreso"
        new_due_date = datetime.now() + timedelta(days=5)
        
        # Act
        success = self.task_manager.update_task(
            task_id=original_id,
            name=new_name,
            description=new_description,
            status=new_status,
            due_date=new_due_date
        )
        
        # Assert
        assert success is True
        updated_task = self.task_manager.get_task_by_id(original_id)
        assert updated_task.name == new_name
        assert updated_task.description == new_description
        assert updated_task.status == new_status
        assert updated_task.due_date == new_due_date
    
    def test_update_nonexistent_task(self):
        """Verifica actualización de tarea inexistente"""
        # Act
        success = self.task_manager.update_task(task_id=999, name="No existe")
        
        # Assert
        assert success is False
    
    def test_delete_task(self):
        """✅ test_delete_task: Verifica la eliminación de tareas"""
        # Arrange
        task1 = self.task_manager.create_task(name="Tarea 1")
        task2 = self.task_manager.create_task(name="Tarea 2")
        task3 = self.task_manager.create_task(name="Tarea 3")
        
        # Act
        success = self.task_manager.delete_task(task2.id)
        
        # Assert
        assert success is True
        remaining_tasks = self.task_manager.list_tasks()
        assert len(remaining_tasks) == 2
        assert task2.id not in [t.id for t in remaining_tasks]
        assert task1.id in [t.id for t in remaining_tasks]
        assert task3.id in [t.id for t in remaining_tasks]
    
    def test_delete_nonexistent_task(self):
        """Verifica eliminación de tarea inexistente"""
        # Act
        success = self.task_manager.delete_task(999)
        
        # Assert
        assert success is False
    
    def test_list_tasks(self):
        """✅ test_list_tasks: Verifica el listado de tareas"""
        # Arrange - Sin tareas iniciales
        assert len(self.task_manager.list_tasks()) == 0
        
        # Act - Crear algunas tareas
        task1 = self.task_manager.create_task(name="Tarea 1")
        task2 = self.task_manager.create_task(name="Tarea 2")
        task3 = self.task_manager.create_task(name="Tarea 3")
        
        # Assert
        tasks = self.task_manager.list_tasks()
        assert len(tasks) == 3
        assert all(isinstance(task, Task) for task in tasks)
        
        # Verificar que es una copia (no la lista original)
        tasks.append("elemento_falso")
        assert len(self.task_manager.list_tasks()) == 3
    
    def test_get_task_by_id(self):
        """Verifica la obtención de tareas por ID"""
        # Arrange
        task1 = self.task_manager.create_task(name="Tarea 1")
        task2 = self.task_manager.create_task(name="Tarea 2")
        
        # Act & Assert
        found_task1 = self.task_manager.get_task_by_id(task1.id)
        found_task2 = self.task_manager.get_task_by_id(task2.id)
        not_found = self.task_manager.get_task_by_id(999)
        
        assert found_task1 == task1
        assert found_task2 == task2
        assert not_found is None
    
    def test_filter_by_status(self):
        """✅ test_filter_by_status: Verifica el filtrado por estado"""
        # Arrange
        task1 = self.task_manager.create_task(name="Tarea 1", status="pendiente")
        task2 = self.task_manager.create_task(name="Tarea 2", status="en_progreso")
        task3 = self.task_manager.create_task(name="Tarea 3", status="completada")
        task4 = self.task_manager.create_task(name="Tarea 4", status="pendiente")
        
        # Act
        pendientes = self.task_manager.filter_tasks(status="pendiente")
        en_progreso = self.task_manager.filter_tasks(status="en_progreso")
        completadas = self.task_manager.filter_tasks(status="completada")
        
        # Assert
        assert len(pendientes) == 2
        assert all(task.status == "pendiente" for task in pendientes)
        assert len(en_progreso) == 1
        assert en_progreso[0] == task2
        assert len(completadas) == 1
        assert completadas[0] == task3
    
    def test_filter_by_date(self):
        """✅ test_filter_by_date: Verifica el filtrado por fecha"""
        # Arrange
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        
        task1 = self.task_manager.create_task(name="Tarea ayer", due_date=yesterday)
        task2 = self.task_manager.create_task(name="Tarea hoy", due_date=today)
        task3 = self.task_manager.create_task(name="Tarea mañana", due_date=tomorrow)
        task4 = self.task_manager.create_task(name="Tarea próxima semana", due_date=next_week)
        
        # Act
        from_today = self.task_manager.filter_tasks(due_date_from=today)
        until_tomorrow = self.task_manager.filter_tasks(due_date_to=tomorrow)
        only_today = self.task_manager.filter_tasks(due_date_from=today, due_date_to=today)
        
        # Assert
        assert len(from_today) == 3  # today, tomorrow, next_week
        assert len(until_tomorrow) == 3  # yesterday, today, tomorrow
        assert len(only_today) == 1  # solo today
        assert only_today[0] == task2
    
    def test_filter_by_name_contains(self):
        """Verifica el filtrado por texto en el nombre"""
        # Arrange
        task1 = self.task_manager.create_task(name="Estudiar Python")
        task2 = self.task_manager.create_task(name="Proyecto de Python")
        task3 = self.task_manager.create_task(name="Tarea de JavaScript")
        task4 = self.task_manager.create_task(name="python avanzado")
        
        # Act
        python_tasks = self.task_manager.filter_tasks(name_contains="python")
        js_tasks = self.task_manager.filter_tasks(name_contains="JavaScript")
        proyecto_tasks = self.task_manager.filter_tasks(name_contains="Proyecto")
        
        # Assert
        assert len(python_tasks) == 3  # Búsqueda insensible a mayúsculas
        assert len(js_tasks) == 1
        assert len(proyecto_tasks) == 1
    
    def test_filter_combined(self):
        """Verifica el filtrado con múltiples criterios"""
        # Arrange
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        task1 = self.task_manager.create_task(
            name="Python pendiente",
            status="pendiente",
            due_date=today
        )
        task2 = self.task_manager.create_task(
            name="Python en progreso",
            status="en_progreso",
            due_date=today
        )
        task3 = self.task_manager.create_task(
            name="Python pendiente mañana",
            status="pendiente",
            due_date=tomorrow
        )
        
        # Act
        filtered = self.task_manager.filter_tasks(
            status="pendiente",
            name_contains="Python",
            due_date_to=today
        )
        
        # Assert
        assert len(filtered) == 1
        assert filtered[0] == task1
    
    def test_get_tasks_by_status(self):
        """Verifica el método get_tasks_by_status"""
        # Arrange
        task1 = self.task_manager.create_task(name="Tarea 1", status="pendiente")
        task2 = self.task_manager.create_task(name="Tarea 2", status="pendiente")
        task3 = self.task_manager.create_task(name="Tarea 3", status="completada")
        
        # Act
        pendientes = self.task_manager.get_tasks_by_status("pendiente")
        completadas = self.task_manager.get_tasks_by_status("completada")
        en_progreso = self.task_manager.get_tasks_by_status("en_progreso")
        
        # Assert
        assert len(pendientes) == 2
        assert len(completadas) == 1
        assert len(en_progreso) == 0
    
    def test_get_overdue_tasks(self):
        """Verifica la obtención de tareas vencidas"""
        # Arrange
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)
        last_week = datetime.now() - timedelta(days=7)
        
        task1 = self.task_manager.create_task(name="Vencida ayer", due_date=yesterday, status="pendiente")
        task2 = self.task_manager.create_task(name="Vencida semana pasada", due_date=last_week, status="en_progreso")
        task3 = self.task_manager.create_task(name="Vencida pero completada", due_date=yesterday, status="completada")
        task4 = self.task_manager.create_task(name="No vencida", due_date=tomorrow, status="pendiente")
        
        # Act
        overdue_tasks = self.task_manager.get_overdue_tasks()
        
        # Assert
        assert len(overdue_tasks) == 2  # task1 y task2 (task3 está completada)
        overdue_ids = [task.id for task in overdue_tasks]
        assert task1.id in overdue_ids
        assert task2.id in overdue_ids
        assert task3.id not in overdue_ids
        assert task4.id not in overdue_ids
    
    def test_get_task_statistics(self):
        """Verifica las estadísticas de tareas"""
        # Arrange
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)
        
        self.task_manager.create_task(name="Pendiente 1", status="pendiente")
        self.task_manager.create_task(name="Pendiente 2", status="pendiente")
        self.task_manager.create_task(name="En progreso 1", status="en_progreso")
        self.task_manager.create_task(name="Completada 1", status="completada")
        self.task_manager.create_task(name="Completada 2", status="completada")
        self.task_manager.create_task(name="Vencida", due_date=yesterday, status="pendiente")
        
        # Act
        stats = self.task_manager.get_task_statistics()
        
        # Assert
        assert stats["total"] == 6
        assert stats["pendiente"] == 3  # Incluye la vencida
        assert stats["en_progreso"] == 1
        assert stats["completada"] == 2
        # Solo la tarea con due_date de ayer y estado pendiente debería contar como vencida
        # Las otras tareas tienen due_date de "ahora" por defecto, así que también pueden estar vencidas
        assert stats["vencidas"] >= 1  # Al menos 1 vencida (la que creamos explícitamente)
    
    def test_save_and_load(self):
        """✅ test_save_and_load: Verifica la persistencia de datos"""
        # Arrange - Crear tareas
        original_task1 = self.task_manager.create_task(
            name="Tarea 1",
            description="Descripción 1",
            status="pendiente"
        )
        original_task2 = self.task_manager.create_task(
            name="Tarea 2",
            description="Descripción 2",
            status="completada"
        )
        
        # Act - Crear nuevo TaskManager con el mismo archivo
        new_task_manager = TaskManager(data_file=self.temp_file.name)
        
        # Assert
        loaded_tasks = new_task_manager.list_tasks()
        assert len(loaded_tasks) == 2
        
        # Verificar que los datos se cargaron correctamente
        loaded_task1 = new_task_manager.get_task_by_id(original_task1.id)
        loaded_task2 = new_task_manager.get_task_by_id(original_task2.id)
        
        assert loaded_task1.name == original_task1.name
        assert loaded_task1.description == original_task1.description
        assert loaded_task1.status == original_task1.status
        
        assert loaded_task2.name == original_task2.name
        assert loaded_task2.description == original_task2.description
        assert loaded_task2.status == original_task2.status
    
    def test_search_tasks(self):
        """Verifica la búsqueda de tareas"""
        # Arrange
        task1 = self.task_manager.create_task(name="Estudiar Python", description="Aprender conceptos básicos")
        task2 = self.task_manager.create_task(name="Proyecto final", description="Desarrollar aplicación en Python")
        task3 = self.task_manager.create_task(name="Tarea de JavaScript", description="Funciones avanzadas")
        
        # Act
        python_search = self.task_manager.search_tasks("Python")
        concepto_search = self.task_manager.search_tasks("conceptos")
        javascript_search = self.task_manager.search_tasks("JavaScript")
        not_found_search = self.task_manager.search_tasks("C++")  # Buscar algo que no existe
        
        # Assert
        assert len(python_search) == 2
        assert len(concepto_search) == 1
        assert len(javascript_search) == 1
        assert len(not_found_search) == 0
    
    def test_clear_all_tasks(self):
        """Verifica la eliminación de todas las tareas"""
        # Arrange
        self.task_manager.create_task(name="Tarea 1")
        self.task_manager.create_task(name="Tarea 2")
        self.task_manager.create_task(name="Tarea 3")
        assert len(self.task_manager.list_tasks()) == 3
        
        # Act
        success = self.task_manager.clear_all_tasks()
        
        # Assert
        assert success is True
        assert len(self.task_manager.list_tasks()) == 0
        assert self.task_manager.next_id == 1
    
    def test_len_method(self):
        """Verifica el método __len__"""
        # Arrange
        assert len(self.task_manager) == 0
        
        # Act
        self.task_manager.create_task(name="Tarea 1")
        self.task_manager.create_task(name="Tarea 2")
        
        # Assert
        assert len(self.task_manager) == 2
    
    def test_str_method(self):
        """Verifica el método __str__"""
        # Arrange
        self.task_manager.create_task(name="Tarea 1", status="pendiente")
        self.task_manager.create_task(name="Tarea 2", status="en_progreso")
        self.task_manager.create_task(name="Tarea 3", status="completada")
        
        # Act
        str_representation = str(self.task_manager)
        
        # Assert
        assert "TaskManager:" in str_representation
        assert "3 tareas" in str_representation
        assert "1 pendientes" in str_representation
        assert "1 en progreso" in str_representation
        assert "1 completadas" in str_representation


if __name__ == "__main__":
    pytest.main([__file__])

import pytest
import os
import tempfile
from src.task_manager import TaskManager
from src.task import Task


