import requests
import json
from json import JSONDecodeError
from backend.config import Config

class LinksCollector:
    def __init__(self):
        pass

    def get_organic_links(self, query):
        url = Config.SERPER_URL

        payload = json.dumps({
        "q": query,
        "gl": Config.SERPER_COUNTRY,
        "num": Config.SERPER_NUM_RESULTS
        })

        headers = {
        'X-API-KEY': Config.SERPER_API_KEY,
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        try:
            results = response.json()  # Extract and parse the JSON from the response
            organic_links = [result["link"] for result in results.get("organic", [])]
            return organic_links
        
        except JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return []
        