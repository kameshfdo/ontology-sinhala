
from api import call_api

def process_messages(messages):
    results = []
    for message in messages:
        result = call_api(message)
        results.append(result)
    return results
