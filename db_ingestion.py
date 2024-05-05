import pandas as pd
from sqlalchemy import create_engine

data = pd.read_csv("./City_Trails.csv")

engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")

try:
    data.to_sql(con=engine, name="cville_trails",if_exists="replace", index=False)
    print("Data successfully uploaded to database aba9jj, table cville_trails")

except Exception as e:
    print("An error occured:", e)
    
# close connection to db
finally:
    engine.dispose()



