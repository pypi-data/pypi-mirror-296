import click
import json
import os
from guigaga import gui

DATA_FILE = 'tasks.json'

def read_tasks():
    """Read tasks from the data file, if it exists."""
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def write_tasks(tasks):
    """Write tasks to the data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)

@gui()
@click.group()
def cli():
    """Simple TODO list command line app"""
    pass

# Define a group for task-related commands
@click.group()
def task():
    """Task-related commands."""
    pass

@task.command()
@click.argument('task_content')
def add(task_content):
    """Add a task to the TODO list."""
    tasks = read_tasks()
    tasks.append(task_content)
    write_tasks(tasks)
    click.echo(f"Added task: {task_content}")

@task.command()
@click.argument('task_content')
def done(task_content):
    """Remove a task from the TODO list."""
    tasks = read_tasks()
    if task_content in tasks:
        tasks.remove(task_content)
        write_tasks(tasks)
        click.echo(f"Removed task: {task_content}")
    else:
        click.echo(f"Task '{task_content}' not found.")

@task.command(name='list')  # we use name parameter to avoid clashing with built-in list
def list_tasks():
    """List the tasks in the TODO list."""
    tasks = read_tasks()
    if tasks:
        for i, task_content in enumerate(tasks, 1):
            click.echo(f"{i}. {task_content}")
    else:
        click.echo("No tasks found.")

# Add the task group to the primary CLI
cli.add_command(task)

if __name__ == '__main__':
    cli()
