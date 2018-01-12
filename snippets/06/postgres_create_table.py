
import psycopg2
import pandas as pd
from sqlalchemy import *

csvFile = 'TX_CSC_FINANCIAL.csv'
dbConnString = 'postgresql://postgres:postgres@localhost:5439/postgres'
csvobjectTableName = "csvobject_table"


# input tables
trx2_ofts_txnTableName = "trx2_ofts_txn"
trx2_stripe_chargeTableName = "trx2_stripe_charge"
tx_csc_financialTableName = "tx_csc_financial"

# output table
tx_ofts_stripe_matchstatusTableName = "trx2_stripe_ofts_matchstatus"  


cache = {}

def cached_date_parser(s):
    if s in cache:
        return cache[s]
    dt = pd.to_datetime(s, format='%Y%m%d', coerce=True)
    cache[s] = dt
    return dt


def csvobjectCreateTable():
    engine = create_engine(dbConnString)
    metadata = MetaData()

    table = Table(csvobjectTableName.lower(), metadata,
        Column('Id'.lower(), String(48)),
        Column('can'.lower(), BigInteger),
        Column('ptc'.lower(), Integer),
        Column('Amount'.lower(), Float),
        Column('TXN_Date'.lower(), DateTime)
    )

    metadata.create_all(engine)


# OFTS TXN (e.g. 20171212__OFTS Sample Data.xls)
def trx2_ofts_txnCreateTable():
    engine = create_engine(dbConnString)
    metadata = MetaData()

    table = Table(trx2_ofts_txnTableName.lower(), metadata,
        Column('Id'.lower(), BigInteger),
        Column('SYSCREATETRNDATETIME'.lower(), DateTime),
        Column('REQID'.lower(), Integer),
        Column('REQNAME'.lower(), String(16)),
        Column('REQREF'.lower(), String(48)), # stripe id
        Column('CAN'.lower(), BigInteger),
        Column('TRNSTATUS'.lower(), String(4)),
        Column('TRNTYPE'.lower(), Integer),
        Column('EZLREF'.lower(), String(48)),
        Column('TRNAMOUNTSGD'.lower(), Float),
        Column('TRNAMOUNT'.lower(), Float),
        Column('TRNTIME'.lower(), BigInteger),
        Column('PRETRNINFO2'.lower(), Integer),
        Column('TRNINFO2'.lower(), Integer),
        Column('TRNAMOUNTSGD'.lower(), Float),
        Column('SYSLOCKTRNTIMESTAMP'.lower(), DateTime),
        Column('SYSSTATUSUPDATETIMESTAMP'.lower(), DateTime),
        Column('LASTTRNUPDATETIMESTAMP'.lower(), DateTime)

    )

    metadata.create_all(engine)




# STRIPE CHARGE (e.g. payments-ezlink.csv)
def trx2_stripe_chargeCreateTable():
    engine = create_engine(dbConnString)
    metadata = MetaData()

    table = Table(trx2_stripe_chargeTableName.lower(), metadata,
        Column('Id'.lower(), String(48)),  # stripe id
        Column('Description'.lower(), String(64)),
        Column('CREATED_UTC'.lower(), DateTime),
        Column('AMOUNT'.lower(), Float),
        Column('Captured'.lower(), String(12)),
        Column('Status'.lower(), String(12)),
        Column('Card_ID'.lower(), String(48)),
        Column('CAN'.lower(), BigInteger),
        Column('Convenience_Fee'.lower(), Float),
        Column('SyncAmount'.lower(), Float),
        Column('Scheme'.lower(), String(12))

    )

    metadata.create_all(engine)


# CMCC (e.g. TX_CSC_FINANCIAL.csv)
def tx_csc_financialCreateTable():
    engine = create_engine(dbConnString)
    metadata = MetaData()

    table = Table(tx_csc_financialTableName.lower(), metadata,
        Column('CSC_APP_NO'.lower(), BigInteger),
        Column('PURSE_TXN_CTR'.lower(), BigInteger),
        Column('MSG_TYPE_CD'.lower(), BigInteger),
        Column('TXN_DATETIME'.lower(), DateTime),
        Column('PROCESSING_DATE'.lower(), DateTime),
        Column('BUSINESS_DATE'.lower(), DateTime),
        Column('TXN_TYPE_CD'.lower(), Integer),
        Column('TXN_AMT'.lower(), Float),
        Column('PURSE_BAL_AMT'.lower(), Float),
        Column('ACQ_ID'.lower(), BigInteger),
        Column('AGENT_ID'.lower(), Integer)

    )

    metadata.create_all(engine)



# output table
def tx_ofts_stripe_matchstatusCreateTable():
    engine = create_engine(dbConnString)
    metadata = MetaData()

    table = Table(tx_ofts_stripe_matchstatusTableName.lower(), metadata,
        Column('TRANSACTION_DATE_TIME'.lower(), DateTime),
        Column('PROCESSING_DATE_TIME'.lower(), DateTime),
        Column('CAN_ID'.lower(), BigInteger),
        Column('PTC'.lower(), BigInteger),
        Column('AGENT_ID'.lower(), Integer),
        Column('AGENT_NAME'.lower(), String(12)),
        Column('EXTERNAL_REFERENCE'.lower(), String(100)),
        Column('AMOUNT'.lower(), Float),
        Column('TXN_TYPE'.lower(), Integer),
        Column('EXCEPTION_CODE'.lower(), String(4)),
        Column('EXTERNAL_SOURCE'.lower(), String(10)),
        Column('UNMATCHED_TYPE'.lower(), String(12)),
        Column('MATCHING_REMARK'.lower(), String(100)),
        Column('MATCHED_ENTRY_DATE'.lower(), DateTime),
        Column('REFUND_METHOD'.lower(), String(100)),
        Column('REFERENCE'.lower(), String(100)),
        Column('LAST_MODIFIED_DATE'.lower(), DateTime),
        Column('LAST_MODIFIED_USER'.lower(), String(24)),
        Column('OnlineOCBC_REFERENCE'.lower(), String(100)),
        Column('STRIPE_ID'.lower(), String(48))
    )

    metadata.create_all(engine)




def loadDB(f):
    engine = create_engine(dbConnString)
    df = pd.read_csv(f)

    # "TX_CSC_FINANCIAL" is name of table
    try:
        df.to_sql(tableName, engine, if_exists='append', index=False)
    except psycopg2.OperationalError as exc:
        print("psycopg2: ", exc)

    # df.to_sql(tableName, engine, if_exists='append', index=False)



def printCSVHeaders(f):
    # df = pd.read_csv('TX_CSC_FINANCIAL.csv',
    #                  index_col=None,
    #                  header=None,
    #                  parse_dates=[0],
    #                  date_parser=cached_date_parser)

    df = pd.read_csv(f)
    df.columns = [c.lower() for c in df.columns] 
    print(df.index)

    for i in df.columns:
        print(i)




#---- main()
#---- Create table
csvobjectCreateTable()
trx2_ofts_txnCreateTable()
trx2_stripe_chargeCreateTable()
tx_csc_financialCreateTable()
tx_ofts_stripe_matchstatusCreateTable()

# --- import data
# try:
#     loadDB(csvFile)
# except Exception as e:
#     print("main - exception: ", e)  

#printCSVHeaders(csvFile)


print("End of run")
