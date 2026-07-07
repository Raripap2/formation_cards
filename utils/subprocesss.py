import json
import signal
import sys

from utils.db_utils import Sheets, Workers, FormationCards, RollingTask

with open('connection.json', 'r',
          encoding='utf-8') as connection_file:  # получение данных для подключения к БД
    postgre_db = json.load(connection_file)['postgre']

workers_db = Workers.WorkersDB(conn_params=postgre_db)
sheets_db = Sheets.SheetsDB(conn_params=postgre_db)
rolling_task_db = RollingTask.RollingTaskDB(conn_params=postgre_db)
formation_cards_db = FormationCards.FormationCardsDB(conn_params=postgre_db)


def cleanup():
    pass


def handle_shutdown(signum, frame):
    print(f"\nПолучен сигнал {signum}, завершение...")
    cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_shutdown)  # обработчик завершения работы
signal.signal(signal.SIGTERM, handle_shutdown)
