import datetime
from typing import Optional, Dict

from utils.db_classes import Database


class FormationCardsDB(Database):
    """
    Класс для работы с БД Формировочных карточек

    Переменные:
        card_id: int - ID фк
        fields: Optional[list[str]] - Список названий требуемых полей
        order_id: str - Номер заказа
        way: str - Направление карточки
        params: Dict - Параметры сущности (фк)
        sheet_id: str - ID листа
        filters: dict - Фильтры для селекта
        order_by: str - Группировка по (название поля)
        order_direction: str - Направление группировки
        page_size: int - Количество строк в селекте
        page_number: int - Страница селекта
        join_: dict - (не испоьзовать)
        worker_id: int - ID пользователя
        message: str - Сообщение для логов (пока не используется)
    """

    def get_card(self, card_id: int, fields: Optional[list[str]] = None) -> dict | None:
        """
        Получение данных карточки по ее ID

        Параметры:
            card_id: ID карточки
            params: card_id, fc_gost_tt, fc_gost_xa, fc_gost_sort, shipment_date, wagon_num, batch, grade, group_num, certificate, position, created_date, order_id, way, closed, deleted

        Возвращает:
            Словарь с параметрами карточки. Если карточки не существует, вернет пустой словарь.
        """

        if not fields:
            fields = self.fields['formation_cards'] + self.fields['formation_cards_info'][1:]
            card = self._execute_query_with_result(
                f"SELECT {', '.join(fields)} FROM formation_cards JOIN formation_cards_info USING(card_id) WHERE card_id = %s",
                card_id)
        else:
            card = self._execute_query_with_result(
                f"SELECT {', '.join(fields)} FROM formation_cards "
                f"JOIN formation_cards_info USING(card_id) WHERE card_id = %s",
                card_id)

        if card:
            return dict([(fields[i], card[0][i]) for i in range(len(fields))])

        return {}

    def get_sheets_by_card(self, card_id: int, fields: list[str]) -> list[dict]:
        '''
        Получение привязанных к карточке листов

        Параметры:
            card_id: ID карточки
            fields: sheet_id, marking_time, sb_order, cut_part_num, heat, batch, tech_violation_code, num_1, grade, carb_eqiv, crack_resist, plate_t, plate_w, plate_l, departed, sheet_id, card_id

        Возвращает:
            Список словарей - всех прикрепленных листов
        '''
        return [
            {
                fields[i]: sheet[i]
                for i in range(len(fields))
            }
            for sheet in self._execute_query_with_result(
                f"SELECT {', '.join(fields)} FROM sheets JOIN sheets_info USING(sheet_id) WHERE card_id = %s",
                card_id
            )
        ]

    def create(self, order_id: str, way: str, params: Optional[Dict] = None, worker_id: int = None) -> int:
        """
        Создает карточку

        Параметры:
            order_id: Номер заказа
            way: Назначение карточки
            params: fc_gost_tt fc_gost_xa fc_gost_sort shipment_date wagon_num group_num certificate position
            worker_id

        Возвращает: ID созданной карточки
        """

        if not worker_id:
            worker_id = 1

        card_id = self._get_max_id('formation_cards', 'card_id') + 1

        self._execute_query_without_result('INSERT INTO formation_cards VALUES (%s, %s, %s, %s)',
                                           card_id, order_id, way, False)

        req = 'INSERT INTO formation_cards_info '
        insert_clauses = ['card_id']
        insert_params = [card_id]

        if params:  # распаковка параметров
            insert_clauses += list(params.keys())
            insert_params += list(params.values())

            insert_clauses.append('created_date')
            insert_params.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            req += f"({', '.join(insert_clauses)}) VALUES ({', '.join(['%s' for _ in range(len(insert_params))])})"

            self._execute_query_without_result(req, *insert_params)

        else:
            req += '(card_id) VALUES (%s)'
            self._execute_query_without_result(req, card_id)

        return card_id

    def edit(self, card_id: int, params: dict, worker_id: int = None, message: str = None):
        """
        Изменяет переданные параметры карточки

        Параметры:
            card_id: ID карточки
            params: fc_gost_tt fc_gost_xa fc_gost_sort shipment_date wagon_num group_num certificate position
            worker_id: ID пользователя
            message: Сообщение об изменении
        """
        if not worker_id:
            worker_id = 1

        fc_fields = self.fields['formation_cards']

        req_fci = 'UPDATE formation_cards_info SET '
        req_fc = 'UPDATE formation_cards SET '

        insert_clauses_fci = []
        insert_params_fci = []
        insert_clauses_fc = []
        insert_params_fc = []

        for field, value in params.items():
            if field in fc_fields:
                insert_clauses_fc.append(f"{field} = %s")  # распаковка параметров
                insert_params_fc.append(value)
            else:
                insert_clauses_fci.append(f"{field} = %s")  # распаковка параметров
                insert_params_fci.append(value)

        insert_params_fci.append(card_id)
        insert_params_fc.append(card_id)

        req_fci += ', '.join(insert_clauses_fci) + ' WHERE card_id = %s'
        req_fc += ', '.join(insert_clauses_fc) + ' WHERE card_id = %s'
        if insert_clauses_fc:
            self._execute_query_without_result(req_fc, *insert_params_fc)
        if insert_clauses_fci:
            self._execute_query_without_result(req_fci, *insert_params_fci)

    def add_sheet(self, card_id: int, sheet_ids: list, worker_id: int = None):
        """Привязка листа к карточке (поиск по ID листа)"""

        if not worker_id:
            worker_id = 1

        for i in sheet_ids:
            self._execute_query_without_result(f"INSERT INTO sheets VALUES "
                                               f"('{i}', {card_id})")
            self._execute_query_without_result(f"UPDATE sheets_info SET order_fk = %s WHERE sheet_id = %s ", 1, i)

    def delete_sheet(self, sheet_id: str, card_id: int, worker_id: int = None):
        """Отвязка листа от карточки"""

        if not worker_id:
            worker_id = 1

        self._execute_query_without_result('DELETE FROM sheets WHERE sheet_id = %s AND card_id = %s',
                                           sheet_id, card_id)

    def delete_sheets_by_card(self, card_id: int, worker_id: int = None):
        """отвязка всех листов от карточки (поиск по ID карточки)"""

        if not worker_id:
            worker_id = 1

        self._execute_query_without_result('DELETE FROM sheets WHERE card_id = %s',
                                           card_id)

    def close_card(self, card_id: int, worker_id: int = None):
        """Закрытие карточки"""

        if not worker_id:
            worker_id = 1

        self._execute_query_without_result('UPDATE formation_cards SET closed = TRUE WHERE card_id = %s',
                                           card_id)

    def delete(self, card_id: int, worker_id: int = None):
        """отвязка всех листов по карточке, полное удаление карточки"""

        if not worker_id:
            worker_id = 1

        self._execute_query_without_result('DELETE FROM formation_cards_info WHERE card_id = %s', card_id)
        self._execute_query_without_result('DELETE FROM formation_cards WHERE card_id = %s', card_id)

    def get_with_filters(self, fields: list[str], filters: dict, order_by: str,
                         order_direction: str, page_size: int, page_number: int, join_: dict = None):
        """
        Поиск по фильтрам

        Для фильтрации по датам в значении фильтра указывать дату начала и конца в кортеже 'date': ('2000-01-01', '2001-01-01')
        Если необходимо фильтровать по конкретной дате, то ее указывать в кортеже два раза 'date': ('2000-01-01', '2000-01-01')

        СТОИТ КОСТЫЛЬ:
        При использовании join совместно с fields = 'all' возникает проблема несовпадения ключей и
        значений. В текущем состоянии функция корректно возвращает данные только когда идет запрос по таблицам
        formation_cards и formation_cards_info. Без join селект проходит только по таблице formation_cards.
        Проблемы не будет в случае ввода требуемых полей вручную (указать все необходимые поля)

        Параметры:
            fields: Поля БД которые функция вернет. Если передана строка "all" функция вернет все поля.
            filters: Словарь фильтров для поиска. ЗНАЧЕНИЕ ДЛЯ ПОЛЕЙ ПЕРЕДАВАТЬ В ФОРМАТЕ СТРОКИ STR!!!!!
            order_by: Поле по которому проводится сортировка.
            order_direction: Направление сортировки.
            page_size: Количество строк в странице.
            page_number: Номер страницы.
            join: словарь со значениями для join в запросе: Таблица: Ключ. {'Таблица': 'Поле'}

        Возвращает массив словарей с найденными данными
        """

        if not fields:
            query = "SELECT * FROM formation_cards"
            fields = self.fields['formation_cards']
            if join_:
                for table in join_.keys():
                    fields += self.fields[table][1:]
        else:
            query = f"SELECT {', '.join(fields)} FROM formation_cards"

        if join_:  # словарь со значениями для join в запросе: Таблица: Ключ. {'Таблица': 'Поле'}
            for table, key in join_.items():
                query += f" JOIN {table} USING({key})"

        filered_query = self._filter(filters, order_by, order_direction, page_size, page_number)
        query += filered_query[0]
        params = filered_query[1]
        print(query)
        # Выполнение запроса
        data = self._execute_query_with_result(query, *params)
        return [{fields[j]: data[i][j] for j in range(len(data[i]))} for i in range(len(data))]
