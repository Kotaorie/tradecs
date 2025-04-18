import requests
from supabase import create_client, Client
import time
import re

# Supabase setup
url = "https://yxqrlkwtgvwwdpepqvkp.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4cXJsa3d0Z3Z3d2RwZXBxdmtwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMTAwMTIsImV4cCI6MjA1OTU4NjAxMn0.dCNgB4M0nMX6b7BipaLukYZeL5ripmrOH6cnr4Lifec"

supabase: Client = create_client(url, key)

# Request headers to simulate a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Referer": "https://steamcommunity.com/market/",
}

WEAR_MAP = {
    "Factory New": "bca54d16-e962-47cb-996f-cf68a32896ea",
    "Minimal Wear": "bd92534f-ca55-4ca9-a9fb-45ae3799e036",
    "Field-Tested": "18b4f8e5-e41e-4d09-9f14-282b8685e546",
    "Well-Worn": "34404936-2d1d-4161-8bd9-3aa1b1926d27",
    "Battle-Scarred": "c605ec91-ae5d-4a20-a642-3f9806071efc"
}

# Start pagination
start = 17200
count = 100

while True:
    steam_url = f"https://steamcommunity.com/market/search/render/?query=appid%3A730&start={start}&count={count}&norender=1&l=fr"
    response = requests.get(steam_url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error fetching data at start={start}")
        break

    data = response.json()
    results = data.get("results", [])
    
    if not results:
        break  # Done

    for item in results:
        hash_name = item.get("hash_name")
        wear_match = re.search(r'\((.*?)\)', hash_name)
        wear = wear_match.group(1) if wear_match else None
        wear_id = WEAR_MAP.get(wear)

        is_stattrak = hash_name.startswith("StatTrak™")
        name_without_wear = re.sub(r'\s*\(.*?\)', '', hash_name).strip()

        # Remove "StatTrak™ " from the front if it's there
        clear_name = re.sub(r'^StatTrak™\s+', '', name_without_wear)

        price_text = item.get("sell_price_text")
        price = item.get("sell_price")

        if not clear_name or price is None:
            print(f"⚠️ Missing data for item: {clear_name}")
            continue

        # Build update fields
        update_fields = {}

        if is_stattrak:
            update_fields["statrack_skin_price"] = price
            update_fields["statrack_skin_price_text"] = price_text
        else:
            update_fields["sell_price"] = price
            update_fields["sell_price_text"] = price_text

        try:
            response = supabase.table("skin") \
                .update(update_fields) \
                .eq("name", clear_name) \
                .eq("usureId", wear_id) \
                .execute()
        
        except Exception as e:
            print(f"❌ Exception for {clear_name}: {e}")

    start += count
    time.sleep(2)  # Avoid rate-limiting
