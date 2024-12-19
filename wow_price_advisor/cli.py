from openai import OpenAI
from pydantic import BaseModel
import json
from typing import List, Optional

from .csv_util import save_json_to_csv, read_csv, add_item_names_to_csv
from .distances_from_embeddings import distances_from_embeddings
from .tsm_service import retrieve_items

class Item(BaseModel):
    item_id: int
    min_buyout: int
    market_value: int
    item_name: str
    item_recipe: Optional[str] = None
    num_tokens: Optional[int] = None
    embedding: Optional[List[float]] = None
    distance: Optional[float] = None

def main():
  question = "Is it cheaper to obtain a goblin sapper charge by using all available item recipes or buying it directly? Use all available item recipes to find the cheapest cost."
  client = OpenAI()

  item_ids = [
      3860, # mith bar
      9061, # goblin rocket fuel
      10646, # goblin sapper charge
      10560, # unstable trigger
      4338, # mageweave cloth
      10505, # solid blasting powder
      7912, # solid stone
  ]
  item_data_csv_path = "item_data.csv"

  item_csv_data = read_csv(item_data_csv_path)
  items = None
  if item_csv_data is not None:
    print("Items loaded from csv")
    items = item_csv_data
    add_item_names_to_csv(item_data_csv_path)  
  else:
    print("Item Data CSV does not exist. Requesting items using the TSM API.")
    items = retrieve_items(item_ids)
    save_json_to_csv(items, item_data_csv_path)
    add_item_names_to_csv(item_data_csv_path)

  all_items = [
    Item(item_id=i["itemId"], min_buyout=i["minBuyout"], market_value=i["marketValue"], item_name=i["itemName"], item_recipe=i["itemRecipe"]) if ("itemId" in i) else None for i in items
  ]
  
  all_items = [i for i in all_items if i]

  def create_embedding_for_item(item: Item) -> list:
      return client.embeddings.create(input=json.dumps(item.model_dump(exclude={'num_tokens', 'embedding', 'distance'})), model="text-embedding-ada-002").data[0].embedding

  all_item_embeddings = [create_embedding_for_item(item) for item in all_items]
  for index, item in enumerate(all_items):
      item.embedding = all_item_embeddings[index]

  qEmbeddings = client.embeddings.create(input=question, model="text-embedding-ada-002").data[0].embedding

  result_distances = distances_from_embeddings(qEmbeddings, [i.embedding for i in all_items], distance_metric="cosine")

  for i, distance in enumerate(result_distances):
      all_items[i].distance = distance

  returns = [json.dumps(i.model_dump(exclude={'num_tokens', 'embedding', 'distance'})) for i in all_items]

  context = "\n\n###\n\n".join(returns)

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Answer the question below. Your task is to find if the crafting cost for the item is less than the cost it is to buy it directly. List the cost of each item in the recipe and whether or not it was cheaper to craft it or buy it directly. If the cost of any item is cheaper using the item recipe, use that instead of buying directly. Try every combination of obtaining an item to see which route is cheapest."
            "If the question can't be answered based on the context, say \"I don't know\"\n\n.",
        },
        {
            "role": "user",
            f"content": f"Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
        },
    ],
    temperature=0,
    max_tokens=None,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
  )

  print(response.choices[0].message.content.strip())

if __name__ == "__main__":
    main()