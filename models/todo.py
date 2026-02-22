from datetime import datetime
from typing import Optional


class Todo:
    """Модель задачи (to-do item)"""

    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        id: Optional[int] = None,
        completed: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        """
        Инициализация задачи

        Args:
            title (str): Заголовок задачи
            description (Optional[str]): Описание задачи
            id (Optional[int]): Уникальный идентификатор задачи
            completed (bool): Статус выполнения задачи
            created_at (Optional[datetime]): Дата и время создания задачи
            updated_at (Optional[datetime]): Дата и время последнего обновления задачи
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """
        Преобразование объекта задачи в словарь

        Returns:
            dict: Словарь с данными задачи
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """
        Создание объекта задачи из словаря

        Args:
            data (dict): Словарь с данными задачи

        Returns:
            Todo: Объект задачи
        """
        created_at = (
            datetime.fromisoformat(data["created_at"])
            if data.get("created_at")
            else None
        )
        updated_at = (
            datetime.fromisoformat(data["updated_at"])
            if data.get("updated_at")
            else None
        )

        return cls(
            id=data.get("id"),
            title=data["title"],
            description=data.get("description"),
            completed=data.get("completed", False),
            created_at=created_at,
            updated_at=updated_at,
        )

    def mark_completed(self):
        """Пометить задачу как выполненную"""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_uncompleted(self):
        """Пометить задачу как невыполненную"""
        self.completed = False
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None):
        """
        Обновление данных задачи

        Args:
            title (Optional[str]): Новый заголовок задачи
            description (Optional[str]): Новое описание задачи
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """Строковое представление задачи"""
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"

    def __eq__(self, other) -> bool:
        """Сравнение задач по ID"""
        if not isinstance(other, Todo):
            return False
        return self.id == other.id
