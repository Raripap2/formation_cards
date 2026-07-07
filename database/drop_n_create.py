import json
import random
import uuid
from datetime import datetime, timedelta

import psycopg2

queries = ["""
DO

$$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END

$$;

CREATE TABLE formation_cards (
    card_id INT PRIMARY KEY, 
    order_id BIGINT,
    way TEXT,
    closed BOOLEAN,
    deleted BOOLEAN   
);

CREATE TABLE formation_cards_info (
    card_id INT PRIMARY KEY,
    fc_gost_tt TEXT,
    fc_gost_xa TEXT,
    fc_gost_sort TEXT,
    shipment_date DATE,
    wagon_num INT,
    batch INT,
    grade TEXT,
    group_num INT,
    certificate TEXT,
    position TEXT,
    created_date TIMESTAMP WITHOUT TIME ZONE,
    FOREIGN KEY (card_id) REFERENCES formation_cards(card_id)
);

CREATE TABLE sheets_info (
    sheet_id TEXT PRIMARY KEY,
    marking_time TIMESTAMP WITHOUT TIME ZONE,
    sb_order BIGINT, 
    cut_part_num INT,
    heat TEXT,
    batch INT,
    tech_violation_code INT,
    num_1 INT,
    grade TEXT,
    carb_eqiv TEXT,
    crack_resist TEXT,
    plate_t NUMERIC,
    plate_w NUMERIC,
    plate_l NUMERIC,
    departed BOOLEAN,
    order_fk INT
);

CREATE TABLE sheets (
    sheet_id TEXT, 
    card_id INT,
    PRIMARY KEY (sheet_id, card_id),
    FOREIGN KEY (card_id) REFERENCES formation_cards(card_id),
    FOREIGN KEY (sheet_id) REFERENCES sheets_info(sheet_id)
);

CREATE TABLE logs (
    log_id SERIAL PRIMARY KEY,
    worker_id INT,
    log_date TIMESTAMP WITHOUT TIME ZONE,
    log_message TEXT,
    log_action INT
);

CREATE TABLE rolling_task (
    DT_TASK_ROLL DATE,
    TASK_POS INT,
    ORDERS BIGINT, 
    ORD_POS INT,
    GRADE_CODE INT,
    GRADE_NAME TEXT,
    PLATE_T NUMERIC,
    PLATE_W NUMERIC,
    PLATE_L NUMERIC,
    GOST_TT TEXT,
    GOST_XA TEXT,
    GOST_SORT TEXT,
    HEAT TEXT, 
    NUM_1 INT, 
    CNT_P INT, 
    NUM_N INT, 
    BATCH INT, 
    INBATCH INT, 
    KDUP INT
);

CREATE TABLE fac_sheets (
    sheet_id TEXT,
    marking_time TIMESTAMP WITHOUT TIME ZONE,
    sb_order BIGINT, 
    cut_part_num INT,
    heat TEXT,
    batch INT,
    tech_violation_code INT,
    num_1 INT,
    grade TEXT,
    carb_eqiv TEXT,
    crack_resist TEXT,
    plate_t NUMERIC,
    plate_w NUMERIC,
    plate_l NUMERIC,
    order_fk INT
);

CREATE TABLE statuses(
    status_id INT PRIMARY KEY NOT NULL,
    status_name TEXT
);

CREATE TABLE fac_workers_info (
    worker_id INT PRIMARY KEY NOT NULL,
    firstname TEXT,
    lastname TEXT,
    secondname TEXT,
    shift INT, 
    brigade INT
);

CREATE TABLE fac_workers(
    worker_id INT PRIMARY KEY NOT NULL,
    login TEXT,
    hash_password TEXT,
    status_id INT NOT NULL,
    FOREIGN KEY (worker_id) REFERENCES fac_workers_info(worker_id),
    FOREIGN KEY (status_id) REFERENCES statuses(status_id)
);

INSERT INTO statuses VALUES
(0, 'Режим бога'),
(1, 'Руководитель'),
(2, 'Оператор'),
(3, 'Гость'),
(4, 'Модератор пользователей');

INSERT INTO fac_workers_info VALUES
(1, 'System', NULL, NULL, NULL, NULL),
(2, 'MISIS','Advance','Team', 0, 0);

INSERT INTO fac_workers VALUES
(1, NULL, NULL, 0),
(2, 'admin', '10ff439a1a73af22f3af7675aae5a95487565a918b102a0851ff7a6fb47ec6bd', 0);
"""]

"""
Роли:
    1 - 'Руководитель' (Просмотр логов; Просмотр пользователей; Полномочия 3)
    2 - 'Оператор' (Создание, редактирование, закрытие ФК; Добавление/удаление листов в/из ФК; Редактирование параметров листов; Полномочия 3)
    3 - 'Гость' (Просмотр ФК)

Специальные Роли:
    0 - 'Режим бога' (Редактирование параметров системы?)
    4 - 'Модератор пользователей' (Просмотр, создание, удаление, редактирование пользователей)

События в логах:
    1 - Создание ФК
    2 - Редактирование ФК
    3 - Закрытие ФК
    4 - Добавление листа
    5 - Привязка листа к ФК
    6 - Отвязка листа к ФК
"""


def random_bd(cursor, num_cards=10, num_sheets=50):
    """
    Генерирует случайные данные для карт формирования и листов.
    """
    print(f"Генерация {num_sheets} листов и {num_cards} карт формирования...")

    # Варианты марок стали для реалистичности
    grades = ['09Г2С', 'Ст3сп', '10ХСНД', '11ЮА', 'K-60D']
    t = [10, 11.5, 12]
    # 2. Генерируем листы для sheets_info, fac_sheets и связи в sheets
    for _ in range(num_sheets):

        # Случайное время за последние 30 дней
        marking_time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23),
                                                  minutes=random.randint(0, 59))
        sb_order = random.randint(1000000, 9999999)
        cut_part_num = random.randint(1, 5)
        heat = f"{random.choice('ZV')}{random.randint(1000, 9999)}"
        batch = random.randint(1, 100)
        tech_violation_code = random.choice([0, 0, 0, 1, 2, 5])  # Чаще 0 (нет нарушений)
        num_1 = random.randint(1, 50)
        grade = random.choice(grades)
        carb_eqiv = f"{random.uniform(0.3, 0.5):.2f}"
        crack_resist = f"{random.uniform(1.0, 4.0):.2f}"
        plate_t = t[random.randint(0,2)]
        plate_w = round(random.uniform(1000.0, 2500.0), 2)
        plate_l = round(random.uniform(4000.0, 12000.0), 2)
        departed = random.choice([True, False])
        sheet_id = str(heat + str(round(random.randint(1,20))))
        # Заполняем sheets_info (основная таблица листов)
        cursor.execute("""
            INSERT INTO sheets_info 
            (sheet_id, marking_time, sb_order, cut_part_num, heat, batch, tech_violation_code, 
             num_1, grade, carb_eqiv, crack_resist, plate_t, plate_w, plate_l, departed, order_fk)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
        """, (sheet_id, marking_time, sb_order, cut_part_num, heat, batch, tech_violation_code,
              num_1, grade, carb_eqiv, crack_resist, plate_t, plate_w, plate_l, departed))

        # Заполняем fac_sheets (предположим, что здесь находятся 50% листов, которые сейчас в цеху)
        if random.choice([True, False]):
            cursor.execute("""
                INSERT INTO fac_sheets 
                (sheet_id, marking_time, sb_order, cut_part_num, heat, batch, tech_violation_code, 
                 num_1, grade, carb_eqiv, crack_resist, plate_t, plate_w, plate_l, order_fk)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
            """, (sheet_id, marking_time, sb_order, cut_part_num, heat, batch, tech_violation_code,
                  num_1, grade, carb_eqiv, crack_resist, plate_t, plate_w, plate_l))



def create_db():
    with open('../connection.json', 'r', encoding='utf-8') as file:
        connect_params = json.load(file)['postgre']
        try:
            connection = psycopg2.connect(
                host=connect_params['host'],
                port=connect_params['port'],
                dbname=connect_params['dbname'],
                user=connect_params['user'],
                password=connect_params['password']
            )
            cursor = connection.cursor()

            # 1. Создаем структуру БД
            for query in queries:
                cursor.execute(query)
            connection.commit()
            print("Таблицы успешно созданы.")

            # 2. Вызываем функцию заполнения рандомными данными
            random_bd(cursor, num_cards=15, num_sheets=100)
            connection.commit()
            print("Случайные данные успешно добавлены.")

        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()  # Откат транзакции при ошибке

        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'connection' in locals() and connection is not None:
                connection.close()


if __name__ == '__main__':
    create_db()