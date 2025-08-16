"""
Pruebas de integración para el Sistema de Gestión de Tareas.

Este módulo contiene las pruebas que verifican la integración completa
entre todos los componentes del sistema.
"""

import pytest
import os
import tempfile
import json
from datetime import datetime, timedelta
import sys
from io import StringIO
from unittest.mock import patch

from src.task_manager import TaskManager
from src.task import Task
from src.cli import TaskCLI


class TestIntegration:
    """Pruebas de integración del sistema completo."""
    
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
    
    def test_complete_workflow(self):
        """✅ test_complete_workflow: Prueba el flujo completo del sistema"""
        # 1. Crear múltiples tareas
        task1 = self.task_manager.create_task(
            name="Estudiar Python",
            description="Aprender conceptos básicos de programación",
            status="pendiente"
        )
        
        task2 = self.task_manager.create_task(
            name="Proyecto final",
            description="Desarrollar aplicación web",
            due_date=datetime.now() + timedelta(days=7),
            status="pendiente"
        )
        
        task3 = self.task_manager.create_task(
            name="Documentación",
            description="Escribir documentación del proyecto",
            due_date=datetime.now() + timedelta(days=3),
            status="pendiente"
        )
        
        # 2. Verificar creación
        assert len(self.task_manager.list_tasks()) == 3
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        
        # 3. Actualizar estados progresivamente
        # Iniciar trabajo en proyecto
        success = self.task_manager.update_task(
            task_id=task2.id,
            status="en_progreso"
        )
        assert success is True
        
        # Completar estudio de Python
        success = self.task_manager.update_task(
            task_id=task1.id,
            status="completada"
        )
        assert success is True
        
        # 4. Verificar filtros y búsquedas
        # Buscar tareas pendientes
        pendientes = self.task_manager.get_tasks_by_status("pendiente")
        assert len(pendientes) == 1
        assert pendientes[0].id == task3.id
        
        # Buscar tareas en progreso
        en_progreso = self.task_manager.get_tasks_by_status("en_progreso")
        assert len(en_progreso) == 1
        assert en_progreso[0].id == task2.id
        
        # Buscar tareas completadas
        completadas = self.task_manager.get_tasks_by_status("completada")
        assert len(completadas) == 1
        assert completadas[0].id == task1.id
        
        # 5. Búsqueda por texto
        python_tasks = self.task_manager.search_tasks("Python")
        assert len(python_tasks) == 1
        assert python_tasks[0].id == task1.id
        
        proyecto_tasks = self.task_manager.search_tasks("proyecto")
        assert len(proyecto_tasks) == 2  # "Proyecto final" y "proyecto" en descripción
        
        # 6. Verificar estadísticas
        stats = self.task_manager.get_task_statistics()
        assert stats["total"] == 3
        assert stats["pendiente"] == 1
        assert stats["en_progreso"] == 1
        assert stats["completada"] == 1
        assert stats["vencidas"] == 0
        
        # 7. Actualizar tarea con nueva información
        success = self.task_manager.update_task(
            task_id=task3.id,
            name="Documentación completa",
            description="Escribir documentación completa del proyecto con ejemplos",
            status="en_progreso"
        )
        assert success is True
        
        updated_task = self.task_manager.get_task_by_id(task3.id)
        assert updated_task.name == "Documentación completa"
        assert updated_task.description == "Escribir documentación completa del proyecto con ejemplos"
        assert updated_task.status == "en_progreso"
        
        # 8. Eliminar una tarea
        success = self.task_manager.delete_task(task1.id)
        assert success is True
        assert len(self.task_manager.list_tasks()) == 2
        
        # 9. Verificar persistencia final
        final_tasks = self.task_manager.list_tasks()
        assert len(final_tasks) == 2
        assert all(task.id != task1.id for task in final_tasks)
    
    def test_data_persistence(self):
        """✅ test_data_persistence: Verifica la persistencia entre sesiones"""
        # Sesión 1: Crear y modificar tareas
        session1_manager = TaskManager(data_file=self.temp_file.name)
        
        # Crear tareas con datos complejos
        task1 = session1_manager.create_task(
            name="Tarea persistente 1",
            description="Esta tarea debe persistir entre sesiones",
            due_date=datetime(2024, 12, 25, 15, 30),
            status="en_progreso"
        )
        
        task2 = session1_manager.create_task(
            name="Tarea persistente 2",
            description="Segunda tarea para persistencia",
            due_date=datetime(2024, 12, 31, 23, 59),
            status="completada"
        )
        
        # Modificar una tarea
        session1_manager.update_task(
            task_id=task1.id,
            description="Descripción actualizada en sesión 1"
        )
        
        # Obtener datos antes de cerrar sesión
        session1_stats = session1_manager.get_task_statistics()
        session1_tasks = session1_manager.list_tasks()
        
        # Sesión 2: Cargar datos desde archivo
        session2_manager = TaskManager(data_file=self.temp_file.name)
        
        # Verificar que los datos se cargaron correctamente
        session2_tasks = session2_manager.list_tasks()
        session2_stats = session2_manager.get_task_statistics()
        
        assert len(session2_tasks) == len(session1_tasks)
        assert session2_stats == session1_stats
        
        # Verificar datos específicos de las tareas
        loaded_task1 = session2_manager.get_task_by_id(task1.id)
        loaded_task2 = session2_manager.get_task_by_id(task2.id)
        
        assert loaded_task1.name == "Tarea persistente 1"
        assert loaded_task1.description == "Descripción actualizada en sesión 1"
        assert loaded_task1.status == "en_progreso"
        assert loaded_task1.due_date == datetime(2024, 12, 25, 15, 30)
        
        assert loaded_task2.name == "Tarea persistente 2"
        assert loaded_task2.status == "completada"
        assert loaded_task2.due_date == datetime(2024, 12, 31, 23, 59)
        
        # Sesión 3: Continuar trabajando con los datos cargados
        # Crear nueva tarea
        task3 = session2_manager.create_task(
            name="Tarea de sesión 2",
            description="Creada en la segunda sesión"
        )
        
        # Verificar que el ID se asignó correctamente
        assert task3.id == 3  # Debe continuar la secuencia
        
        # Sesión 4: Verificar persistencia final
        session3_manager = TaskManager(data_file=self.temp_file.name)
        final_tasks = session3_manager.list_tasks()
        
        assert len(final_tasks) == 3
        assert session3_manager.next_id == 4  # Debe estar listo para el siguiente ID
    
    def test_cli_integration(self):
        """✅ test_cli_integration: Verifica la integración con la interfaz CLI"""
        # Crear una instancia del CLI con nuestro TaskManager
        cli = TaskCLI()
        cli.task_manager = self.task_manager  # Usar nuestro manager de prueba
        
        # Simular creación de tarea a través del CLI
        with patch('builtins.input', side_effect=[
            "Tarea desde CLI",  # nombre
            "Descripción desde CLI",  # descripción
            "2024-12-25",  # fecha de vencimiento
            "pendiente"  # estado
        ]):
            cli.create_task()
        
        # Verificar que la tarea se creó correctamente
        tasks = cli.task_manager.list_tasks()
        assert len(tasks) == 1
        
        created_task = tasks[0]
        assert created_task.name == "Tarea desde CLI"
        assert created_task.description == "Descripción desde CLI"
        assert created_task.status == "pendiente"
        assert created_task.due_date.date() == datetime(2024, 12, 25).date()
        
        # Simular actualización de tarea
        with patch('builtins.input', side_effect=[
            str(created_task.id),  # ID de la tarea
            "Tarea actualizada desde CLI",  # nuevo nombre
            "Nueva descripción desde CLI",  # nueva descripción
            "",  # mantener fecha actual
            "en_progreso"  # nuevo estado
        ]):
            cli.update_task()
        
        # Verificar actualización
        updated_task = cli.task_manager.get_task_by_id(created_task.id)
        assert updated_task.name == "Tarea actualizada desde CLI"
        assert updated_task.description == "Nueva descripción desde CLI"
        assert updated_task.status == "en_progreso"
        
        # Simular búsqueda
        with patch('builtins.input', return_value="CLI"):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                cli.search_tasks()
                output = mock_stdout.getvalue()
                # El nombre puede estar truncado en la tabla, busquemos por "actualizada"
                assert "actualizada" in output or "CLI" in output
        
        # Simular eliminación
        with patch('builtins.input', side_effect=[
            str(created_task.id),  # ID de la tarea
            "s"  # confirmar eliminación
        ]):
            cli.delete_task()
        
        # Verificar eliminación
        assert len(cli.task_manager.list_tasks()) == 0
    
    def test_error_handling(self):
        """✅ test_error_handling: Verifica el manejo de errores"""
        # 1. Error al crear tarea con nombre vacío
        with pytest.raises(ValueError, match="El nombre de la tarea no puede estar vacío"):
            self.task_manager.create_task(name="")
        
        with pytest.raises(ValueError, match="El nombre de la tarea no puede estar vacío"):
            self.task_manager.create_task(name="   ")  # Solo espacios
        
        # 2. Error al crear tarea con estado inválido
        with pytest.raises(ValueError, match="Estado inválido"):
            self.task_manager.create_task(name="Tarea", status="estado_invalido")
        
        # 3. Error al actualizar tarea inexistente
        success = self.task_manager.update_task(task_id=999, name="No existe")
        assert success is False
        
        success = self.task_manager.delete_task(999)
        assert success is False
        
        # 4. Error al actualizar con estado inválido
        task = self.task_manager.create_task(name="Tarea válida")
        with pytest.raises(ValueError, match="Estado inválido"):
            self.task_manager.update_task(task_id=task.id, status="estado_invalido")
        
        # 5. Manejo de archivo corrupto
        # Escribir JSON inválido
        with open(self.temp_file.name, 'w') as f:
            f.write("json inválido {")
        
        # Crear nuevo manager con archivo corrupto
        corrupted_manager = TaskManager(data_file=self.temp_file.name)
        
        # Debe inicializar con estado limpio
        assert len(corrupted_manager.list_tasks()) == 0
        assert corrupted_manager.next_id == 1
        
        # Debe poder crear tareas normalmente después del error
        task = corrupted_manager.create_task(name="Tarea después del error")
        assert task.id == 1
        assert len(corrupted_manager.list_tasks()) == 1
    
    def test_date_filtering_integration(self):
        """Verifica la integración completa del filtrado por fechas"""
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)
        next_week = now + timedelta(days=7)
        last_week = now - timedelta(days=7)
        
        # Crear tareas con diferentes fechas
        task_past = self.task_manager.create_task(
            name="Tarea del pasado",
            due_date=last_week,
            status="pendiente"
        )
        
        task_yesterday = self.task_manager.create_task(
            name="Tarea de ayer",
            due_date=yesterday,
            status="en_progreso"
        )
        
        task_today = self.task_manager.create_task(
            name="Tarea de hoy",
            due_date=now,
            status="pendiente"
        )
        
        task_tomorrow = self.task_manager.create_task(
            name="Tarea de mañana",
            due_date=tomorrow,
            status="pendiente"
        )
        
        task_future = self.task_manager.create_task(
            name="Tarea del futuro",
            due_date=next_week,
            status="completada"
        )
        
        # Probar filtros de fecha
        # Tareas desde hoy
        from_today = self.task_manager.filter_tasks(due_date_from=now)
        assert len(from_today) == 3  # today, tomorrow, next_week
        
        # Tareas hasta mañana
        until_tomorrow = self.task_manager.filter_tasks(due_date_to=tomorrow)
        assert len(until_tomorrow) == 4  # last_week, yesterday, today, tomorrow
        
        # Tareas de esta semana (desde ayer hasta próxima semana)
        this_week = self.task_manager.filter_tasks(
            due_date_from=yesterday,
            due_date_to=next_week
        )
        assert len(this_week) == 4  # yesterday, today, tomorrow, next_week
        
        # Tareas vencidas (solo tareas no completadas que han pasado su fecha)
        overdue = self.task_manager.get_overdue_tasks()
        # Las tareas vencidas incluyen: past (pendiente), yesterday (en_progreso), y today (pendiente)
        assert len(overdue) == 3  # past, yesterday, today están todas vencidas
        
        # Verificar que las tareas vencidas son las correctas
        overdue_ids = [task.id for task in overdue]
        assert task_past.id in overdue_ids
        assert task_yesterday.id in overdue_ids
        assert task_today.id in overdue_ids  # También está vencida porque ya pasó el momento
        
        # Combinar filtros de fecha y estado
        overdue_pending = self.task_manager.filter_tasks(
            status="pendiente",
            due_date_to=yesterday
        )
        assert len(overdue_pending) == 1
        assert overdue_pending[0].id == task_past.id
    
    def test_export_import_integration(self):
        """Verifica la funcionalidad de exportar/importar"""
        # Crear datos de prueba
        original_tasks = []
        original_tasks.append(self.task_manager.create_task(
            name="Tarea 1",
            description="Primera tarea",
            status="completada"
        ))
        
        original_tasks.append(self.task_manager.create_task(
            name="Tarea 2",
            description="Segunda tarea",
            due_date=datetime.now() + timedelta(days=5),
            status="en_progreso"
        ))
        
        original_tasks.append(self.task_manager.create_task(
            name="Tarea 3",
            description="Tercera tarea",
            status="pendiente"
        ))
        
        # Crear archivo de exportación
        export_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        export_file.close()
        
        try:
            # Exportar tareas
            success = self.task_manager.save_to_file(export_file.name)
            assert success is True
            
            # Verificar que el archivo de exportación existe y tiene contenido
            assert os.path.exists(export_file.name)
            
            with open(export_file.name, 'r') as f:
                export_data = json.load(f)
            
            assert "tasks" in export_data
            assert "next_id" in export_data
            assert len(export_data["tasks"]) == 3
            assert export_data["next_id"] == 4
            
            # Crear nuevo manager e importar
            import_manager = TaskManager(data_file="dummy_file.json")  # Archivo que no existe
            
            success = import_manager.load_from_file(export_file.name)
            assert success is True
            
            # Verificar que los datos se importaron correctamente
            imported_tasks = import_manager.list_tasks()
            assert len(imported_tasks) == 3
            assert import_manager.next_id == 4
            
            # Verificar datos específicos
            for original_task in original_tasks:
                imported_task = import_manager.get_task_by_id(original_task.id)
                assert imported_task is not None
                assert imported_task.name == original_task.name
                assert imported_task.description == original_task.description
                assert imported_task.status == original_task.status
                # Las fechas deberían ser iguales (con pequeña tolerancia por serialización)
                time_diff = abs((imported_task.due_date - original_task.due_date).total_seconds())
                assert time_diff < 1  # Menos de 1 segundo de diferencia
                
        finally:
            # Limpiar archivo de exportación
            if os.path.exists(export_file.name):
                os.unlink(export_file.name)
    
    def test_large_dataset_performance(self):
        """Verifica el rendimiento con un conjunto grande de datos"""
        import time
        
        # Crear muchas tareas
        num_tasks = 100
        start_time = time.time()
        
        for i in range(num_tasks):
            self.task_manager.create_task(
                name=f"Tarea {i+1}",
                description=f"Descripción de la tarea número {i+1}",
                status=["pendiente", "en_progreso", "completada"][i % 3]
            )
        
        creation_time = time.time() - start_time
        
        # Verificar que se crearon todas las tareas
        assert len(self.task_manager.list_tasks()) == num_tasks
        
        # Probar operaciones de búsqueda y filtrado
        start_time = time.time()
        
        # Filtrar por estado
        pendientes = self.task_manager.get_tasks_by_status("pendiente")
        en_progreso = self.task_manager.get_tasks_by_status("en_progreso")
        completadas = self.task_manager.get_tasks_by_status("completada")
        
        # Búsqueda por texto
        search_results = self.task_manager.search_tasks("Tarea 50")
        
        # Obtener estadísticas
        stats = self.task_manager.get_task_statistics()
        
        search_time = time.time() - start_time
        
        # Verificar resultados
        assert len(pendientes) + len(en_progreso) + len(completadas) == num_tasks
        assert len(search_results) == 1  # Solo "Tarea 50"
        assert stats["total"] == num_tasks
        
        # Verificar que las operaciones fueron razonablemente rápidas
        # (estos valores pueden ajustarse según el hardware)
        assert creation_time < 5.0  # Crear 100 tareas en menos de 5 segundos
        assert search_time < 1.0   # Búsquedas en menos de 1 segundo
        
        print(f"Creación de {num_tasks} tareas: {creation_time:.2f}s")
        print(f"Operaciones de búsqueda: {search_time:.2f}s")


if __name__ == "__main__":
    pytest.main([__file__])


