

import pandas as pd


cache = {}

def cached_date_parser(s):
    if s in cache:
        return cache[s]
    dt = pd.to_datetime(s, format='%Y%m%d', coerce=True)
    cache[s] = dt
    return dt


# df = pd.read_csv('TX_CSC_FINANCIAL.csv',
#                  index_col=None,
#                  header=None,
#                  parse_dates=[0],
#                  date_parser=cached_date_parser)


df = pd.read_csv('TX_CSC_FINANCIAL.csv')

df.columns = [c.lower() for c in df.columns] 

for i in df.columns:
	print(i)


from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5439/postgres')

# "trial" is name of table
df.to_sql("TX_CSC_FINANCIAL", engine, if_exists='append',index=False)


