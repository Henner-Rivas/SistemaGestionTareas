"""
Interfaz de línea de comandos para el Sistema de Gestión de Tareas
"""

import click
from tabulate import tabulate
from colorama import init, Fore, Style
from .task_manager import TaskManager
from .task import TaskStatus, TaskPriority
from .utils import format_datetime, get_task_summary, sort_tasks_by_priority

# Inicializar colorama para Windows
init()

# Instancia global del gestor de tareas
task_manager = TaskManager()

@click.group()
def main():
    """Sistema de Gestión de Tareas - Administra tus tareas de forma eficiente"""
    pass

@main.command()
@click.argument('title')
@click.option('--description', '-d', default="", help='Descripción de la tarea')
@click.option('--priority', '-p', 
              type=click.Choice(['baja', 'media', 'alta']), 
              default='media', 
              help='Prioridad de la tarea')
def add(title, description, priority):
    """Añade una nueva tarea"""
    priority_enum = TaskPriority(priority)
    task = task_manager.add_task(title, description, priority_enum)
    click.echo(f"{Fore.GREEN}✅ Tarea creada exitosamente:{Style.RESET_ALL}")
    click.echo(f"   ID: {task.id}")
    click.echo(f"   Título: {task.title}")
    click.echo(f"   Prioridad: {priority}")

@main.command()
@click.option('--status', '-s', 
              type=click.Choice(['pendiente', 'en_progreso', 'completada']),
              help='Filtrar por estado')
@click.option('--priority', '-p',
              type=click.Choice(['baja', 'media', 'alta']),
              help='Filtrar por prioridad')
def list(status, priority):
    """Lista todas las tareas o filtra por estado/prioridad"""
    tasks = task_manager.get_all_tasks()
    
    if status:
        tasks = [t for t in tasks if t.status == TaskStatus(status)]
    
    if priority:
        tasks = [t for t in tasks if t.priority == TaskPriority(priority)]
    
    if not tasks:
        click.echo(f"{Fore.YELLOW}No se encontraron tareas.{Style.RESET_ALL}")
        return
    
    # Ordenar por prioridad
    tasks = sort_tasks_by_priority(tasks)
    
    # Crear tabla
    table_data = []
    for task in tasks:
        status_color = {
            TaskStatus.PENDIENTE: Fore.YELLOW,
            TaskStatus.EN_PROGRESO: Fore.BLUE,
            TaskStatus.COMPLETADA: Fore.GREEN
        }
        priority_color = {
            TaskPriority.BAJA: Fore.GREEN,
            TaskPriority.MEDIA: Fore.YELLOW,
            TaskPriority.ALTA: Fore.RED
        }
        
        table_data.append([
            task.id,
            task.title[:50] + "..." if len(task.title) > 50 else task.title,
            f"{status_color[task.status]}{task.status.value}{Style.RESET_ALL}",
            f"{priority_color[task.priority]}{task.priority.value}{Style.RESET_ALL}",
            format_datetime(task.created_at)
        ])
    
    headers = ["ID", "Título", "Estado", "Prioridad", "Creada"]
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))

@main.command()
@click.argument('task_id', type=int)
def show(task_id):
    """Muestra los detalles completos de una tarea"""
    task = task_manager.get_task(task_id)
    if not task:
        click.echo(f"{Fore.RED}❌ Tarea con ID {task_id} no encontrada.{Style.RESET_ALL}")
        return
    
    click.echo(f"\n{Fore.CYAN}📋 Detalles de la Tarea:{Style.RESET_ALL}")
    click.echo(f"   ID: {task.id}")
    click.echo(f"   Título: {task.title}")
    click.echo(f"   Descripción: {task.description or 'Sin descripción'}")
    click.echo(f"   Estado: {task.status.value}")
    click.echo(f"   Prioridad: {task.priority.value}")
    click.echo(f"   Creada: {format_datetime(task.created_at)}")
    click.echo(f"   Actualizada: {format_datetime(task.updated_at)}")
    if task.completed_at:
        click.echo(f"   Completada: {format_datetime(task.completed_at)}")

@main.command()
@click.argument('task_id', type=int)
@click.argument('status', type=click.Choice(['pendiente', 'en_progreso', 'completada']))
def update_status(task_id, status):
    """Actualiza el estado de una tarea"""
    status_enum = TaskStatus(status)
    if task_manager.update_task_status(task_id, status_enum):
        click.echo(f"{Fore.GREEN}✅ Estado actualizado a '{status}' para la tarea {task_id}{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}❌ Tarea con ID {task_id} no encontrada.{Style.RESET_ALL}")

@main.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Marca una tarea como completada"""
    if task_manager.update_task_status(task_id, TaskStatus.COMPLETADA):
        click.echo(f"{Fore.GREEN}✅ Tarea {task_id} marcada como completada.{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}❌ Tarea con ID {task_id} no encontrada.{Style.RESET_ALL}")

@main.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='¿Estás seguro de que quieres eliminar esta tarea?')
def delete(task_id):
    """Elimina una tarea"""
    if task_manager.delete_task(task_id):
        click.echo(f"{Fore.GREEN}✅ Tarea {task_id} eliminada exitosamente.{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}❌ Tarea con ID {task_id} no encontrada.{Style.RESET_ALL}")

@main.command()
@click.argument('query')
def search(query):
    """Busca tareas por título o descripción"""
    tasks = task_manager.search_tasks(query)
    if not tasks:
        click.echo(f"{Fore.YELLOW}No se encontraron tareas que coincidan con '{query}'.{Style.RESET_ALL}")
        return
    
    click.echo(f"{Fore.CYAN}🔍 Resultados de búsqueda para '{query}':{Style.RESET_ALL}")
    for task in tasks:
        click.echo(f"   {get_task_summary(task)}")

@main.command()
def stats():
    """Muestra estadísticas del sistema"""
    stats = task_manager.get_stats()
    
    click.echo(f"\n{Fore.CYAN}📊 Estadísticas del Sistema:{Style.RESET_ALL}")
    click.echo(f"   Total de tareas: {stats['total']}")
    click.echo(f"   Completadas: {Fore.GREEN}{stats['completed']}{Style.RESET_ALL}")
    click.echo(f"   En progreso: {Fore.BLUE}{stats['in_progress']}{Style.RESET_ALL}")
    click.echo(f"   Pendientes: {Fore.YELLOW}{stats['pending']}{Style.RESET_ALL}")
    click.echo(f"   Tasa de completitud: {stats['completion_rate']:.1f}%")

if __name__ == '__main__':
    main()
