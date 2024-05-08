import os
import pandas as pd
import openai
import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, text
from datetime import datetime


# Used to produce ChatGPT response if keywords aren't identified
def ask_openai(question, content=None):
    content_for_q = "Your name is AskHoos and you are a helpful assistant specializing in information about Charlottesville, Virginia. You are an adamant University of Virginia Fan! Go Hoos! Users can command !parks, !trails, !transportation, or !updates for help with specific Charlottesville issues."
    
    # Maximum length allowed for content_for_q
    max_length = 2000

    # Calculate the remaining space available
    remaining_space = max_length - len(content_for_q)
    
    # If content is not None and there is space available, append it
    if content is not None and remaining_space > 0:
        for row in content:
            row_str = str(row)
            # Check if adding the row exceeds the remaining space
            if len(row_str) <= remaining_space:
                content_for_q += row_str
                remaining_space -= len(row_str)
            else:
                # Truncate the row to fit the remaining space
                content_for_q += row_str[:remaining_space]
                break  # Stop appending rows once the limit is reached
            
        print("Content length: ", len(content_for_q))
    '''
    # Now content_for_q is guaranteed to be within the 2000 character limit
    if content is not None:
        for row in content:
            content_for_q += str(row)
    
    '''


    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Choose the model you prefer
        messages=[
            {"role": "system", "content": content_for_q},
            {"role": "user", "content": question}
        ],
        temperature=0.5,
        max_tokens=1000,
        stop=['quit', 'stop']
    )
    answer = response['choices'][0]['message']['content']
    return answer


def get_response(user_input: str) -> str:

    lowered: str = user_input.lower()

    if lowered == '':
        return "You are quiet. Do you have any questions about Charlottesville?"
    elif 'hello' in lowered:
        return "Hello to you, friend. Do you have any questions about Charlottesville?"
    elif 'bye' in lowered:
        return "Goodbye, friend! Have a great time in Charlottesville. I will be here whenever you need me again!"
    elif 'help' in lowered:
        return "You can command !parks, !trails, !transportation, or !crime for specific, up-to-date Charlottesville related information."
    else:
        load_dotenv()
        OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
        openai.api_key = OPEN_AI_KEY

        if '!parks' in lowered:
            recreation_dat = get_park_data()
            return ask_openai("What is some useful information and/or suggestions for Charlottsville parks?", content=recreation_dat)
        elif '!trails' in lowered:
            trail_dat = get_trail_data()
            return ask_openai("What is some useful information and/or suggestions for Charlottesville trails?", content=trail_dat)
        elif '!transportation' in lowered:
            trans_dat = get_trans_data()
            return ask_openai("List the provided bus stops and bike racks, along with their information.", content=trans_dat)
        elif '!crime' in lowered:
            crime_dat = get_crime_data()
            return ask_openai("What are the recent crimes in Charlottesville from proided data? Include where and when they happened/were reported.", content=crime_dat)
        else:
            return ask_openai(user_input)
        
    


#### Functions for database querying based on user's commands ####
def get_park_data():
    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")
    conn = engine.connect()

    try:
        query = text("SELECT PARKNAME FROM parks WHERE PARK_TYPE = 'COMMUNITY' ORDER BY RAND() LIMIT 2")
        results = conn.execute(query)

        return results 

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()


def get_trail_data():
    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")
    conn = engine.connect()

    try:
        query = text("SELECT NAME, TYPE FROM trails WHERE status = 'Existing' ORDER BY RAND() LIMIT 1")
        results = conn.execute(query)
        print(results)
        return results

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()


def get_trans_data():
    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")
    conn = engine.connect()

    try:
        bus_query = text("SELECT StopID, StopName FROM bus_stops ORDER BY RAND() LIMIT 2")
        results = conn.execute(bus_query)
        print(results)
        return results

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()


def get_crime_data():
    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")
    conn = engine.connect()

    try:
        crime_query = text("SELECT Offense, StreetName, DateReported, HourReported FROM crime WHERE DateReported IS NOT NULL and HourReported IS NOT NULL LIMIT 2")
        results = conn.execute(crime_query)
        # Convert timestamps to human-readable dates and hours
        crime_data = []

        # to convert DateReported and HourReported from Unix timestamp to human readable
        for result in results:
            offense = result[0]
            street_name = result[1]
            
            # Convert Unix timestamp to datetime object for DateReported
            date_reported = datetime.fromtimestamp(int(result[2]) / 1000)
            
            # Convert HourReported to hour and minute string
            hour_reported = "{:02}:{:02}".format(int(result[3]) // 100, int(result[3]) % 100)
            
            crime_data.append((offense, street_name, date_reported, hour_reported))

        return crime_data

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()
