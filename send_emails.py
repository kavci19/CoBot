import db
import access
import datetime
from datetime import date
import smtplib
import yagmail
from gs_quant.session import GsSession, Environment
import pandas as pd

GsSession.use(Environment.PROD, 'b16a94fab7714a61b29065f6d6bda51b', '2179ad8fec38bbe8995f4d07293f9b476476dbef67b99f3a4074099de3fff049', ('read_product_data',))
EMAIL_ADDRESS = "cothebot@gmail.com"
EMAIL_PASSWORD = "HiImCo!!"

yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
today = date.today()

def get_users():
    try:
        conn = db.get_db_conn(outside_flask=True)
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM USER'
        )
        rows = cur.fetchall()
        if rows is None:
            return [], None
        user_list = []
        for row in rows:
            user_list.append({
                    'email': row[0],
                    'record_confirmed': row[1] == 1,
                    'record_fatalities': row[2] == 1,
                    'top_5_most_confirmed': row[3] == 1,
                    'top_5_most_fatalities': row[4] == 1,
                    'top_5_least_confirmed': row[5] == 1,
                    'top_5_least_fatalities': row[6] == 1,
                    'total_fatalities_highest': row[7] == 1,
                    'total_confirmed_highest': row[8] == 1,
                    'notification_time': row[9],
            })
        return user_list, None
    except pymysql.Error as e:
        return None, e
    finally:
        conn.close()


def create_emails():
    user_list, err = get_users()
    # record_confirmed = access.get_new_daily_record_confirmed('newConfirmed')
    # record_fatalities = access.get_new_daily_record_confirmed('newFatalities')
    top_5_most_confirmed_str, top_5_most_confirmed_df = access.get_top_n_countries(5, 'newConfirmed', None, 'most')
    top_5_most_fatalities_str, top_5_most_fatalities_df = access.get_top_n_countries(5, 'newFatalities', None, 'most')
    top_5_least_confirmed_str, top_5_least_confirmed_df = access.get_top_n_countries(5, 'newConfirmed', None, 'least')
    top_5_least_fatalities_str, top_5_least_fatalities_df = access.get_top_n_countries(5, 'newFatalities', None, 'least')
    total_confirmed_highest = access.get_top_n_countries(1, 'totalConfirmed', None, 'most')
    total_fatalities_highest = access.get_top_n_countries(1, 'totalFatalities', None, 'most')
    if err:
        return str(err)
    for user in user_list:
        email_string = """Hi here! It's Co!
        Here is your daily summary of global COVID-19 statistics for """
        email_string += str(today) + ': ' + '\n' + '\n'
        email = user['email']
        info_string = [email_string]
        # if user['record_confirmed']:
        #     info_string.append(record_confirmed)
        #     info_string.append('\n')
        # if user['record_fatalities']:
        #     info_string.append(record_fatalities)
        #     info_string.append('\n')
        if user['top_5_most_confirmed']:
            info_string.append(top_5_most_confirmed_str)
            info_string.append(top_5_most_confirmed_df)
            info_string.append('\n')
        if user['top_5_most_fatalities']:
            info_string.append(top_5_most_fatalities_str)
            info_string.append(top_5_most_fatalities_df)
            info_string.append('\n')
        if user['top_5_least_confirmed']:
            info_string.append(top_5_least_confirmed_str)
            info_string.append(top_5_least_confirmed_df)
            info_string.append('\n')
        if user['top_5_least_fatalities']:
            info_string.append(top_5_least_fatalities_str)
            info_string.append(top_5_least_fatalities_df)
            info_string.append('\n')
        if user['total_fatalities_highest']:
            info_string.append(total_fatalities_highest)
            info_string.append('\n')
        if user['total_confirmed_highest']:
            info_string.append(total_confirmed_highest)
            info_string.append('\n')
        info_string.append('Stay safe and healthy!')
        info_string.append(yagmail.inline('co1.png'))
        yag.send(email, 'Daily COVID-19 Report by Co', info_string)

create_emails()
