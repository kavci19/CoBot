import datetime
import heapq
from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

date = str(datetime.datetime.now()).split()[0].split('-')
GsSession.use(Environment.PROD, 'b16a94fab7714a61b29065f6d6bda51b',
              '2179ad8fec38bbe8995f4d07293f9b476476dbef67b99f3a4074099de3fff049', ('read_product_data',))

region_to_key = {'Americas': 'AMRO',
                 'Eastern Mediterranean': 'EMRO',
                 'Western Pacific': 'WPRO',
                 'Southeast Asia': 'SEARO'}


# functionality: computes the countries with the most/least amount of daily new deaths/infected in a given region (if
# supplied)
# N = amount of countries to be returned
# queryType = newConfirmed or newFatalities
# region = region of the world to query (Americas, Southeast Asia, etc.)
# order = least or greatest

def get_daily_new(N, queryType, region=None, order='least'):

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


# samples
if __name__ == '__main__':
    print(get_daily_new(5, 'newConfirmed'))
    print(get_daily_new(5, 'newConfirmed', 'Americas', 'most'))
    print(get_daily_new(3, 'newFatalities', 'Eastern Mediterranean', 'most'))
    print(get_daily_new(10, 'newConfirmed', 'Western Pacific', 'least'))
    print(get_daily_new(10, 'newConfirmed', 'Southeast Asia', 'most'))
