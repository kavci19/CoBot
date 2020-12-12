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
    top_5_most_confirmed, top_5_most_fatalities,
    top_5_least_confirmed, top_5_least_fatalities,
    total_fatalities_highest, total_confirmed_highest, notification_time):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO USER (email, record_confirmed, record_fatalities,
            top_5_most_confirmed, top_5_most_fatalities,
            top_5_least_confirmed, top_5_least_fatalities,
            total_fatalities_highest, total_confirmed_highest, notification_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (email, record_confirmed, record_fatalities,
            top_5_most_confirmed, top_5_most_fatalities,
            top_5_least_confirmed, top_5_least_fatalities,
            total_fatalities_highest, total_confirmed_highest, notification_time))
        conn.commit()
        return None
    except pymysql.Error as e:
        return e
