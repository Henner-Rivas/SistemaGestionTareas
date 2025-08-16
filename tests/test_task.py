"""
Pruebas unitarias para la clase Task.

Este módulo contiene las pruebas para verificar el correcto funcionamiento
de la clase Task y sus métodos.
"""

import pytest
from datetime import datetime, timedelta
from src.task import Task


class TestTask:
    """Pruebas para la clase Task."""
    
    def test_task_creation(self):
        """✅ test_task_creation: Verifica la creación correcta de tareas"""
        # Arrange
        task_id = 1
        name = "Tarea de prueba"
        description = "Descripción de prueba"
        due_date = datetime.now() + timedelta(days=1)
        status = "pendiente"
        
        # Act
        task = Task(
            id=task_id,
            name=name,
            description=description,
            due_date=due_date,
            status=status
        )
        
        # Assert
        assert task.id == task_id
        assert task.name == name
        assert task.description == description
        assert task.due_date == due_date
        assert task.status == status
        assert isinstance(task.created_at, datetime)
    
    def test_task_creation_with_defaults(self):
        """Verifica la creación de tareas con valores por defecto"""
        # Arrange & Act
        task = Task(id=1, name="Tarea básica")
        
        # Assert
        assert task.id == 1
        assert task.name == "Tarea básica"
        assert task.description == ""
        assert task.status == "pendiente"
        assert isinstance(task.due_date, datetime)
        assert isinstance(task.created_at, datetime)
    
    def test_task_update(self):
        """✅ test_task_update: Verifica la actualización de atributos"""
        # Arrange
        task = Task(id=1, name="Tarea original", description="Descripción original")
        new_name = "Tarea actualizada"
        new_description = "Nueva descripción"
        new_status = "en_progreso"
        new_due_date = datetime.now() + timedelta(days=2)
        
        # Act
        task.update(
            name=new_name,
            description=new_description,
            status=new_status,
            due_date=new_due_date
        )
        
        # Assert
        assert task.name == new_name
        assert task.description == new_description
        assert task.status == new_status
        assert task.due_date == new_due_date
    
    def test_task_update_partial(self):
        """Verifica la actualización parcial de atributos"""
        # Arrange
        original_name = "Tarea original"
        original_description = "Descripción original"
        task = Task(id=1, name=original_name, description=original_description)
        
        # Act - Solo actualizar el estado
        task.update(status="completada")
        
        # Assert
        assert task.name == original_name  # No cambia
        assert task.description == original_description  # No cambia
        assert task.status == "completada"  # Cambia
    
    def test_task_to_dict(self):
        """✅ test_task_to_dict: Verifica la conversión a diccionario"""
        # Arrange
        due_date = datetime(2024, 12, 25, 10, 30)
        created_at = datetime(2024, 12, 20, 9, 0)
        task = Task(
            id=1,
            name="Tarea de prueba",
            description="Descripción",
            due_date=due_date,
            status="pendiente"
        )
        task.created_at = created_at  # Simular fecha de creación específica
        
        # Act
        task_dict = task.to_dict()
        
        # Assert
        expected_dict = {
            "id": 1,
            "name": "Tarea de prueba",
            "description": "Descripción",
            "due_date": due_date.isoformat(),
            "status": "pendiente",
            "created_at": created_at.isoformat()
        }
        assert task_dict == expected_dict
    
    def test_task_from_dict(self):
        """✅ test_task_from_dict: Verifica la creación desde diccionario"""
        # Arrange
        task_data = {
            "id": 2,
            "name": "Tarea desde dict",
            "description": "Descripción desde dict",
            "due_date": "2024-12-25T10:30:00",
            "status": "en_progreso",
            "created_at": "2024-12-20T09:00:00"
        }
        
        # Act
        task = Task.from_dict(task_data)
        
        # Assert
        assert task.id == 2
        assert task.name == "Tarea desde dict"
        assert task.description == "Descripción desde dict"
        assert task.status == "en_progreso"
        assert task.due_date == datetime.fromisoformat("2024-12-25T10:30:00")
        assert task.created_at == datetime.fromisoformat("2024-12-20T09:00:00")
    
    def test_invalid_status(self):
        """✅ test_invalid_status: Verifica validación de estados"""
        # Test 1: Estado inválido en creación
        with pytest.raises(ValueError, match="Estado inválido"):
            Task(id=1, name="Tarea", status="estado_invalido")
        
        # Test 2: Estado inválido en actualización
        task = Task(id=1, name="Tarea")
        with pytest.raises(ValueError, match="Estado inválido"):
            task.update(status="estado_invalido")
    
    def test_valid_statuses(self):
        """Verifica que todos los estados válidos funcionan"""
        valid_statuses = ["pendiente", "en_progreso", "completada"]
        
        for status in valid_statuses:
            # Crear tarea con estado válido
            task = Task(id=1, name="Tarea", status=status)
            assert task.status == status
            
            # Actualizar a estado válido
            task.update(status=status)
            assert task.status == status
    
    def test_task_str_representation(self):
        """Verifica la representación en cadena de la tarea"""
        # Arrange
        due_date = datetime(2024, 12, 25)
        task = Task(id=1, name="Mi Tarea", status="pendiente", due_date=due_date)
        
        # Act
        str_representation = str(task)
        
        # Assert
        expected = "Tarea #1: Mi Tarea [PENDIENTE] - Vence: 2024-12-25"
        assert str_representation == expected
    
    def test_task_repr_representation(self):
        """Verifica la representación técnica de la tarea"""
        # Arrange
        due_date = datetime(2024, 12, 25)
        task = Task(id=1, name="Mi Tarea", status="pendiente", due_date=due_date)
        
        # Act
        repr_representation = repr(task)
        
        # Assert
        expected = f"Task(id=1, name='Mi Tarea', status='pendiente', due_date={due_date})"
        assert repr_representation == expected
    
    def test_task_with_empty_description(self):
        """Verifica manejo de descripción vacía"""
        # Test con descripción vacía explícita
        task1 = Task(id=1, name="Tarea", description="")
        assert task1.description == ""
        
        # Test con descripción None (valor por defecto)
        task2 = Task(id=2, name="Tarea")
        assert task2.description == ""
    
    def test_task_date_handling(self):
        """Verifica el manejo correcto de fechas"""
        # Test con fecha específica
        specific_date = datetime(2024, 12, 25, 15, 30)
        task = Task(id=1, name="Tarea", due_date=specific_date)
        assert task.due_date == specific_date
        
        # Test con fecha None (debe usar fecha actual)
        task2 = Task(id=2, name="Tarea", due_date=None)
        assert isinstance(task2.due_date, datetime)
        # Verificar que la fecha es reciente (dentro de 1 minuto)
        time_diff = abs((datetime.now() - task2.due_date).total_seconds())
        assert time_diff < 60


if __name__ == "__main__":
    pytest.main([__file__])

