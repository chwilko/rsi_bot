# import datetime
import time

from read_price_helper import ReadPriceHelper
from rsi_counter import relative_strength_index

now = int(time.time() * 1000)
start = now - 1000 * 3600 * 24 * 14

data = ReadPriceHelper().read_interval(start, now)


res = relative_strength_index(data, close_key="closePrice")

print(res)

# while 1:

#     sleep(2)
#     print("lol")
