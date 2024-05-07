import random

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "You r quiet"
    elif 'hello' in lowered:
        return "Hello to you too"
    elif 'roll dice' in lowered:
        return "You rolled a " + str(random.randint(1, 6))
    