import csv
import requests

# File paths
csv_file_path = 'filtered_rows.csv'
collections_lookup_path = 'collections_rows.csv'
output_csv_file_path = 'collection.csv'

# Load Mykel skin data
url = 'https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/fr/skins.json'
response = requests.get(url)
data = response.json()

# Build lookup for skins by name
skin_lookup = {item['name']: item for item in data}

# 🔁 Load collection name → ID mapping from your own CSV
collection_name_to_id = {}

with open(collections_lookup_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row.get('name')
        cid = row.get('id')  # or 'collection_id' depending on your column name
        if name and cid:
            collection_name_to_id[name] = cid

# Final output
output_rows = []

with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        weapon_name = row['name']
        matched_skin = skin_lookup.get(weapon_name)

        if matched_skin:
            collections = matched_skin.get('collections', [])
            if collections:
                collection_name = collections[0]['name']
                collection_id = collection_name_to_id.get(collection_name, 'Unknown')
                row['collection'] = collection_id
            else:
                row['collection'] = 'Unknown'
        else:
            row['collection'] = 'Not found'

        output_rows.append(row)

# Save to output CSV with collection ID instead of name
fieldnames = output_rows[0].keys()

with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

print(f"✅ Collection IDs saved in {output_csv_file_path}")
