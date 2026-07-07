import pandas as pd
import psycopg2
import json
from datetime import datetime


def load_excel_to_postgres():
    with open('../connection.json', 'r', encoding='utf-8') as file:
        db_params = json.load(file)['postgre']

    excel_file = 'Выборка.xlsx'
    df = pd.read_excel(excel_file, sheet_name='Sheet1')

    if 'DT_TASK_ROLL' in df.columns:
        df['DT_TASK_ROLL'] = pd.to_datetime(df['DT_TASK_ROLL']).dt.date

    try:
        conn = psycopg2.connect(
            host=db_params['host'],
            port=db_params['port'],
            dbname=db_params['dbname'],
            user=db_params['user'],
            password=db_params['password']
        )
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE rolling_task")

        # Вставка данных
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO rolling_task (
                    DT_TASK_ROLL, TASK_POS, ORDERS, ORD_POS, GRADE_CODE, GRADE_NAME,
                    PLATE_T, PLATE_W, PLATE_L, GOST_TT, GOST_XA, GOST_SORT,
                    HEAT, NUM_1, CNT_P, NUM_N, BATCH, INBATCH, KDUP
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                row['DT_TASK_ROLL'], row['TASK_POS'], row['ORDERS'], row['ORD_POS'],
                row['GRADE_CODE'], row['GRADE_NAME'], row['PLATE_T'], row['PLATE_W'],
                row['PLATE_L'], row['GOST_TT'], row['GOST_XA'], row['GOST_SORT'],
                row['HEAT'], row['NUM_1'], row['CNT_P'], row['NUM_N'], row['BATCH'],
                row['INBATCH'] if pd.notna(row['INBATCH']) else None,
                row['KDUP']
            ))

        conn.commit()
        print(f"Успешно загружено {len(df)} записей в таблицу rolling_task")

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    load_excel_to_postgres()