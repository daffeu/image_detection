from db.models.tasks import Tasks
from sqlalchemy.orm import Session
from schemas.tasks import TasksBase


def list_tasks(db: Session):
    items = db.query(Tasks).all()
    return items


def retreive_task(id: int, db: Session):
    item = db.query(Tasks).filter(Tasks.id == id).first()
    return item


def create_new_task(task: TasksBase, db: Session):
    task_object = Tasks(**task.dict())
    db.add(task_object)
    db.commit()
    db.refresh(task_object)
    return task_object