from db import *

# Helper function to search tasks assigned to a user
def search_tasks_by_user(user_id):
    tasks = session.query(Task).filter(Task.assigned_to.ilike(f'%{user_id}%')).all()
    return tasks

def search_tasks_by_author_id(author_id):
    tasks = session.query(Task).filter(Task.author_id.ilike(f'%{author_id}%')).all()
    return tasks

# Helper function to search tasks assigned to a user
def search_tasks_by_task_id(task_id):
    task = session.query(Task).get(task_id)
    if task: return task
    return False

# Helper function to create a new task
def create_task(author_id, assigned_to, description, deadline):
    task = Task(author_id=author_id, assigned_to=assigned_to, description=description, deadline=deadline)
    session.add(task)
    session.commit()
    return task

# Helper function to delete a task
def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()

# Helper function to update a user's name
def add_experience(task_id, experience):
    task = session.query(Task).get(task_id)
    if task:
        task.experience = experience
        session.commit()
        return task
    else:
        return None
    
# Helper function to update a user's name
def mark_task_done(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.isdone = True
        session.commit()
        return task
    else:
        return None