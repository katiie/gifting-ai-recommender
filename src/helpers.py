from functools import lru_cache
import requests


@lru_cache(maxsize=1)
def get_countries():
    response = requests.get("https://api.first.org/data/v1/countries")
    if response.status_code == 200:
        return sorted(list(map(lambda x: x["country"].capitalize(),
                      response.json()['data'].values())))
    return None
