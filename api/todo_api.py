from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from database.db import get_db, init_database
from services.todo_service import TodoService
from models.todo import Todo

# Создание роутера
router = APIRouter(
    prefix="/api/v1/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    """
    Получение экземпляра сервиса задач

    Args:
        db (Session): Сессия базы данных

    Returns:
        TodoService: Экземпляр сервиса задач
    """
    return TodoService(db)


@router.get("/", response_model=dict)
async def get_todos(
    completed: Optional[bool] = Query(None, description="Фильтр по статусу выполнения"),
    limit: int = Query(
        100, ge=1, le=1000, description="Максимальное количество результатов"
    ),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    service: TodoService = Depends(get_todo_service),
):
    """
    Получение списка всех задач

    Args:
        completed (Optional[bool]): Фильтр по статусу выполнения
        limit (int): Максимальное количество результатов
        offset (int): Смещение для пагинации
        service (TodoService): Сервис задач

    Returns:
        dict: Словарь с данными задач
    """
    todos = service.get_all_todos(completed=completed, skip=offset, limit=limit)
    count = len(todos)

    return {
        "status": "success",
        "data": [todo.to_dict() for todo in todos],
        "count": count,
    }


@router.get("/{todo_id}", response_model=dict)
async def get_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    """
    Получение задачи по ID

    Args:
        todo_id (int): Идентификатор задачи
        service (TodoService): Сервис задач

    Returns:
        dict: Словарь с данными задачи

    Raises:
        HTTPException: Если задача не найдена
    """
    todo = service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return {"status": "success", "data": todo.to_dict()}


@router.post("/", response_model=dict, status_code=201)
async def create_todo(
    todo_data: dict, service: TodoService = Depends(get_todo_service)
):
    """
    Создание новой задачи

    Args:
        todo_data (dict): Данные задачи
        service (TodoService): Сервис задач

    Returns:
        dict: Словарь с данными созданной задачи
    """
    try:
        title = todo_data.get("title")
        description = todo_data.get("description")

        if not title:
            raise HTTPException(
                status_code=400, detail="Поле 'title' обязательно для заполнения"
            )

        todo = service.create_todo(title, description)

        return {"status": "success", "data": todo.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{todo_id}", response_model=dict)
async def update_todo(
    todo_id: int, todo_data: dict, service: TodoService = Depends(get_todo_service)
):
    """
    Обновление задачи

    Args:
        todo_id (int): Идентификатор задачи
        todo_data (dict): Данные для обновления
        service (TodoService): Сервис задач

    Returns:
        dict: Словарь с данными обновленной задачи

    Raises:
        HTTPException: Если задача не найдена или данные некорректны
    """
    try:
        # Проверяем, что задача существует
        existing_todo = service.get_todo(todo_id)
        if not existing_todo:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        # Обработка значения completed с преобразованием типов
        completed = todo_data.get("completed")
        if completed is not None:
            if isinstance(completed, bool):
                # Если уже булево значение, оставляем как есть
                pass
            elif isinstance(completed, str):
                # Преобразуем строковые значения в булевы
                completed = completed.lower() in ("true", "1", "yes", "on")
            elif isinstance(completed, (int, float)):
                # Преобразуем числовые значения в булевы
                completed = bool(completed)
            else:
                # Для других типов данных устанавливаем None
                completed = None
        # Обновляем задачу
        todo = service.update_todo(
            todo_id,
            title=todo_data.get("title"),
            description=todo_data.get("description"),
            completed=completed,
        )

        if not todo:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        return {"status": "success", "data": todo.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    """
    Удаление задачи

    Args:
        todo_id (int): Идентификатор задачи
        service (TodoService): Сервис задач

    Returns:
        dict: Словарь с сообщением об успешном удалении

    Raises:
        HTTPException: Если задача не найдена
    """
    success = service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return {"status": "success", "message": "Задача успешно удалена"}


@router.get("/stats", response_model=dict)
async def get_stats(service: TodoService = Depends(get_todo_service)):
    """
    Получение статистики по задачам

    Args:
        service (TodoService): Сервис задач

    Returns:
        dict: Словарь со статистикой
    """
    stats = service.get_stats()

    return {"status": "success", "data": stats}
