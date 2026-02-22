from typing import List, Optional
from models.todo import Todo
from repositories.todo_repository import TodoRepository
from sqlalchemy.orm import Session


class TodoService:
    """Сервис для работы с задачами"""

    def __init__(self, db: Session):
        """
        Инициализация сервиса

        Args:
            db (Session): Сессия базы данных
        """
        self.repository = TodoRepository(db)

    def create_todo(self, title: str, description: Optional[str] = None) -> Todo:
        """
        Создание новой задачи

        Args:
            title (str): Заголовок задачи
            description (Optional[str]): Описание задачи

        Returns:
            Todo: Созданная задача

        Raises:
            ValueError: Если заголовок пустой или содержит только пробельные символы
        """
        # Валидация заголовка
        if not title or not title.strip():
            raise ValueError("Заголовок задачи не может быть пустым")

        if len(title.strip()) > 255:
            raise ValueError("Заголовок задачи не может превышать 255 символов")

        # Создание задачи
        todo = Todo(title=title.strip(), description=description)
        return self.repository.create(todo)

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Получение задачи по ID

        Args:
            todo_id (int): Идентификатор задачи

        Returns:
            Optional[Todo]: Задача или None, если не найдена
        """
        return self.repository.get_by_id(todo_id)

    def get_all_todos(
        self, completed: Optional[bool] = None, skip: int = 0, limit: int = 100
    ) -> List[Todo]:
        """
        Получение всех задач

        Args:
            completed (Optional[bool]): Фильтр по статусу выполнения
            skip (int): Количество пропускаемых записей
            limit (int): Максимальное количество записей

        Returns:
            List[Todo]: Список задач
        """
        if completed is not None:
            return self.repository.get_by_status(completed, skip, limit)
        return self.repository.get_all(skip, limit)

    def update_todo(
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

        Raises:
            ValueError: Если заголовок пустой или содержит только пробельные символы
        """
        # Валидация заголовка, если он передан
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Заголовок задачи не может быть пустым")

            if len(title.strip()) > 255:
                raise ValueError("Заголовок задачи не может превышать 255 символов")

            title = title.strip()

        # Валидация описания, если оно передано
        if description is not None and len(description) > 1000:
            raise ValueError("Описание задачи не может превышать 1000 символов")

        return self.repository.update(todo_id, title, description, completed)

    def delete_todo(self, todo_id: int) -> bool:
        """
        Удаление задачи

        Args:
            todo_id (int): Идентификатор задачи

        Returns:
            bool: True, если задача была удалена, False если не найдена
        """
        return self.repository.delete(todo_id)

    def toggle_todo_status(self, todo_id: int) -> Optional[Todo]:
        """
        Переключение статуса выполнения задачи

        Args:
            todo_id (int): Идентификатор задачи

        Returns:
            Optional[Todo]: Обновленная задача или None, если не найдена
        """
        todo = self.get_todo(todo_id)
        if not todo:
            return None

        # Переключаем статус
        new_status = not todo.completed
        return self.update_todo(todo_id, completed=new_status)

    def get_stats(self) -> dict:
        """
        Получение статистики по задачам

        Returns:
            dict: Словарь со статистикой
        """
        total = self.repository.count()
        completed = self.repository.count_by_status(True)
        pending = self.repository.count_by_status(False)

        return {"total": total, "completed": completed, "pending": pending}
