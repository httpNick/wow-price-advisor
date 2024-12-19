import csv
import os
import pandas as pd

def save_json_to_csv(json_data, csv_file_path):
  if not os.path.exists(csv_file_path):
    fieldnames = json_data[0].keys()

    with open(csv_file_path, 'w', newline='') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()
      
      for entry in json_data:
        writer.writerow(entry)

def read_csv(csv_file_path):
    if os.path.exists(csv_file_path):
      with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
        return data
    else:
      return None
    
def add_item_names_to_csv(csv_file_path):
  df = pd.read_csv(csv_file_path)

  df['itemName'] = ''
  df["itemRecipe"] = ''

  item_id_to_name = {
      3860: 'Mithril Bar',
      9061: 'Goblin Rocket Fuel',
      10646: "Goblin Sapper Charge",
      10560: "Unstable Trigger",
      4338: "Mageweave Cloth",
      10505: "Solid Blasting Powder",
      7912: "Solid Stone"
  }

  item_id_to_recipe = {
      10505: "2 Solid Stone",
      10646: "1 Unstable Trigger, 1 Mageweave Cloth, 3 Solid Blasting Powder",
      10560: "1 Mithril Bar, 1 Mageweave Cloth, 1 Solid Blasting Powder"
  }

  df['itemName'] = df['itemId'].map(item_id_to_name)
  df['itemRecipe'] = df['itemId'].map(item_id_to_recipe)

  df.to_csv(csv_file_path, index=False)