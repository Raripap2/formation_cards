from typing import Optional, Dict

from utils.db_classes import Database


class WorkersDB(Database):
    """класс для работы с БД пользователей"""

    def create(self,
               login: str,
               hash_password: str,
               status_id: int,
               user_data: Optional[Dict] = None,
               worker_id: int = None) -> int:

        """
        Создает нового пользователя

        Параметры:
            login: Логин пользователя.
            hash_password: Хэш пароля пользователя.
            status: ID статуса пользователя.
            firstname: Имя пользователя.
            lastname: Фамилия Пользователя.
            secondname: Отчетсво пользователя.
            shift: Смена пользователя.
            brigade: Бригада пользователя.

        Возвращает: ID созданного пользователя.
        """

        if not worker_id:
            worker_id = 1

        if not all(field for field in [login, hash_password, status_id]):
            raise ValueError('Поля login, hash_password, status не должны содержать пустых значений.')

        if not status_id in range(0, 5):
            raise ValueError('Status должен находится в диапазоне 0 - 4')

        worker_id = self._get_max_id('fac_workers', 'worker_id') + 1

        fields = list(user_data.keys())
        values = list(user_data.values())
        req = f'INSERT INTO fac_workers_info(worker_id, {", ".join(fields)}) VALUES ({"%s, " * (len(values))} %s)'
        self._execute_query_without_result(req, * [worker_id] + values)

        self._execute_query_without_result('INSERT INTO fac_workers VALUES (%s, %s, %s, %s)',
                                           worker_id, login, hash_password, status_id)

        return worker_id

    def get(self,
            fields: list[str], order_by: str = None, order_direction: str = None, page_size: int = None,
            page_number: int = None, worker_id: int = None, filters: dict = None):
        """
        Возвращает: Словарь с данными о пользователе.

        В req и keys заменить 'status_name' на 'status_id' при необходимости. 'JOIN statuses' убрать
        """
        if worker_id and not filters:
            query = (f"SELECT {', '.join(fields)} FROM fac_workers JOIN fac_workers_info USING(worker_id) "
                     f"JOIN statuses USING(status_id) WHERE worker_id = %s")
            responce = self._execute_query_with_result(query, worker_id)
            if responce:
                responce = responce[0]
                return {fields[i]: responce[i] for i in range(len(fields))}
            return {}
        elif not worker_id and order_by and order_direction and page_size and page_number:
            query = (f"SELECT {', '.join(fields)} FROM fac_workers JOIN fac_workers_info USING(worker_id) "
                     f"JOIN statuses USING(status_id)")
            filered_query = self._filter(filters, order_by, order_direction, page_size, page_number)
            query += filered_query[0]
            params = filered_query[1]
            response = self._execute_query_with_result(query, *params)
            if response:
                return [{fields[j]: response[i][j] for j in range(len(fields))} for i in range(len(response))]
            return []
        else:
            raise AttributeError

    def find_by_login(self, login: str) -> tuple | None:
        """
        Возвращает:
            Если логин найден: ID пользователя и Хэш пароля
            Иначе: None
        """
        user = self._execute_query_with_result('SELECT worker_id, password FROM fac_workers WHERE login = %s',
                                               login)

        if user:
            return user[0]
        return None

    def edit(self, worker_id_to_edit: int, params: dict, login: str = None, hash_password: str = None,
             status_id: int = None, worker_id: int = None, message: str = None) -> None:
        """
        Обновляет переданные параметры пользователя

        Параметры:
            worker_id: ID пользователя
            login: Логин пользователя.
            password: Хэш пароля пользователя.
            status_id: ID статуса пользователя.
            params:
                firstname: Имя пользователя.
                lastname: Фамилия Пользователя.
                secondname: Отчетсво пользователя.
                shift: Смена пользователя.
                brigade: Бригада пользователя.
        """

        if not worker_id:
            worker_id = 1

        req = f"SELECT {', '.join(list(params.keys()))}"
        log_params = list(params)

        if login:
            req += 'login, '
            log_params.append('login')
        if hash_password:
            req += 'password, '
            log_params.append('password')
        if status_id:
            req += 'status_id, '
            log_params.append('status_id')

        req += f'FROM fac_workers JOIN fac_workers_info WHERE worker_id = %s'

        req = 'UPDATE fac_workers SET '
        update_clauses = []
        req_params = []

        if login:
            update_clauses.append('login = %s')
            req_params.append(login)
        if hash_password:
            update_clauses.append('password = %s')
            req_params.append(hash_password)
        if status_id:
            update_clauses.append('status_id = %s')
            req_params.append(status_id)

        if update_clauses:
            req += ', '.join(update_clauses) + ' WHERE worker_id = %s'
            req_params.append(worker_id_to_edit)
            self._execute_query_without_result(req, *req_params)

        req = 'UPDATE fac_workers_info SET '
        update_clauses = []
        req_params = []

        for field, value in params.items():
            if value:
                update_clauses.append(f"{field} = %s")
                req_params.append(value)

        req += ', '.join(update_clauses) + ' WHERE worker_id = %s'
        req_params.append(worker_id_to_edit)
        self._execute_query_without_result(req, *req_params)

    def delete(self, worker_id_to_delete: int, worker_id: int = None):
        """
        Полное удаление пользователя из системы.
        Для закрытия доступа для пользователя устанавливать login = None через edit_worker
        """

        if not worker_id:
            worker_id = 1

        req = ('DELETE FROM fac_workers WHERE worker_id = %s;'
               'DELETE FROM fac_workers_info WHERE worker_id = %s;')
        self._execute_query_without_result(req, worker_id_to_delete, worker_id_to_delete)
