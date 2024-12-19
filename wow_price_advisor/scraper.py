import requests
import json
import re
from html import unescape

from bs4 import BeautifulSoup

def clean_json(data):
    # Step 1: Replace HTML entities with their corresponding characters
  data = unescape(data)

  # Step 2: Replace single quotes with double quotes around values
  data = data.replace("'", '"')

  # Step 3: Ensure keys are quoted
  # Use a regex to wrap unquoted keys with double quotes
  data = re.sub(r'(\w+):', r'"\1":', data)

  # Step 4: Remove trailing commas
  data = re.sub(r',\s*([\]}])', r'\1', data)

  # Step 5: Handle JavaScript-style object references (like WH.TERMS.createdby)å
  data = re.sub(r'WH\.TERMS\.createdby', '"WH.TERMS.createdby"', data)

  # Attempt to load the cleaned string as JSON
  try:
    return json.loads(data)
  except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)

def scrape():
    resp = requests.get('https://www.wowhead.com/classic/item=10646#created-by-spell')
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find_all("script")
    for i in script_tag:
      pattern = r"id:\s*['\"]created-by-spell['\"]"
      if re.search(pattern, str(i)):
         pattern = r"\{\s*template:\s*['\"]spell['\"],\s*id:\s*['\"]created-by-spell['\"],(.*?)\n\}"
         match = re.search(pattern, str(i), re.DOTALL)
         if match:
            object_string = match.group(0)

            # Load into a Python dictionary
            try:
              json_object = clean_json(object_string)
              print(json.dumps(json_object, indent=4))å
            except json.JSONDecodeError as e:
              print("Failed to decode JSON:", e)