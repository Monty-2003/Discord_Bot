from api_responses import crime_data

from sqlalchemy import create_engine
from datetime import datetime
from pytz import timezone

# connect to db
engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")

try:
    # get data from api
    crime_df = crime_data.get_crime_data()
    crime_df.to_sql(con=engine, name="crime",if_exists="replace", index=False)
    print("Data successfully uploaded to database at EST:", datetime.now(timezone('EST')))

except Exception as e:
    print("An error occured:", e)

# close connection to db
finally:
    engine.dispose()




