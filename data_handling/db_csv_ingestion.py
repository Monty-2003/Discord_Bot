import pandas as pd
from datetime import datetime
from pytz import timezone
from sqlalchemy import create_engine


def main():
    # Get .csv file data
    trail_data = pd.read_csv("./csv_data/City_Trails.csv")
    park_data = pd.read_csv("./csv_data/Park_Area.csv")
    bus_stop_data = pd.read_csv("./csv_data/CAT_Bus_Stop_Points.csv")
    bike_rack_data = pd.read_csv("./csv_data/Bicycle_Rack_Points.csv")


    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")

    try:
        # load data to mysql db
        trail_data.to_sql(con=engine, name="trails",if_exists='replace', index=False)
        print("Trail data successfully uploaded to database at EST:", datetime.now(timezone('EST')))

        park_data.to_sql(con=engine, name="parks", if_exists='replace', index=False)
        print("Park area data successfully uploaded to database at EST:", datetime.now(timezone('EST')))

        bus_stop_data.to_sql(con=engine, name="bus_stops", if_exists='replace', index=False)
        print("Bus stop data successfully uploaded to database at EST:", datetime.now(timezone('EST')))

        bike_rack_data.to_sql(con=engine, name="bike_racks", if_exists='replace', index=False)
        print("Bike rack data successfully uploaded to database at EST:", datetime.now(timezone('EST')))

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()

