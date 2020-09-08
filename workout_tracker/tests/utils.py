from workout_tracker.urls import PREFIX_API_URL


def add_api_prefix(suburl):
    return f'/{PREFIX_API_URL}{suburl.replace(" ", "%20")}'
