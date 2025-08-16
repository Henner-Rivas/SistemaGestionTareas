"""
Módulo de interfaz de línea de comandos para el Sistema de Gestión de Tareas.

Este módulo proporciona una interfaz CLI interactiva para gestionar tareas,
permitiendo crear, actualizar, eliminar, listar y filtrar tareas.
"""

import sys
from datetime import datetime, timedelta
from typing import Optional
from .task_manager import TaskManager
from .utils import format_date, parse_date, validate_status, display_tasks_table


class TaskCLI:
    """
    Interfaz de línea de comandos para el Sistema de Gestión de Tareas.
    
    Proporciona un menú interactivo para gestionar tareas.
    """
    
    def __init__(self):
        """Inicializa la interfaz CLI."""
        self.task_manager = TaskManager()
        self.running = True
    
    def run(self):
        """
        Ejecuta el bucle principal de la interfaz CLI.
        """
        print("\n🚀 Sistema de Gestión de Tareas")
        print("=" * 50)
        
        while self.running:
            self.show_menu()
            choice = input("\nSeleccione una opción: ").strip()
            self.handle_choice(choice)
    
    def show_menu(self):
        """
        Muestra el menú principal de opciones.
        """
        print("\n📋 MENÚ PRINCIPAL")
        print("-" * 30)
        print("1. ➕ Crear nueva tarea")
        print("2. 📋 Listar todas las tareas")
        print("3. 🔍 Buscar tareas")
        print("4. ✏️  Actualizar tarea")
        print("5. ❌ Eliminar tarea")
        print("6. 📊 Ver estadísticas")
        print("7. 🔽 Filtrar tareas")
        print("8. ⚠️  Ver tareas vencidas")
        print("9. 💾 Exportar/Importar")
        print("0. 🚪 Salir")
    
    def handle_choice(self, choice: str):
        """
        Maneja la elección del usuario del menú.
        
        Args:
            choice (str): Opción seleccionada por el usuario
        """
        menu_actions = {
            '1': self.create_task,
            '2': self.list_all_tasks,
            '3': self.search_tasks,
            '4': self.update_task,
            '5': self.delete_task,
            '6': self.show_statistics,
            '7': self.filter_tasks,
            '8': self.show_overdue_tasks,
            '9': self.export_import_menu,
            '0': self.exit_program
        }
        
        action = menu_actions.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Por favor, intente nuevamente.")
        else:
            print("❌ Opción inválida. Por favor, seleccione una opción válida.")
    
    def create_task(self):
        """
        Crea una nueva tarea mediante input del usuario.
        """
        print("\n➕ CREAR NUEVA TAREA")
        print("-" * 25)
        
        name = input("Nombre de la tarea: ").strip()
        if not name:
            print("❌ El nombre de la tarea no puede estar vacío.")
            return
        
        description = input("Descripción (opcional): ").strip()
        
        # Fecha de vencimiento
        due_date_str = input("Fecha de vencimiento (YYYY-MM-DD, opcional): ").strip()
        due_date = None
        if due_date_str:
            due_date = parse_date(due_date_str)
            if not due_date:
                print("❌ Formato de fecha inválido. Usando fecha actual.")
                due_date = datetime.now()
        
        # Estado inicial
        print("\nEstados disponibles: pendiente, en_progreso, completada")
        status = input("Estado inicial (pendiente): ").strip() or "pendiente"
        if not validate_status(status):
            print("❌ Estado inválido. Usando 'pendiente'.")
            status = "pendiente"
        
        try:
            task = self.task_manager.create_task(
                name=name,
                description=description,
                due_date=due_date,
                status=status
            )
            print(f"✅ Tarea creada exitosamente: {task}")
        except ValueError as e:
            print(f"❌ Error al crear tarea: {e}")
    
    def list_all_tasks(self):
        """
        Lista todas las tareas.
        """
        print("\n📋 TODAS LAS TAREAS")
        print("-" * 20)
        
        tasks = self.task_manager.list_tasks()
        if not tasks:
            print("📝 No hay tareas registradas.")
            return
        
        display_tasks_table(tasks)
    
    def search_tasks(self):
        """
        Busca tareas por nombre o descripción.
        """
        print("\n🔍 BUSCAR TAREAS")
        print("-" * 17)
        
        query = input("Ingrese texto a buscar: ").strip()
        if not query:
            print("❌ Debe ingresar un texto para buscar.")
            return
        
        tasks = self.task_manager.search_tasks(query)
        if not tasks:
            print(f"📝 No se encontraron tareas que contengan '{query}'.")
            return
        
        print(f"\n🔍 Resultados para '{query}':")
        display_tasks_table(tasks)
    
    def update_task(self):
        """
        Actualiza una tarea existente.
        """
        print("\n✏️ ACTUALIZAR TAREA")
        print("-" * 19)
        
        try:
            task_id = int(input("ID de la tarea a actualizar: "))
        except ValueError:
            print("❌ ID inválido. Debe ser un número.")
            return
        
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"❌ No se encontró tarea con ID {task_id}.")
            return
        
        print(f"\nTarea actual: {task}")
        print("\nDeje en blanco para mantener el valor actual:")
        
        # Nuevo nombre
        name = input(f"Nuevo nombre ({task.name}): ").strip()
        name = name if name else None
        
        # Nueva descripción
        description = input(f"Nueva descripción ({task.description}): ").strip()
        description = description if description else None
        
        # Nueva fecha
        due_date_str = input(f"Nueva fecha ({format_date(task.due_date)}): ").strip()
        due_date = None
        if due_date_str:
            due_date = parse_date(due_date_str)
            if not due_date:
                print("❌ Formato de fecha inválido. Manteniendo fecha actual.")
        
        # Nuevo estado
        print("\nEstados disponibles: pendiente, en_progreso, completada")
        status = input(f"Nuevo estado ({task.status}): ").strip()
        status = status if status and validate_status(status) else None
        
        try:
            success = self.task_manager.update_task(
                task_id=task_id,
                name=name,
                description=description,
                due_date=due_date,
                status=status
            )
            
            if success:
                print("✅ Tarea actualizada exitosamente.")
            else:
                print("❌ Error al actualizar la tarea.")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def delete_task(self):
        """
        Elimina una tarea.
        """
        print("\n❌ ELIMINAR TAREA")
        print("-" * 17)
        
        try:
            task_id = int(input("ID de la tarea a eliminar: "))
        except ValueError:
            print("❌ ID inválido. Debe ser un número.")
            return
        
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"❌ No se encontró tarea con ID {task_id}.")
            return
        
        print(f"\nTarea a eliminar: {task}")
        confirm = input("¿Está seguro? (s/N): ").strip().lower()
        
        if confirm == 's':
            if self.task_manager.delete_task(task_id):
                print("✅ Tarea eliminada exitosamente.")
            else:
                print("❌ Error al eliminar la tarea.")
        else:
            print("❌ Eliminación cancelada.")
    
    def show_statistics(self):
        """
        Muestra estadísticas de las tareas.
        """
        print("\n📊 ESTADÍSTICAS")
        print("-" * 15)
        
        stats = self.task_manager.get_task_statistics()
        
        print(f"📋 Total de tareas: {stats['total']}")
        print(f"⏳ Pendientes: {stats['pendiente']}")
        print(f"🔄 En progreso: {stats['en_progreso']}")
        print(f"✅ Completadas: {stats['completada']}")
        print(f"⚠️  Vencidas: {stats['vencidas']}")
        
        if stats['total'] > 0:
            completion_rate = (stats['completada'] / stats['total']) * 100
            print(f"📈 Tasa de finalización: {completion_rate:.1f}%")
    
    def filter_tasks(self):
        """
        Filtra tareas por diferentes criterios.
        """
        print("\n🔽 FILTRAR TAREAS")
        print("-" * 17)
        
        print("Criterios de filtrado (deje en blanco para omitir):")
        
        # Filtro por estado
        status = input("Estado (pendiente/en_progreso/completada): ").strip()
        status = status if status and validate_status(status) else None
        
        # Filtro por fecha desde
        date_from_str = input("Fecha desde (YYYY-MM-DD): ").strip()
        date_from = parse_date(date_from_str) if date_from_str else None
        
        # Filtro por fecha hasta
        date_to_str = input("Fecha hasta (YYYY-MM-DD): ").strip()
        date_to = parse_date(date_to_str) if date_to_str else None
        
        # Filtro por texto en nombre
        name_contains = input("Texto en el nombre: ").strip()
        name_contains = name_contains if name_contains else None
        
        tasks = self.task_manager.filter_tasks(
            status=status,
            due_date_from=date_from,
            due_date_to=date_to,
            name_contains=name_contains
        )
        
        if not tasks:
            print("📝 No se encontraron tareas con los criterios especificados.")
            return
        
        print(f"\n🔽 Tareas filtradas ({len(tasks)} encontradas):")
        display_tasks_table(tasks)
    
    def show_overdue_tasks(self):
        """
        Muestra las tareas vencidas.
        """
        print("\n⚠️ TAREAS VENCIDAS")
        print("-" * 18)
        
        overdue_tasks = self.task_manager.get_overdue_tasks()
        
        if not overdue_tasks:
            print("✅ No hay tareas vencidas.")
            return
        
        print(f"⚠️  {len(overdue_tasks)} tarea(s) vencida(s):")
        display_tasks_table(overdue_tasks)
    
    def export_import_menu(self):
        """
        Menú para exportar/importar tareas.
        """
        print("\n💾 EXPORTAR/IMPORTAR")
        print("-" * 20)
        print("1. Exportar tareas a archivo")
        print("2. Importar tareas desde archivo")
        print("3. Volver al menú principal")
        
        choice = input("Seleccione una opción: ").strip()
        
        if choice == '1':
            self.export_tasks()
        elif choice == '2':
            self.import_tasks()
        elif choice == '3':
            return
        else:
            print("❌ Opción inválida.")
    
    def export_tasks(self):
        """
        Exporta las tareas a un archivo.
        """
        filename = input("Nombre del archivo (tasks_backup.json): ").strip()
        filename = filename if filename else "tasks_backup.json"
        
        if self.task_manager.save_to_file(filename):
            print(f"✅ Tareas exportadas exitosamente a '{filename}'.")
        else:
            print("❌ Error al exportar las tareas.")
    
    def import_tasks(self):
        """
        Importa tareas desde un archivo.
        """
        filename = input("Nombre del archivo a importar: ").strip()
        if not filename:
            print("❌ Debe especificar un nombre de archivo.")
            return
        
        print("⚠️  ADVERTENCIA: Esto reemplazará todas las tareas actuales.")
        confirm = input("¿Continuar? (s/N): ").strip().lower()
        
        if confirm == 's':
            if self.task_manager.load_from_file(filename):
                print(f"✅ Tareas importadas exitosamente desde '{filename}'.")
            else:
                print("❌ Error al importar las tareas.")
        else:
            print("❌ Importación cancelada.")
    
    def exit_program(self):
        """
        Sale del programa.
        """
        print("\n👋 ¡Hasta luego!")
        print("Todas las tareas han sido guardadas automáticamente.")
        self.running = False


def main():
    """
    Función principal para ejecutar la CLI.
    """
    try:
        cli = TaskCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, reporte este error.")
        sys.exit(1)


if __name__ == "__main__":
    main()
