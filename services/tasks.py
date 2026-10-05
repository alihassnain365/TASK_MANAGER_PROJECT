from models import Task
import services.exceptions as exceptions
from sqlalchemy import select

"""1. creating the task"""
def create_task(db,title,user_id,status):
    task = Task(title=title, user_id=user_id, status=status)
    db.add(task)
    db.commit()
    return task

"""2. get the list of tasks"""
def get_list(db,user_id):
    result = db.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
    if result is None:
        raise exceptions.TaskNotFound()
    return result


"""3. mark the test complete"""
def mark_task_complete(db, task_id, user_id):
    task = db.get(Task, task_id)
    if task is None:
        raise exceptions.TaskNotFound() 
    if task.user_id != user_id:
        raise exceptions.ForbidenRequest()
    task.status = True
    db.commit()
    return task

"""4. delete task"""
def delete_task(db,task_id, user_id):
    task = db.get(Task, task_id)
    if task is None:
        raise exceptions.TaskNotFound()
    if task.user_id != user_id:
        raise exceptions.ForbidenRequest()
    db.delete(task)
    db.commit()