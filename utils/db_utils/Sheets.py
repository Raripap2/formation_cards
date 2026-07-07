from typing import Optional

from utils.db_classes import Database


class SheetsDB(Database):
    """
    Класс для работы с БД листов

    Переменные:
        sheet_ids: list[str] - Массив ID листов
        worker_id: int - ID пользователя
        fields: Optional[list[str]] - Список названий требуемых полей
        filters: dict - Фильтры для селекта
        order_by: str - Группировка по (название поля)
        order_direction: str - Направление группировки
        page_size: int - Количество строк в селекте
        page_number: int - Страница селекта
    """

    def transfer_sheet(self, sheet_ids: list[str], worker_id: int = None): #Не реализовано
        """Добавляет в таблицу sheets_info лист/листы по ID"""
        pass


    def delete(self, sheet_ids: list[str], worker_id: int = None):
        """Удаляет из таблицы sheets лист/листы по ID"""
        if not worker_id:
            worker_id = 1

        for sheet in sheet_ids:
            self._execute_query_without_result('DELETE FROM sheets WHERE sheet_id = %s', sheet)

    def get(self, sheet_ids: list[str], fields: Optional[list[str]] = None) -> dict | list[dict]:
        """
        Получение данных по листам

        Параметры:
            sheet_ids: ID одного листа или список нескольких
            fields: назнавие полей необходимых данных
                sheet_id: ID листа
                marking_time: Время маркировки
                sb_order: Заказ
                cut_part_num: Номер части при порезки на Дел. нижницах
                heat: Плавка
                batch: Партия
                tech_violation_code: Код нарушения технологии
                num_1: Номер листа
                grade: Марка
                carb_eqiv: Углеродный эквивалент
                crack_resist: Коэф. трещиностойкости
                plate_t: Толщина
                plate_w: Ширина
                plate_l: Длина

        Возвращает cписок словарей по нескольким
        """

        def find_sheet(param, sheet_id):  # Получение данных по ID листа
            if not param:
                param = self.fields['fac_sheets']
                data = self._execute_query_with_result('SELECT * FROM sheets_info WHERE sheet_id = %s',
                                                       sheet_id)
            else:
                data = self._execute_query_with_result(
                    f"SELECT {', '.join(param)} FROM sheets_info WHERE sheet_id = %s", sheet_id)

            return param, data

        result = []
        for ii in range(len(sheet_ids)):
            sheet_params, sheet_data = find_sheet(fields, sheet_ids[ii])
            result.append({sheet_params[i]: sheet_data[ii][i] for i in range(len(sheet_params))})
        return result

    def get_with_filters(self, filters: dict, order_by: str, order_direction: str, page_size: int, page_number: int,
                         fields: Optional[list[str]] = None):
        """
        Поиск по фильтрам

        Для фильтрации по датам в значении фильтра указывать дату начала и конца в кортеже 'date': ('2000-01-01', '2002-02-02')
        Если необходимо фильтровать по конкретной дате, то ее указывать в кортеже два раза 'date': ('2000-01-01', '2000-01-01')

        Параметры:
            fields: Поля БД которые функция вернет. Если передана строка "all" функция вернет все поля.
            filters: Словарь фильтров для поиска.
            order_by: Поле по которому проводится сортировка.
            order_direction: Направление сортировки.
            page_size: Количество строк в странице.
            page_number: Номер страницы.

        Возвращает массив словарей с найденными данными
        """

        if not fields:
            query = "SELECT * FROM sheets_info"
            fields = self.fields['fac_sheets']
        else:
            query = f"SELECT {', '.join(fields)} FROM sheets_info WHERE order_fk = 0"

        filered_query = self._filter(filters, order_by, order_direction, page_size, page_number)
        query += filered_query[0]
        params = filered_query[1]

        # Выполнение запроса
        data = self._execute_query_with_result(query, *params)
        return [{fields[j]: data[i][j] for j in range(len(data[i]))} for i in range(len(data))]
