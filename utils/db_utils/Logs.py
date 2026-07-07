import datetime
import json
from typing import Dict, List, Optional

from utils.db_classes import Database


class LogsDB(Database):
    """класс для логирования"""

    def add_log(
            self,
            worker_id: int,
            message: str,
            log_action: int) -> None:
        """
        Логирует действие в таблицу logs.

        Параметры:
            worker_id: ID сотрудника, выполнившего действие.
            message: Сообщение для лога.
            log_action: Событие
                11 - Создание ФК;
                12 - Редактирование ФК;
                13 - Закрытие ФК;
                14 - Привязка листа;
                15 - Отвязка Листа;

                21 - Добавление листа;
                22 - Удаление листа;

                31 - Создание пользователя
                32 - Редактирование пользователя
                33 - Удаление пользователя
        """
        date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = """
            INSERT INTO logs(worker_id, log_date, log_message, log_action)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self._execute_query_without_result(query, worker_id, date_now, message, log_action)

    def get_filtered_logs(self,
                          filters: Optional[Dict] = None,
                          page_number: int = 1,
                          page_size: int = 10,
                          order_by: str = "log_date",
                          order_direction: str = "DESC") -> List[Dict[str, str]]:
        """
        Получает записи из таблицы logs с фильтрацией по указанным полям и пагинацией.

        Параметры:
            filters: Словарь с фильтрами (ключ - название поля, значение - значение для фильтра).
            page_number: Номер страницы (начинается с 1).
            page_size: Количество записей на странице.
            order_by: Поле для сортировки.
            order_direction: Направление сортировки (ASC или DESC).

        Поля для фильтра:
        log_id: INT
        card_id: INT
        act_id: INT
        worker_id: INT
        sheet_id: STR
        log_date: TIMESTAMP WITHOUT TIME ZONE

        Возвращает:
            Список с записями из таблицы logs.

        Пример использования:
        filters = {
            "card_id": 123,
            "worker_id": 456
        }
        logs = get_filtered_logs(
            filters=filters,
            page_number=2,
            page_size=10,
            order_by="log_date",
            order_direction="DESC"
        )
        """
        if filters is None:
            filters = {}

        # Формирование SQL-запроса
        query = "SELECT * FROM logs"
        filered_query = self._filter(filters, order_by, order_direction, page_size, page_number)
        query += filered_query[0]
        params = filered_query[1]

        # Выполнение запроса
        return self._execute_query_with_result(query, *params)