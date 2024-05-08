import os
import pandas as pd
import openai
from dotenv import load_dotenv
from sqlalchemy import create_engine, Table, MetaData, select

# Used to produce ChatGPT response if keywords aren't identified
def ask_openai(question, content=(('', ''), ('', ''))):
    content_for_q = "Your name is AskHoos and you are a helpful assistant specializing in information about Charlottesville, Virginia. You are an adamant University of Virginia Fan! Go Hoos! Users can command !recreation, !transportation, !updates for help with specific Charlottesville issues."
    content_for_q += content[0][0]
    content_for_q += content[0][1]
    content_for_q += content[1][0]
    content_for_q += content[1][1]

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
        return "You can command !recreation, !transportation, or !updates for Charlottesville related information."
    else:
        load_dotenv()
        OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
        openai.api_key = OPEN_AI_KEY

        if '!recreation' in lowered:
            recreation_dat = get_recreation_data()
            return ask_openai("Give general information and suggestions for ideas based on the provided Charlottesville park and trail system information.", content=recreation_dat)
        elif '!transportation' in lowered:
            return ask_openai(user_input)
        elif '!updates' in lowered:
            return ask_openai(user_input)
        else:
            return ask_openai(user_input)
        
    
def get_recreation_data():
    engine = create_engine("mysql+mysqlconnector://aba9jj:aba9jj!@database.ds2002.org/aba9jj")
    connection = engine.connect()
    #metadata = MetaData()
    # get data from db
    #park_table = Table('parks', metadata)
    #trail_table = Table('trails', metadata)

    #park_query = select(park_table)
    #trail_query = select(trail_table)

    try:
       park_result = pd.read_sql("SELECT `PARK_TYPE`, 'PARKNAME' FROM parks WHERE `PARK_TYPE`='COMMUNITY'", engine)
       trail_result = pd.read_sql('SELECT `NAME`, `TYPE`, `STATUS`, `PROPERTY_OWNER` FROM trails', engine)

       return [("Park information: ", park_result.to_string(index=False)), ("Trail information: ", trail_result.to_string(index=False))]

    except Exception as e:
        print("An error occured:", e)

    # close connection to db
    finally:
        engine.dispose()