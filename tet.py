import csv
from supabase import create_client, Client

# 🧾 Load your CSV
csv_file_path = 'collection.csv'

# 🔐 Supabase setup
url = "https://yxqrlkwtgvwwdpepqvkp.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4cXJsa3d0Z3Z3d2RwZXBxdmtwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMTAwMTIsImV4cCI6MjA1OTU4NjAxMn0.dCNgB4M0nMX6b7BipaLukYZeL5ripmrOH6cnr4Lifec"
supabase: Client = create_client(url, key)

# 📤 Update loop
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        weapon_name = row['name']
        collection_id = row['collection']

        if collection_id in ['Unknown', 'Not found', '', None]:
            print(collection_id)
            print(f"⚠️ Skipping {weapon_name} — Invalid collection ID")
            continue

        # Update the row in Supabase
        response = supabase.table('skin').update({'collectionId': collection_id}).eq('name', weapon_name).execute()

        # if response.status_code == 200:
        #     print(f"✅ Updated: {weapon_name}")
        # else:
        #     print(f"❌ Failed: {weapon_name} — {response.status_code} — {response.data}")
