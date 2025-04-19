import multiprocessing
import requests
import time
import random
from fake_useragent import UserAgent
from supabase import create_client, Client

# --- CONFIGURATION ---

API_KEYS = ["API_KEY_1", "API_KEY_2", "API_KEY_3", "API_KEY_4", "API_KEY_5"]
PROXIES = [
    "http://user:pass@ip1:port",
    "http://user:pass@ip2:port",
    "http://user:pass@ip3:port",
    "http://user:pass@ip4:port",
    "http://user:pass@ip5:port",
]
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-api-key"
TABLE_NAME = "skins_data"

TOTAL_SKINS = 100_000
NUM_BOTS = 5
BATCH_SIZE = 100
PER_BOT = TOTAL_SKINS // NUM_BOTS
COUNT = 100
CALLS_PER_BOT = PER_BOT // COUNT


# --- FUNCTIONS ---

def insert_batch(supabase: Client, batch, table):
    if not batch:
        return
    try:
        supabase.table(table).insert(batch).execute()
        print(f"Inserted {len(batch)} records to Supabase.")
        batch.clear()
    except Exception as e:
        print(f"Batch insert failed: {e}")


def fetch_data(start, count, calls, proxy, api_key, bot_id):
    ua = UserAgent()
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    batch = []

    session = requests.Session()
    session.proxies = {"http": proxy, "https": proxy}
    session.headers.update({"User-Agent": ua.random})

    for i in range(calls):
        url = f"https://api.steampowered.com/your_endpoint?start={start}&count={count}&key={api_key}"

        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()

                # Replace with your real parsing logic
                items = data.get("items", [])  
                for item in items:
                    batch.append({
                        "name": item["name"],
                        "price": item["price"],
                        "skin_id": item["id"]
                    })

                insert_batch(supabase, batch, TABLE_NAME)

                print(f"[Bot {bot_id}] Fetched {len(items)} items from {start}")
            else:
                print(f"[Bot {bot_id}] Error {response.status_code} at {start}")

        except Exception as e:
            print(f"[Bot {bot_id}] Failed at {start}: {e}")

        time.sleep(random.uniform(0.4, 1.2))  # Anti-detection delay
        start += count

    insert_batch(supabase, batch, TABLE_NAME)


def main():
    processes = []

    for i in range(NUM_BOTS):
        start = i * PER_BOT
        proxy = PROXIES[i]
        key = API_KEYS[i]
        p = multiprocessing.Process(
            target=fetch_data,
            args=(start, COUNT, CALLS_PER_BOT, proxy, key, i + 1)
        )
        p.start()
        processes.append(p)
        time.sleep(2)  # Staggered start

    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
