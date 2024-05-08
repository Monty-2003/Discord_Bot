import os
import openai
from dotenv import load_dotenv

# Used to produce ChatGPT response if keywords aren't identified
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Choose the model you prefer
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
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
    else:
        load_dotenv()
        OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
        openai.api_key = OPEN_AI_KEY
        return ask_openai(user_input)