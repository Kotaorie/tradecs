import requests
import csv
from supabase import create_client, Client

url = "https://yxqrlkwtgvwwdpepqvkp.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4cXJsa3d0Z3Z3d2RwZXBxdmtwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMTAwMTIsImV4cCI6MjA1OTU4NjAxMn0.dCNgB4M0nMX6b7BipaLukYZeL5ripmrOH6cnr4Lifec"

supabase: Client = create_client(url, key)

# === Step 1: Load all ByMykel skins and build image -> hash_name lookup ===
print("📦 Fetching skin data from ByMykel...")
url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"
response = requests.get(url)
all_skins = response.json()

img_to_hashname = {skin['image']: skin['name'] for skin in all_skins}
print(f"✅ Loaded {len(img_to_hashname)} skins.")

# === Step 2: Load all skins from Supabase ===
print("🧠 Fetching skins from Supabase...")
all_skins = []
batch_size = 1000
for i in range(0, 10000, batch_size):  # Adjust upper bound if needed
    res = supabase.table("skin").select("id", "img_url").range(i, i + batch_size - 1).execute()
    if res.data:
        all_skins.extend(res.data)
    if len(res.data) < batch_size:
        break  # No more data

print(f"✅ Loaded {len(all_skins)} skins.")
# === Step 3: Match and update ===
updated_count = 0

for skin in all_skins:
    img_url = skin.get("img_url")
    skin_id = skin.get("id")
    hash_name = img_to_hashname.get(img_url)

    if not hash_name:
        print(f"❌ No match for skin ID {skin_id} → Supabase img: {img_url}")
        print("👀 ByMykel match candidates:")
        for url in img_to_hashname.keys():
            if img_url.split("/")[-1] in url:
                print("    🔁 Maybe:", url)


    # Update skin with hash_name
    response = supabase.table("skin") \
        .update({"name": hash_name, "lang": "eng"}) \
        .eq("id", skin_id) \
        .execute()

    # if response.ok :
    #     print(f"✅ Updated skin {skin_id} with hash_name: {hash_name}")
    #     updated_count += 1
    # else:
    #     print(f"⚠️ Failed to update skin {skin_id}: {response.data}")

print(f"\n🎉 Done! {updated_count} skins updated with hash names.")
