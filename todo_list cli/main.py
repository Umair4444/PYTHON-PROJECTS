import click as cli
import os
import json

TODO_FILE = "todo.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open (TODO_FILE,"r") as file:
        return json.load(file) 
    
def save_tasks(tasks):
    with open(TODO_FILE,"w") as file:
        json.dump(tasks,file,indent=4)

@cli.group()
def cmd():
    """Simple Todo List Manager"""
    pass

@cli.command()
@cli.argument("task")
def add(task):
    """Adding Task"""
    tasks = load_tasks()
    tasks.append({"task":task,"done":False})
    save_tasks(tasks)
    cli.echo(f"Task added Successfully : {task}")

@cli.command()
def list():
    """List All Tasks"""
    tasks = load_tasks()
    if not tasks:
        cli.echo("No task found")
        return
    for index,task in enumerate(tasks,1):
        status = "✅" if task["done"] else "❌"
        cli.echo(f"{index} : {task["task"]} -- {status}")

@cli.command()
@cli.argument("task_number",type=int)
def remove(task_number):
    """Remove task"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        remove = tasks.pop(task_number-1)
        save_tasks(tasks)
        cli.echo(f"remove task is {remove['task']}") 
    else:
        cli.echo(f"invlid task number")    

@cli.command()
@cli.argument('task_number',type=int)
def complete(task_number):
    """Make your Task Complete"""
    tasks=load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number-1]["done"] = True
        save_tasks(tasks)
        print("debug",task_number)
        print("debug",task_number-1)
        cli.echo(f"Task -- {tasks[task_number-1]["task"]} marked as completed!")  
    else:
        cli.echo("Invalid task number.") 


cmd.add_command(add)
cmd.add_command(list)
cmd.add_command(remove)
cmd.add_command(complete)


if __name__ == "__main__":
    cmd()

