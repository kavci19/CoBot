import pymysql
from flask import g
import datetime

HOST_ADDRESS = 'gs-hackathon.c0bqqwmr6qnn.us-east-1.rds.amazonaws.com'
PORT = 3306
USER = 'admin'
PASSWORD = 'Gsh1211!'
DB_NAME = 'GSHDB'

def get_db_conn(outside_flask=False):
    if not outside_flask and 'db_conn' in g:
        return g.db_conn
    conn = pymysql.connect(
            host=HOST_ADDRESS,
            port=PORT,
            user=USER,
            password=PASSWORD,
            db=DB_NAME)
    if outside_flask:
        return conn
    else:
        g.db_conn = conn
        return g.db_conn


def close_db(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def register_user(email, record_confirmed, record_fatalities,
top_5_most_confirmed, top_5_most_fatalities, population_pct,
top_5_least_confirmed, top_5_least_fatalities,
total_fatalities_highest, total_confirmed_highest, notification_time):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO USER (email, record_confirmed, record_fatalities,
            top_5_most_confirmed, top_5_most_fatalities,
            population_pct, top_5_least_confirmed, top_5_least_fatalities,
            total_fatalities_highest, total_confirmed_highest, notification_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (email, record_confirmed, record_fatalities,
            top_5_most_confirmed, top_5_most_fatalities,
            population_pct, top_5_least_confirmed, top_5_least_fatalities,
            total_fatalities_highest, total_confirmed_highest, notification_time))
        conn.commit()
        return None
    except pymysql.Error as e:
        return e


def get_users():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM USER'
        )
        rows = cur.fetchall()
        if rows is None:
            return [], None
        user_list = []
        for row in rows:
            item_list.append({
                    'email': row[0],
                    record_confirmed: row[1],
                    record_fatalities: row[2],
                    top_5_most_confirmed: row[3],
                    top_5_most_fatalities: row[4],
                    population_pct: row[5],
                    top_5_least_confirmed: row[6],
                    top_5_least_fatalities: row[7],
                    total_fatalities_highest: row[8],
                    total_confirmed_highest: row[9],
                    notification_time: row[10],
            })
        return item_list, None
    except pymysql.Error as e:
        return None, e
