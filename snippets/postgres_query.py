
# Import packages
from sqlalchemy import create_engine
import pandas as pd

# Create engine: engine
engine = create_engine('postgresql://postgres:postgres@localhost:5439/postgres')

# Open engine connection
con = engine.connect()

# Perform query: rs
rs = con.execute('select id, reqref, can, syscreatetrndatetime from Trial')

# Save results of the query to list: ll
ll = rs.fetchall()

# Close connection
con.close()


# Print head of list
print(len(ll),type(ll),ll[:3])

print("\r\n\r\n")

# Save results of the query to DataFrame
df=pd.DataFrame(ll)
df.head(3)

print(df)

df = pd.read_sql_query(
    "SELECT id, reqref, can, syscreatetrndatetime from Trial WHERE id >= 6966 order by id",
    engine
)

print("\r\n\r\n")
print(df.to_string())

