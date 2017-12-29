
import stripe
import json
import sys
import time
import random


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


def charge_customer(amt, src, desc, cust):
  resp = stripe.Charge.create(
    amount=amt,
    currency="sgd",
    source=src, # obtained with Stripe.js
    description=desc,
    customer=cust
  )
  print(resp)




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

def test_charge_own(start, stop, src):
  for i in range(start, stop):
    desc = "customer {0}".format(i)
    charge_customer(2000, src, desc)
    time.sleep(2)


def test_charge_own2(start, stop, src, cust):
  random.seed()
  for i in range(start, stop):
    desc="item number {0}".format(i)
    n = random.randrange(1,6)
    try:
      charge_customer(n*1000, src[n-1], desc, cust)
    except stripe.error.CardError:
      print("Oops! ", stripe.error.CardError)
    time.sleep(n)


# main()
# -----------------
token = ["tok_visa", "tok_sg", "tok_hk", "tok_au", "tok_be", "tok_it"]
token2 = ["tok_visa_debit", "tok_mastercard", "tok_mastercard_debit", "tok_chargeDeclined", "tok_discover", "tok_diners"]
token3 = ["tok_nl", "tok_jcb", "tok_avsFail", "tok_gb", "tok_ch", "tok_ru"]

test_charge_own2(71, 90, token, None)
time.sleep(50)
test_charge_own2(91, 120, token2, None)




# "tok_amex"





# test_own_stripe()
# print("\n")
# test_own_stripe2('2017-12-13 00:00:00', '2017-12-13 23:59:59')
# print("\n")
# test_own_stripe2('2017-12-14 00:00:00', '2017-12-14 23:59:59')
# print("\n")
# test_own_stripe2('2017-12-15 00:00:00', '2017-12-15 23:59:59')
# print("\n")

# 1513330100  GMT: Friday, 15 December 2017 09:28:20
# 1513134672  GMT: Wednesday, 13 December 2017 03:11:12


# 260000.00                       
# 266700.00 6700.00           
# 273567.50 6867.50           
# 280606.69 7039.19     45000.00                                100000.00 
# 287821.85 7215.17     47200.00  2200.00   9415.17             104400.00 4400.00
# 295217.40 7395.55     49488.00  2288.00   9683.55             108976.00 4576.00
# 302797.84 7580.44     51867.52  2379.52   9959.96             113735.04 4759.04
# 310567.78 7769.95     54342.22  2474.70   10244.65            118684.44 4949.40
# 318531.98 7964.19     56915.91  2573.69   10537.88            123831.82 5147.38
# 326695.28 8163.30     59592.55  2676.64   10839.94            129185.09 5353.27
# 335062.66 8367.38     62376.25  2783.70   11151.08            134752.50 5567.40
# 343639.22 8576.57     65271.30  2895.05   11471.62            140542.60 5790.10
# 352430.20 8790.98     68282.15  3010.85   11801.83            146564.30 6021.70
# 361440.96 9010.76     71413.44  3131.29   12142.04            152826.87 6262.57


#08 10 12 14 16 18 20
# 188000
# 195920
# 204156
# 212723

