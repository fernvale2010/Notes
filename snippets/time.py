
# https://www.epochconverter.com/

import time



et = int(time.mktime(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S'))) - time.timezone
print(et)
# 946730040
# GMT: Saturday, 1 January 2000 12:34:00
# Your time zone: Saturday, 1 January 2000 20:34:00 GMT+08:00


# 14/12/2017 7:27
et = int(time.mktime(time.strptime('14/12/2017 7:27:00', '%d/%m/%Y %H:%M:%S'))) - time.timezone
print(et)
# 1513236420
# GMT: Thursday, 14 December 2017 07:27:00
# Your time zone: Thursday, 14 December 2017 15:27:00 GMT+08:00




