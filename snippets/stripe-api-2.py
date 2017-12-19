
import stripe
import json
import sys
import time


#   print(json.dumps(c, sort_keys=True, indent=3, separators=(',', ': ')))

stripe.api_key = "sk_test_xxxxxxxxxxxx" # own a/c test key

timeStrFmt = '%Y-%m-%d %H:%M:%S'
# timeStrFmt = '%d/%m/%Y %H:%M:%S'


# Converts from UTC time to epoch
# Parameters:
#   timStr: e.g.'14/12/2017 7:27:00'
#   timFmt: e.g. '%d/%m/%Y %H:%M:%S' (default)
# returna:
#   UTC epoch (int)
def time_utc_to_epoch(timStr, timFmt=timeStrFmt):
  et = int(time.mktime(time.strptime(timStr, timFmt))) - time.timezone
  return et


# Converts from epoch (int) to UTC time (string)
def time_epoch_to_utc(epoch):
  global timeStrFmt
  utc = time.strftime(timeStrFmt, time.gmtime(epoch))
  return utc


# returns a list of charge objects from fromDate to toDate..
# parameters:
#   fromDate: e.g. '14/12/2017 7:27:00', INCLUSIVE
#   toDate:   e.g. '14/12/2017 23:59:59', INCLUSIVE
#   num:      number of records to fetch, can be lesser if records are less.
# returns:
#   list of charge objects
def retrieve_charge_objects(fromDate, toDate, num):
  fd = time_utc_to_epoch(fromDate)
  td = time_utc_to_epoch(toDate)
  dict = {'gte': fd, 'lte': td}
  print(dict, "gte: ", fromDate, ", lte: ", toDate)
  l = stripe.Charge.list(limit=num, created=dict, include=["total_count"])
  return l







# TESTING FUNCTIONS
#-------------------
def test_stripe_api():
  print('\r\nretrieving customers:')

  #  auto-pagination
  # customers is a ListObject
  customers = stripe.Customer.all(limit=3) # stripe.Customer.list(limit=3)
  for cust in customers.auto_paging_iter():
    #print(cust)
    print(cust['description'])
    print(cust['email'])

  # charge a customer
  print('\r\ncharging a customer:')
  resp = stripe.Charge.create(
    amount=2000,
    currency="sgd",
    source="card_1BYUrqArMeo2le8DWl0KH1fe", # obtained with Stripe.js
    description="Charge for ownself@example.com",
    capture='true',
    customer='cus_BwNbIUFrkcmlbx'
  )

  print(resp)


  #sys.exit()

  print('\r\nretrieving charges:')
  # Returns s dictionary with a data property that contains an array of charges
  # Each entry in the array is a separate charge object. 
  charges = stripe.Charge.list(limit=3)
  #charges = stripe.Charge.all()
  #print(json.dumps(charges))


  # c is a charge object
  for c in charges.auto_paging_iter():
    print(c['id'])
    print(c['description'])

  print('')
  print(charges.data[0].id)
  print(charges.url)


# retrieve charge objects from '2017-12-14 04:33' (INCLUSIVE) to '2017-12-14 08:19' (INCLUSIVE)
# NOTE: The date/time in "Created (UTC)" column (in exported csv file) do not show the seconds, so 
#       need to be aware that not all seconds are 0s (ie, in actual charge records)..
def test_ezlink_stripe():
  charges = retrieve_charge_objects('2017-12-14 04:33:00', '2017-12-14 08:19:00', 20)
  print("number of records: ", len(charges))
  print("total_count=", charges.total_count)
  print("has next=", charges.has_more)
  for c in charges.auto_paging_iter():
    print(c['id'])
    print(c['created'], ", utc=", time_epoch_to_utc(c['created']))
    print(c['metadata']['CAN'])
    print('\n')



def test_own_stripe():
  l = stripe.Charge.list(limit=20, include=["total_count"])
  print("number of records: ", len(l))
  print("total_count=", l.total_count)
  print("has next=", l.has_more)
  for i in l.data:
    print(i['created'], ", utc=", time_epoch_to_utc(i['created']))

def test_own_stripe2(fr, to):
  l = retrieve_charge_objects(fr, to, 20)
  print("number of records: ", len(l))
  print("total_count=", l.total_count)
  print("has next=", l.has_more)
  for i in l.data:
    print(i['created'], ", utc=", time_epoch_to_utc(i['created']))    



# main()
# -----------------
test_own_stripe()
print("\n")
test_own_stripe2('2017-12-13 00:00:00', '2017-12-13 23:59:59')
print("\n")
test_own_stripe2('2017-12-14 00:00:00', '2017-12-14 23:59:59')
print("\n")
test_own_stripe2('2017-12-15 00:00:00', '2017-12-15 23:59:59')
print("\n")
# 1513330100  GMT: Friday, 15 December 2017 09:28:20
# 1513134672  GMT: Wednesday, 13 December 2017 03:11:12

