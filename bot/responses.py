import os
import pandas as pd
import openai
import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, text


# Used to produce ChatGPT response if keywords aren't identified
def ask_openai(question, content=None):
    content_for_q = "Your name is AskHoos and you are a helpful assistant specializing in information about Charlottesville, Virginia. You are an adamant University of Virginia Fan! Go Hoos! Users can command !recreation, !transportation, !updates for help with specific Charlottesville issues."
    
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
        temperature=0.5
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
        return "You can command !parks, !trails, !transportation, or !updates for specific Charlottesville related information."
    else:
        load_dotenv()
        OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
        openai.api_key = OPEN_AI_KEY

        if '!parks' in lowered:
            recreation_dat = get_park_data()
            return ask_openai("Give general information and suggestions for ideas based on the given Charlottesville park information.", content=recreation_dat)
        elif '!trails' in lowered:
            trail_dat = get_trail_data()
            return ask_openai("Give general information and suggestions for ideas based on the given Charlottesville trail information.", content=trail_dat)
        elif '!transportation' in lowered:
            return ask_openai(user_input)
        elif '!updates' in lowered:
            return ask_openai(user_input)
        else:
            return ask_openai(user_input)
        
    


#### Functions for database querying based on user's commands ####
def get_park_data():
    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")
    conn = engine.connect()

    try:
        query = text("SELECT PARKNAME FROM parks WHERE PARK_TYPE = 'COMMUNITY' LIMIT 2")
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
        query = text("SELECT NAME, TYPE, STATUS FROM trails LIMIT 2")
        results = conn.execute(query)
        print(results)
        return results

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()

