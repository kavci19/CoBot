# GS Quant documentation available at:
# https://developer.gs.com/docs/gsquant/guides/getting-started/
import db
import datetime
from datetime import date
import json
import os
import pandas as pd
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


def get_new_daily_record_confirmed(queryType):
    return_countries = []
    country_ids = list(country_id_name_dict.keys())
    for country in country_ids:
        highest_confirmed = ds.get_data(datetime.date(2020, 1, 21), countryId=[country])[queryType].max()
        today_confirmed = ds.get_data(today, countryId=[country])[[queryType]]
        if highest_confirmed == today_confirmed[queryType].values[0]:
            return_countries.append(country_id_name_dict[country])
    if queryType == 'newConfirmed':
        word = 'confirmed cases'
    else:
        word = 'fatalities'
    if len(return_countries) == 0:
        return None
    elif len(return_countries) == 1:
        message = return_countries[0] + ' has reached a new record of daily ' + word + '.'
    else:
        message = 'The following countries have reached a new record of daily ' + word + ': ' + ', '.join(return_countries) + '.'
    return message


# functionality: computes the countries with the most/least amount of daily new deaths/infected in a given region (if
# supplied)
# N = amount of countries to be returned
# queryType = newConfirmed or newFatalities
# region = region of the world to query (Americas, Southeast Asia, etc.)
# order = least or greatest
def get_top_n_countries(N, queryType, region, order):
    region_to_key = {'Americas': 'AMRO',
                     'Eastern Mediterranean': 'EMRO',
                     'Western Pacific': 'WPRO',
                     'Southeast Asia': 'SEARO'}

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
        data = ds.get_data(today)
    else:
        data = ds.get_data(today, regionName=regionId)

    cases = data[queryType]
    country = data['countryName']

    heap = []

    for i in range(len(cases)):
        heapq.heappush(heap, (multiplier * cases[i], country[i]))
        if len(heap) > N:
            heapq.heappop(heap)

    heap.sort(key=lambda x: x[0])

    if queryType == 'newConfirmed':
        word = 'daily new confirmed cases '
    elif queryType == 'newFatalities':
        word = 'daily new fatalities '
    elif queryType == 'totalConfirmed':
        word = 'total confirmed cases '
    else:
        word = 'total fatalities '

    if region is not None:
        regionWord = ' in ' + region
    else:
        regionWord = ''

    result_dict = {'Country': [], 'Number of Cases': []}

    if order == 'most':
        adjective = 'highest number of '
        for entry in heap:
            result_dict['Country'].insert(0, str(entry[1]))
            result_dict['Number of Cases'].insert(0, str(int(abs(entry[0]))))
    else:
        adjective = 'lowest number of '
        for entry in heap:
            result_dict['Country'].append(str(entry[1]))
            result_dict['Number of Cases'].append(str(int(abs(entry[0]))))

    if N > 1:
        result = 'The top ' + str(N) + ' countries' + ' with the ' + adjective + word + regionWord + 'are:\n'
        return result, pd.DataFrame(result_dict)
    else:
        result = 'The country with the ' + adjective + word + regionWord + 'is: ' + result_dict['Country'][0] + ' with ' + result_dict['Number of Cases'][0] + ' cases.'
        return result
