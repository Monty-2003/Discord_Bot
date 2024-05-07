from api_responses import crime_data
from api_responses import closure_data

from sqlalchemy import create_engine
from datetime import datetime
from pytz import timezone

def main():
    # connect to db
    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")

    try:
        # get data from api
        crime_df = crime_data.get_crime_data()
        crime_df = crime_df[['RecordID', 'Offense', 'IncidentID', 'BlockNumber', 'StreetName', 'Agency', 'DateReported', 'HourReported', 'ReportingOfficer']]
        crime_df.to_sql(con=engine, name="crime",if_exists="replace", index=False)
        print("Crime data successfully uploaded to database at EST:", datetime.now(timezone('EST')))

        closure_df = closure_data.get_closure_data()
        closure_df.to_sql(con=engine, name='closures',if_exists='replace',index=False)
        print("Closure data successfully uploaded to database at EST:", datetime.now(timezone('EST')))

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()








