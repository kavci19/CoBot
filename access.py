# GS Quant documentation available at:
# https://developer.gs.com/docs/gsquant/guides/getting-started/
import db
import datetime
from datetime import date
import json
import os
import smtplib
from email.message import EmailMessage
import heapq

from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

GsSession.use(Environment.PROD, 'b16a94fab7714a61b29065f6d6bda51b', '2179ad8fec38bbe8995f4d07293f9b476476dbef67b99f3a4074099de3fff049', ('read_product_data',))

ds = Dataset('COVID19_COUNTRY_DAILY_WHO')
today = date.today()
countries = ds.get_data(today)[['countryName', 'countryId']].drop_duplicates()
country_id_name_dict = {}
for index, row in countries.iterrows():
    country_id_name_dict[row['countryId']] = row['countryName']


def get_country_with_largest_total_deaths(data):
    jsonified_data = json.loads(data.to_json(orient="table"))["data"]
    max_total_deaths = float("-inf")
    country_info = None
    for entry in jsonified_data:
        current_total_fatalities = entry["totalFatalities"]
        if current_total_fatalities >= max_total_deaths:
            max_total_deaths = current_total_fatalities
            country_info = entry
    country_name = country_info['countryName']
    print(f"{country_name} is the country with the most total deaths.\nTotal deaths: {max_total_deaths}")
    return f"{country_name} is the country with the most total deaths.\nTotal deaths: {max_total_deaths}\n"


def get_country_with_largest_total_confirmed_cases(data):
    jsonified_data = json.loads(data.to_json(orient="table"))["data"]
    max_confirmed_cases = float("-inf")
    country_info = None
    for entry in jsonified_data:
        current_confirmed_cases = entry["totalConfirmed"]
        if current_confirmed_cases >= max_confirmed_cases:
            max_confirmed_cases = current_confirmed_cases
            country_info = entry
    country_name = country_info['countryName']
    print(f"{country_name} is the country with the most confirmed cases\nconfirmed cases: {max_confirmed_cases}")
    return f"{country_name} is the country with the most confirmed cases\nconfirmed cases: {max_confirmed_cases}\n"

test_data = ds.get_data(datetime.date(2020, 1, 21), limit=1)

def create_email_string(test_data):
    email_string = ""
    email_string += get_country_with_largest_total_deaths(test_data)
    email_string += get_country_with_largest_total_confirmed_cases(test_data)
    return email_string


def send_client_email(email_string, decision_table):
    EMAIL_ADDRESS = "cothebot@gmail.com"
    EMAIL_PASSWORD = "HiImCo!!"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, "cothebot@gmail.com", email_string)
    server.quit()


def get_new_daily_record_confirmed():
    return_countries = []
    country_ids = list(country_id_name_dict.keys())
    for country in country_ids:
        highest_confirmed = ds.get_data(datetime.date(2020, 1, 21), countryId=[country])['newConfirmed'].max()
        today_confirmed = ds.get_data(datetime.date(2020, 12, 11), countryId=[country])[['newConfirmed']]
        if highest_confirmed == today_confirmed['newConfirmed'].values[0]:
            return_countries.append(country_id_name_dict[country])
    if len(return_countries) == 0:
        return None
    elif len(return_countries) == 1:
        message = return_countries[0] + ' has reached a new record of daily COVID-19 confirmed cases.'
    else:
        message = 'The following countries have reached a new record of daily COVID-19 confirmed cases: ' + ', '.join(return_countries) + '.'
    return message


def get_new_daily_record_fatalities():
    return_countries = []
    country_ids = list(country_id_name_dict.keys())
    for country in country_ids:
        highest_fatalities = ds.get_data(datetime.date(2020, 1, 21), countryId=[country])['newFatalities'].max()
        today_fatalities= ds.get_data(today, countryId=[country])[['newFatalities']]
        if highest_fatalities == today_fatalities['newFatalities'].values[0]:
            return_countries.append(country_id_name_dict[country])
    if len(return_countries) == 0:
        return None
    elif len(return_countries) == 1:
        message = return_countries[0] + ' has reached a new record of daily COVID-19 death cases.'
    else:
        message = 'The following countries have reached a new record of daily COVID-19 death cases: ' + ', '.join(return_countries) + '.'
    return message


def get_top_5_daily_new_confirmed():
    new_confirmed = ds.get_data(today)[['countryId', 'newConfirmed']]
    new_confirmed = new_confirmed.nlargest(5, 'newConfirmed')
    return_countries = [country_id_name_dict[country] for country in new_confirmed['countryId'].values]
    message = 'The top 5 countries who have the highest number of new confirmed cases today are: ' + ', '.join(return_countries) + '.'
    return message


def get_top_5_daily_new_fatalities():
    new_fatalities = ds.get_data(today)[['countryId', 'newFatalities']]
    new_fatalities = new_fatalities.nlargest(5, 'newFatalities')
    return_countries = [country_id_name_dict[country] for country in new_fatalities['countryId'].values]
    message = '''The top 5 countries who have the highest number of new death cases today are: ''' + ', '.join(return_countries) + '.'
    return message


<<<<<<< HEAD
# get_country_with_largest_total_confirmed_cases(test_data)
# send_client_email(create_email_string(), [{'email': 'cothecovidbot@gmail.com', 'record_confirmed': False, 'record_fatalities': True, 'top_5_most_confirmed': False, 'top_5_most_fatalities': False,
#                                            'population_pct': False, 'top_5_least_confirmed': False, 'top_5_least_fatalities': True, 'total_fatalities_highest': False, 'total_confirmed_highest': False, 'notification_time': None}])
=======
# functionality: computes the countries with the most/least amount of daily new deaths/infected in a given region (if
# supplied)
# N = amount of countries to be returned
# queryType = newConfirmed or newFatalities
# region = region of the world to query (Americas, Southeast Asia, etc.)
# order = least or greatest

def get_daily_new(N, queryType, region=None, order='least'):

    region_to_key = {'Americas': 'AMRO',
                     'Eastern Mediterranean': 'EMRO',
                     'Western Pacific': 'WPRO',
                     'Southeast Asia': 'SEARO'}

    date = str(datetime.datetime.now()).split()[0].split('-')

    ds = Dataset('COVID19_COUNTRY_DAILY_WHO')

    if order == 'least':
        multiplier = -1
    else:
        multiplier = 1

    if region:
        if region not in region_to_key:
            regionId = 'Other'
        else:
            regionId = region_to_key[region]

    if region is None:
        data = ds.get_data(datetime.date(int(date[0]), int(date[1]), int(date[2])), limit=2)
    else:
        data = ds.get_data(datetime.date(int(date[0]), int(date[1]), int(date[2])), regionName=regionId, limit=2)

    cases = data[queryType]
    country = data['countryName']

    heap = []

    for i in range(len(cases)):
        heapq.heappush(heap, (multiplier * cases[i], country[i]))
        if len(heap) > N:
            heapq.heappop(heap)

    heap.sort(key=lambda x: x[0])

    if queryType == 'newConfirmed':
        word = 'cases'
    else:
        word = 'deaths'

    regionWord = ''
    if region is not None:
        regionWord = ' in ' + region

    result = 'The ' + str(N) + ' countries with the ' + order + ' daily new ' + word + regionWord + ' are:\n'

    for entry in heap:
        result += str(entry[1]) + ': ' + str(int(abs(entry[0]))) + '\n'

    return result




test_data = ds.get_data(datetime.date(2020, 1, 21), limit=1)
get_country_with_largest_total_confirmed_cases(test_data)
send_client_email(create_email_string(test_data), [{'email': 'cothebot@gmail.com', 'record_confirmed': False, 'record_fatalities': True, 'top_5_most_confirmed': False, 'top_5_most_fatalities': False,
                                           'population_pct': False, 'top_5_least_confirmed': False, 'top_5_least_fatalities': True, 'total_fatalities_highest': False, 'total_confirmed_highest': False, 'notification_time': None}])
>>>>>>> d9bbab73a3dd4af40078cd77811f3b2a5e86bc65
