
import psycopg2

dbConnString = 'postgresql://postgres:postgres@localhost:5439/postgres'
csvobjectTableName = "csvobject_table"

trx2_ofts_txnTableName = "trx2_ofts_txn"
trx2_stripe_chargeTableName = "trx2_stripe_charge"
tx_csc_financialTableName = "tx_csc_financial"

# output table
tx_ofts_stripe_matchstatusTableName = "trx2_stripe_ofts_matchstatus"  

dropTableName = [csvobjectTableName, trx2_ofts_txnTableName, \
                trx2_stripe_chargeTableName, tx_csc_financialTableName, \
                tx_ofts_stripe_matchstatusTableName]

# drop tables
def dropTable():
    conn = psycopg2.connect(dbConnString)
    cur = conn.cursor()
    for name in dropTableName:
        print("Dropping {0}", name)
        try:
            cmd = str.format("DROP TABLE {0};", name)
            cur.execute(cmd)  
            conn.commit()
        except Exception as e:
            print(e)

    conn.close()    


dropTable()
print("End of run")
