import json

from workout_tracker.urls import PREFIX_API_URL


def add_api_prefix(suburl):
    return f'/{PREFIX_API_URL}{suburl.replace(" ", "%20")}'


def invalidate_credentials(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Token INVALID_TOKEN')


def get_json_file_len(filepath):
    with open(filepath, 'r') as file:
        return len(list(json.load(file)))
