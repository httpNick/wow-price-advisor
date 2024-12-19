from openai import OpenAI
from csv_util import save_json_to_csv, read_csv, add_item_names_to_csv
from tsm_service import retrieve_items

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
