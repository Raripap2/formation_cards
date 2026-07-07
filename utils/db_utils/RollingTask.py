from typing import Optional

from utils.db_classes import Database


class RollingTaskDB(Database):
    """класс для работы с заданием на прокат"""

    def get_with_filters(self, filters: dict, order_by: str, order_direction: str, page_size: int, page_number: int,
                         fields: Optional[list[str]] = None):
        """
        Поиск по фильтрам

        Для фильтрации по датам в значении фильтра указывать дату начала и конца в кортеже 'date': ('2000-01-01', '2001-01-01')
        Если необходимо фильтровать по конкретной дате, то ее указывать в кортеже два раза 'date': ('2000-01-01', '2000-01-01')

        Параметры:
            fields: Поля БД которые функция вернет. Если передана строка "all" функция вернет все поля.
            filters: Словарь фильтров для поиска. ЗНАЧЕНИЕ ДЛЯ ПОЛЕЙ ПЕРЕДАВАТЬ В ФОРМАТЕ СТРОКИ STR!!!!!
            order_by: Поле по которому проводится сортировка.
            order_direction: Направление сортировки.
            page_size: Количество строк в странице.
            page_number: Номер страницы.


        Возвращает массив словарей с найденными данными
        """

        if fields == 'all':
            query = "SELECT * FROM rolling_task"
            fields = self.fields['rolling_task']
        else:
            query = f"SELECT {', '.join(fields)} FROM rolling_task"

        filered_query = self._filter(filters, order_by, order_direction, page_size, page_number)
        query += filered_query[0]
        params = filered_query[1]

        # Выполнение запроса
        data = self._execute_query_with_result(query, *params)
        return [{fields[j]: data[i][j] for j in range(len(data[i]))} for i in range(len(data))]
