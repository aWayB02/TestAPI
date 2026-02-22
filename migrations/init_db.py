#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных.
Создает необходимые таблицы в базе данных SQLite.
"""

from database.db import init_database, engine, Base, TodoDB
from sqlalchemy import text
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    """Создание таблиц в базе данных"""
    logger.info("Создание таблиц в базе данных...")
    try:
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)
        logger.info("Таблицы успешно созданы")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        raise


def check_tables():
    """Проверка существующих таблиц"""
    logger.info("Проверка существующих таблиц...")
    try:
        # Получение списка таблиц
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table';")
            )
            tables = [row[0] for row in result]
            logger.info(f"Существующие таблицы: {tables}")
    except Exception as e:
        logger.error(f"Ошибка при проверке таблиц: {e}")
        raise


def main():
    """Основная функция инициализации базы данных"""
    logger.info("Начало инициализации базы данных")

    try:
        # Создание таблиц
        create_tables()

        # Проверка таблиц
        check_tables()

        logger.info("Инициализация базы данных завершена успешно")
        print("База данных успешно инициализирована!")

    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        print(f"Ошибка: {e}")
        raise


if __name__ == "__main__":
    main()
