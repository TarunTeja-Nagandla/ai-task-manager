from langchain.tools import tool
from database import LocalSession, Task
from datetime import datetime, date
from sqlalchemy import select
from typing import Optional

@tool
def create_tasks(title: str, description: str = "", priority: str = "medium", due_date: Optional[str] = None):
    """
    Creates and saves a new task in the database.
    Args:
        title (str): Short, descriptive title for the task (Required).
        description (str, optional): Additional detailed notes or context for the task. Defaults to None.
        priority (str, optional): Urgency level. Allowed values: 'low', 'medium', 'high'. Defaults to 'medium'.
        due_date (str, optional): Target completion date in 'YYYY-MM-DD' format (e.g., '2026-08-15'). Defaults to None.
    """
    task_priority = priority.lower() if priority else "medium"
    if task_priority not in ["low", "high", "medium"]:
        task_priority = "medium"

    with LocalSession() as session:
        task = Task(
            title=title,
            description=description,
            priority=task_priority,
            due_date=date.fromisoformat(due_date) if due_date else None
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return f"""
        Task Created Successfully!

        ID : {task.id}
        Title : {task.title}
        Priority : {task.priority}
        Status : {task.status}
        """

@tool
def list_tasks(status: str = "all", priority: str = "all"):
    """
    Retrieves and lists tasks from the database with optional filtering.
    Args:
        status (str, optional): Filter by task status. Allowed values: 'pending', 'in_progress', 'done', or 'all'. Use 'all' to fetch all tasks regardless of status. Defaults to 'all'.
        priority (str, optional): Filter by task priority. Allowed values: 'low', 'medium', 'high', or 'all'. Use 'all' to fetch all priorities. Defaults to 'all'.
    """
    with LocalSession() as session:
        status = status.lower()
        priority = priority.lower()
        query = select(Task)
        if status != "all":
            query = query.where(Task.status == status)
        if priority != "all":
            query = query.where(Task.priority == priority)

        query = query.order_by(Task.id)
        results = session.scalars(query).all()
        if not results:
            return "No Tasks Found !"
        all_tasks = [todo.to_dict() for todo in results]
        return all_tasks

@tool
def update_tasks(
    task_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    status: Optional[str] = None, 
    priority: Optional[str] = None, 
    due_date: Optional[str] = None):
    """
    Updates specific fields of an existing task identified by its task_id. Only pass arguments for fields that need to be changed.
    Args:
        task_id (int): The unique integer ID of the task to update (Required).
        title (str, optional): Updated task title. Omit or pass None if unchanged.
        description (str, optional): Updated task description. Omit or pass None if unchanged.
        status (str, optional): Updated status. Allowed values: 'pending', 'in_progress', 'done'. Omit if unchanged.
        priority (str, optional): Updated priority. Allowed values: 'low', 'medium', 'high'. Omit if unchanged.
        due_date (str, optional): Updated target completion date in 'YYYY-MM-DD' format (e.g., '2026-08-15'). Omit if unchanged.
    """
    with LocalSession() as session:
        task = session.get(Task, task_id)
        if not task:
            return f"Task with ID {task_id} Not Found..."
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date

        session.commit()
        session.refresh(task)
        return f"""
            Task: {task.id} Updated!
            {task.to_dict()}
        """

@tool
def delete_tasks(task_id: int):
    """
    Permanently deletes a task from the database using its unique task ID.
    Args:
        task_id (int): The unique integer ID of the task to delete (Required).
    """
    with LocalSession() as session:
        task = session.get(Task, task_id)
        if not task:
            return f"Task with ID {task_id} Not Found..."
        task_title = task.title
        session.delete(task)
        session.commit()
        return f"""
            Task Deleted Successfully.
            {task_id}: {task_title}
        """