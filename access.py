# GS Quant documentation available at:
# https://developer.gs.com/docs/gsquant/guides/getting-started/

import datetime

from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

GsSession.use(Environment.PROD, 'b16a94fab7714a61b29065f6d6bda51b', '2179ad8fec38bbe8995f4d07293f9b476476dbef67b99f3a4074099de3fff049', ('read_product_data',))

ds = Dataset('COVID19_COUNTRY_DAILY_WHO')
data = ds.get_data(datetime.date(2020, 1, 21), countryId=["CN", "OM", "MH"], limit=50)
print(data.head())  # peek at first few rows of data
