
import psycopg2
import pandas as pd
from sqlalchemy import *

csvFile = 'TX_CSC_FINANCIAL.csv'
dbConnString = 'postgresql://postgres:postgres@localhost:5439/postgres'
tableName = "tx_csc_financial"

cache = {}

def cached_date_parser(s):
    if s in cache:
        return cache[s]
    dt = pd.to_datetime(s, format='%Y%m%d', coerce=True)
    cache[s] = dt
    return dt


def createTable():
    engine = create_engine(dbConnString)
    metadata = MetaData()

    tx_csc_financial = Table(tableName, metadata,
        Column('csc_app_no'.upper(), BigInteger),
        Column('purse_txn_ctr'.upper(), Integer),
        Column('msg_type_cd'.upper(), Integer),
        Column('txn_datetime'.upper(), DateTime),
        Column('processing_date'.upper(), DateTime),
        Column('business_date'.upper(), DateTime),
        Column('blob_id'.upper(), String(26)),
        Column('csc_make'.upper(), Integer),
        Column('issuer_id'.upper(), Integer),
        Column('dev_type_cd'.upper(), Integer),
        Column('dev_seq_no'.upper(), Integer),
        Column('bad_debt_ctr'.upper().upper().upper().upper(), Integer),
        Column('purse_status_cd'.upper().upper().upper().upper(), String(10)),
        Column('txn_type_cd'.upper().upper().upper().upper(), Integer),
        Column('txn_amt'.upper().upper().upper().upper(), Float),
        Column('purse_bal_amt'.upper().upper().upper().upper(), Float),
        Column('av_ctr'.upper().upper().upper().upper(), Integer),
        Column('modify_purse_ctr'.upper().upper().upper().upper(), Integer),
        Column('debit_option_list'.upper().upper().upper().upper(), Integer),
        Column('pay_mode_cd'.upper().upper().upper().upper(), Integer),
        Column('acq_id'.upper().upper().upper().upper(), Integer),
        Column('agent_id'.upper().upper().upper(), Integer),
        Column('last_purse_status_cd'.upper().upper().upper(), Integer),
        Column('last_txn_type_cd'.upper().upper().upper(), Integer),
        Column('last_txn_amt'.upper().upper().upper(), Float),
        Column('last_txn_datetime'.upper().upper().upper(), DateTime),
        Column('last_purse_bal_amt'.upper().upper().upper(), Float),
        Column('last_purse_txn_ctr'.upper().upper().upper(), Integer),
        Column('last_av_ctr'.upper().upper().upper(), Integer),
        Column('last_modify_purse_ctr'.upper().upper().upper(), Integer),
        Column('last_txn_debit_option_list'.upper().upper().upper(), Integer),
        Column('last_pay_mode_cd'.upper().upper(), Integer),
        Column('last_txn_acq_id'.upper().upper(), Integer),
        Column('last_txn_agent_id'.upper().upper(), Integer),
        Column('last_debit_option_list'.upper().upper(), Integer),
        Column('last_sign_cert_no'.upper().upper(), String(20)),
        Column('last_cr_txn_type_cd'.upper().upper(), Integer),
        Column('last_cr_txn_amt'.upper().upper(), Integer),
        Column('last_cr_txn_datetime'.upper().upper(), DateTime),
        Column('last_cr_debit_option_list'.upper().upper(), Integer),
        Column('last_cr_txn_pay_mode_cd'.upper().upper(), Integer),
        Column('last_cr_txn_acq_id'.upper(), Integer),
        Column('last_cr_txn_agent_id'.upper(), Integer),
        Column('csc_dep_amt'.upper(), Integer),
        Column('csc_cost_amt'.upper(), Integer),
        Column('purse_create_date'.upper(), DateTime),
        Column('purse_expiry_date'.upper(), DateTime),
        Column('replace_ind'.upper(), String(20)),
        Column('personal_fee_amt'.upper(), Float),
        Column('black_reason_cd'.upper(), String(20)),
        Column('acct_holder_name'.upper(), String(20)),
        Column('acct_holder_personal_id'.upper(), String(20)),
        Column('acct_holder_id_type_cd'.upper(), String(20)),
        Column('acct_holder_addr'.upper(), String(20)),
        Column('acct_holder_birth_date'.upper(), DateTime),
        Column('acct_holder_phone_no'.upper(), String(20)),
        Column('bank_cd'.upper(), String(20)),
        Column('bank_acct_type_cd'.upper(), String(20)),
        Column('bank_acct_no'.upper(), Integer),
        Column('autoload_refr_no'.upper(), Integer),
        Column('autoload_int'.upper(), Integer),
        Column('autoload_type_cd'.upper(), String(20)),
        Column('autoload_end_date'.upper(), DateTime),
        Column('autoload_amt'.upper(), Integer),
        Column('sys_audit_trace_no'.upper(), Integer),
        Column('nets_terminal_id'.upper(), String(20)),
        Column('nets_txn_datetime'.upper(), DateTime),
        Column('nets_resp_cd'.upper(), String(20)),
        Column('nets_auth_cd'.upper(), String(20)),
        Column('ref_receipt_no'.upper(), String(20)),
        Column('ref_method_cd'.upper(), String(20)),
        Column('csc_retain_ind'.upper(), String(20)),
        Column('ref_csc_dep_amt'.upper(), Float),
        Column('ref_purse_bal_amt'.upper(), Float),
        Column('ref_goodwill_amt'.upper(), Float),
        Column('ref_penalty_fee_amt'.upper(), Float),
        Column('ref_admin_fee_amt'.upper(), Float),
        Column('ref_status_cd'.upper(), String(20)),
        Column('sur_reason_cd'.upper(), String(20)),
        Column('personal_id'.upper(), String(20)),
        Column('personal_id_type_cd'.upper(), String(20)),
        Column('spt_no'.upper(), String(20)),
        Column('vehicle_no'.upper(), String(20)),
        Column('car_park_loc_id'.upper(), String(20)),
        Column('valid_mon'.upper(), String(20)),
        Column('car_park_seq_no'.upper(), String(20)),
        Column('prt_amt'.upper(), Float),
        Column('csa_pass_no'.upper(), String(20)),
        Column('sign_cert_no'.upper(), String(20)),
        Column('create_datetime'.upper(), DateTime),
        Column('personal_ctry_cd'.upper(), String(20)),
        Column('cheque_no'.upper(), String(20)),
        Column('old_purse_expiry_date'.upper(), DateTime),
        Column('old_csc_dep_amt'.upper(), Float),
        Column('old_ref_status_cd'.upper(), String(20)),
        Column('old_autoload_type_cd'.upper(), String(20)),
        Column('old_autoload_end_date'.upper(), DateTime),
        Column('old_bad_debt_ctr'.upper(), String(20)),
        Column('new_purse_expiry_date'.upper(), DateTime),
        Column('new_csc_dep_amt'.upper(), Float),
        Column('new_ref_status_cd'.upper(), String(20)),
        Column('new_autoload_type_cd'.upper(), String(20)),
        Column('new_autoload_end_date'.upper(), DateTime),
        Column('new_bad_debt_ctr'.upper(), Integer),
        Column('purse_return_ind'.upper(), String(20)),
        Column('fee_pay_ind'.upper(), String(20)),
        Column('ref_dep_ind'.upper(), String(20)),
        Column('encode_txn_amt'.upper(), Float),
        Column('csc_profile_type_cd'.upper(), String(20)),
        Column('rental_dep_amt'.upper(), Float),
        Column('ref_rental_dep_amt'.upper(), Float),
        Column('rental_dep_create_date'.upper(), DateTime),
        Column('rental_dep_expiry_date'.upper(), DateTime),
        Column('old_csc_profile_type_cd'.upper(), String(20)),
        Column('rental_dep_writeoff_amt'.upper(), Float)
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
createTable()

# --- import data
try:
    loadDB(csvFile)
except Exception as e:
    print("main - exception: ", e)  

#printCSVHeaders(csvFile)



