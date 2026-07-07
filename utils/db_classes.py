import json

import psycopg2


class Database:
    """базовый класс для подключения к БД"""

    def __init__(self, logdb=None, conn_params=None):
        self.conn_params = conn_params
        self.logdb = logdb
        with open('db_fields.json', 'r', encoding='utf-8') as fields:
            self.fields = json.load(fields)

    def __repr__(self):
        print(*self.conn_params, sep='\n')

    def connect(self):
        connection = psycopg2.connect(**self.conn_params)  # подключение к БД
        cursor = connection.cursor()  # вызывать данный метод только внутри блока try
        return connection, cursor

    def _execute_query_with_result(self, query, *variables):  # выполнение 1 запроса к БД с результатом
        try:
            connection, cursor = self.connect()
            if variables:
                cursor.execute(query, variables)
            else:
                cursor.execute(query)
            connection.commit()
            result = cursor.fetchall()
            connection.close()
            return result

        except Exception as e:
            print(f"An error occurred: {e}")


    def _execute_query_without_result(self, query: str,
                                      *variables) -> None:  # выполнение 1 запроса к БД без результата
        try:
            connection, cursor = self.connect()
            if variables:
                cursor.execute(query, variables)
            else:
                cursor.execute(query)
            connection.commit()
            connection.close()

        except Exception as e:
            cursor.rollback
            print(f"An error occurred: {e}")


    def _filter(self, filters: dict, order_by: str, order_direction: str, page_size: int = None,
                page_number: int = None):
        where_clauses = []
        params = []
        query = ''

        # Добавление условий фильтрации
        if filters:
            for field, value in filters.items():
                if field in self.fields['dates']:
                    where_clauses.append(f"{field} BETWEEN %s AND %s")
                    params += list(value)
                else:
                    where_clauses.append(f"{field}::TEXT ILIKE %s")
                    params.append(f"%{value}%")

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # Добавление сортировки и пагинации
        if page_size and page_number:
            query += f" ORDER BY {order_by} {order_direction}"
            query += " LIMIT %s OFFSET %s"
            params.extend([page_size, (page_number - 1) * page_size])
        return query, params

    def _get_max_id(self, table: str, field: str):
        # Находит максимальный ID в указанной таблице
        id = self._execute_query_with_result(f'SELECT MAX({field}) FROM {table}')
        if id[0][0]:
            return id[0][0]
        return 0

    def _test(self):
        return self._execute_query_with_result('SELECT * FROM statuses')
