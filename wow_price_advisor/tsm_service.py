import requests
from dotenv import load_dotenv
import os

def retrieve_items(item_ids):
  load_dotenv()
  r = requests.post("https://auth.tradeskillmaster.com/oauth2/token",{
    "client_id": "c260f00d-1071-409a-992f-dda2e5498536",
    "grant_type": "api_token",
    "scope": "app:realm-api app:pricing-api",
    "token": os.getenv('TSM_API_KEY')
  })
  responseJson = r.json();
  accessToken = responseJson["access_token"]
  items = [
    requests.get(f"https://pricing-api.tradeskillmaster.com/ah/556/item/{i_id}", headers={'Authorization': 'Bearer ' + accessToken}).json() for i_id in item_ids
  ]
  return items