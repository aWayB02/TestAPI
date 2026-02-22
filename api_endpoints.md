# API Endpoints для To-Do List

## Общая информация

- Формат ответа: JSON
- Кодировка: UTF-8
- Базовый URL: /api/v1

## Эндпоинты

### 1. Получить список всех задач

**GET** `/api/v1/todos`

**Описание**: Возвращает список всех задач

**Параметры запроса**:
- `completed` (опционально) - фильтр по статусу выполнения (true/false)
- `limit` (опционально) - ограничение количества результатов (по умолчанию 100)
- `offset` (опционально) - смещение для пагинации (по умолчанию 0)

**Пример запроса**:
```
GET /api/v1/todos
GET /api/v1/todos?completed=true
GET /api/v1/todos?limit=10&offset=20
```

**Пример ответа (200 OK)**:
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "Купить молоко",
      "description": "Сходить в магазин и купить молоко",
      "completed": false,
      "created_at": "2026-02-22T10:00:00Z",
      "updated_at": null
    },
    {
      "id": 2,
      "title": "Позвонить другу",
      "description": null,
      "completed": true,
      "created_at": "2026-02-22T09:30:00Z",
      "updated_at": "2026-02-22T09:45:00Z"
    }
  ],
  "count": 2
}
```

### 2. Получить задачу по ID

**GET** `/api/v1/todos/{id}`

**Описание**: Возвращает информацию о конкретной задаче по её ID

**Параметры пути**:
- `id` - уникальный идентификатор задачи (целое число)

**Пример запроса**:
```
GET /api/v1/todos/1
```

**Пример ответа (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Купить молоко",
    "description": "Сходить в магазин и купить молоко",
    "completed": false,
    "created_at": "2026-02-22T10:00:00Z",
    "updated_at": null
  }
}
```

**Ошибки**:
- 404 Not Found - задача с указанным ID не найдена

### 3. Создать новую задачу

**POST** `/api/v1/todos`

**Описание**: Создает новую задачу

**Тело запроса**:
```json
{
  "title": "string (обязательно)",
  "description": "string (опционально)"
}
```

**Пример запроса**:
```
POST /api/v1/todos
Content-Type: application/json

{
  "title": "Купить молоко",
  "description": "Сходить в магазин и купить молоко"
}
```

**Пример ответа (201 Created)**:
```json
{
  "status": "success",
  "data": {
    "id": 3,
    "title": "Купить молоко",
    "description": "Сходить в магазин и купить молоко",
    "completed": false,
    "created_at": "2026-02-22T10:15:00Z",
    "updated_at": null
  }
}
```

**Ошибки**:
- 400 Bad Request - неверный формат данных или отсутствуют обязательные поля

### 4. Обновить задачу

**PUT** `/api/v1/todos/{id}`

**Описание**: Обновляет информацию о задаче

**Параметры пути**:
- `id` - уникальный идентификатор задачи (целое число)

**Тело запроса**:
```json
{
  "title": "string (опционально)",
  "description": "string (опционально)",
  "completed": "boolean (опционально)"
}
```

**Пример запроса**:
```
PUT /api/v1/todos/1
Content-Type: application/json

{
  "title": "Купить молоко и хлеб",
  "completed": true
}
```

**Пример ответа (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Купить молоко и хлеб",
    "description": "Сходить в магазин и купить молоко",
    "completed": true,
    "created_at": "2026-02-22T10:00:00Z",
    "updated_at": "2026-02-22T10:20:00Z"
  }
}
```

**Ошибки**:
- 404 Not Found - задача с указанным ID не найдена
- 400 Bad Request - неверный формат данных

### 5. Удалить задачу

**DELETE** `/api/v1/todos/{id}`

**Описание**: Удаляет задачу по её ID

**Параметры пути**:
- `id` - уникальный идентификатор задачи (целое число)

**Пример запроса**:
```
DELETE /api/v1/todos/1
```

**Пример ответа (200 OK)**:
```json
{
  "status": "success",
  "message": "Задача успешно удалена"
}
```

**Ошибки**:
- 404 Not Found - задача с указанным ID не найдена

## Форматы ошибок

Все ошибки возвращаются в следующем формате:

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Описание ошибки"
  }
}
```

Примеры:
```json
{
  "status": "error",
  "error": {
    "code": "TODO_NOT_FOUND",
    "message": "Задача с указанным ID не найдена"
  }
}
```

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Поле 'title' обязательно для заполнения"
  }
}