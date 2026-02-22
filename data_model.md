# Модель данных To-Do List

## Описание модели задачи (Todo)

### Поля модели

| Название поля | Тип данных | Обязательное | Описание |
|--------------|-----------|-------------|----------|
| id | Integer | Да | Уникальный идентификатор задачи (первичный ключ) |
| title | String (255) | Да | Заголовок задачи |
| description | Text | Нет | Описание задачи |
| completed | Boolean | Да | Статус выполнения задачи (по умолчанию False) |
| created_at | DateTime | Да | Дата и время создания задачи |
| updated_at | DateTime | Нет | Дата и время последнего обновления задачи |

### Методы модели

1. `__init__(self, title, description=None)` - конструктор модели
2. `to_dict()` - преобразование объекта в словарь для сериализации
3. `from_dict(data)` - создание объекта из словаря
4. `mark_completed()` - пометить задачу как выполненную
5. `mark_uncompleted()` - пометить задачу как невыполненную
6. `update(title=None, description=None)` - обновление данных задачи

## ER-диаграмма

```
mermaid
erDiagram
    TODO_ITEMS {
        integer id PK
        string title
        text description
        boolean completed
        datetime created_at
        datetime updated_at
    }
```

## SQL схема таблицы

```sql
CREATE TABLE todo_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

## Валидация данных

### Правила валидации

1. **title**:
   - Обязательное поле
   - Минимальная длина: 1 символ
   - Максимальная длина: 255 символов
   - Не может содержать только пробельные символы

2. **description**:
   - Опциональное поле
   - Максимальная длина: 1000 символов (если задано)

3. **completed**:
   - Булево значение
   - По умолчанию: False

## Пример использования модели

```python
# Создание новой задачи
todo = Todo(title="Купить молоко", description="Сходить в магазин и купить молоко")

# Преобразование в словарь для JSON сериализации
todo_dict = todo.to_dict()

# Пометить как выполненную
todo.mark_completed()

# Обновить данные
todo.update(title="Купить молоко и хлеб")