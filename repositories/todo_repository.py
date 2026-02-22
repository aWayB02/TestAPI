from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import TodoDB
from models.todo import Todo
from datetime import datetime


class TodoRepository:
    """Репозиторий для работы с задачами в базе данных"""

    def __init__(self, db: Session):
        """
        Инициализация репозитория

        Args:
            db (Session): Сессия базы данных
        """
        self.db = db

    def create(self, todo: Todo) -> Todo:
        """
        Создание новой задачи

        Args:
            todo (Todo): Объект задачи для создания

        Returns:
            Todo: Созданная задача
        """
        db_todo = TodoDB(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)

        # Преобразуем обратно в модель Todo
        return Todo(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            completed=db_todo.completed,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
        )

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Получение задачи по ID

        Args:
            todo_id (int): Идентификатор задачи

        Returns:
            Optional[Todo]: Задача или None, если не найдена
        """
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if db_todo:
            return Todo(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                completed=db_todo.completed,
                created_at=db_todo.created_at,
                updated_at=db_todo.updated_at,
            )
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Получение всех задач с пагинацией

        Args:
            skip (int): Количество пропускаемых записей
            limit (int): Максимальное количество записей

        Returns:
            List[Todo]: Список задач
        """
        db_todos = self.db.query(TodoDB).offset(skip).limit(limit).all()
        return [
            Todo(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                completed=db_todo.completed,
                created_at=db_todo.created_at,
                updated_at=db_todo.updated_at,
            )
            for db_todo in db_todos
        ]

    def get_by_status(
        self, completed: bool, skip: int = 0, limit: int = 100
    ) -> List[Todo]:
        """
        Получение задач по статусу выполнения

        Args:
            completed (bool): Статус выполнения
            skip (int): Количество пропускаемых записей
            limit (int): Максимальное количество записей

        Returns:
            List[Todo]: Список задач
        """
        db_todos = (
            self.db.query(TodoDB)
            .filter(TodoDB.completed == completed)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            Todo(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                completed=db_todo.completed,
                created_at=db_todo.created_at,
                updated_at=db_todo.updated_at,
            )
            for db_todo in db_todos
        ]

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Todo]:
        """
        Обновление задачи

        Args:
            todo_id (int): Идентификатор задачи
            title (Optional[str]): Новый заголовок
            description (Optional[str]): Новое описание
            completed (Optional[bool]): Новый статус выполнения

        Returns:
            Optional[Todo]: Обновленная задача или None, если не найдена
        """
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if not db_todo:
            return None

        if title is not None:
            db_todo.title = title
        if description is not None:
            db_todo.description = description
        if completed is not None:
            db_todo.completed = completed

        db_todo.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(db_todo)

        return Todo(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            completed=db_todo.completed,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
        )

    def delete(self, todo_id: int) -> bool:
        """
        Удаление задачи

        Args:
            todo_id (int): Идентификатор задачи

        Returns:
            bool: True, если задача была удалена, False если не найдена
        """
        db_todo = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if db_todo:
            self.db.delete(db_todo)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """
        Получение общего количества задач

        Returns:
            int: Общее количество задач
        """
        return self.db.query(func.count(TodoDB.id)).scalar()

    def count_by_status(self, completed: bool) -> int:
        """
        Получение количества задач по статусу

        Args:
            completed (bool): Статус выполнения

        Returns:
            int: Количество задач с указанным статусом
        """
        return (
            self.db.query(func.count(TodoDB.id))
            .filter(TodoDB.completed == completed)
            .scalar()
        )
