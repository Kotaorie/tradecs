# Nuxt Minimal Starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

To inplement for scrap price : 

Absolutely — here's a clean **step-by-step plan to scrape 10,000 skins using AWS Lambda for free**, assuming the API allows `?start=X&count=100`.

---

## 🎯 **Goal:**  
Scrape 10,000 skins (in batches of 100) using AWS Lambda for speed, efficiency, and free-tier goodness.

---

## 🧩 Basic Strategy:

1. **Split the work**:  
   10,000 skins ÷ 100 = **100 API calls**
   
2. **Parallelize** with **multiple Lambda functions** or **one Lambda function triggered multiple times** with different `start` values.

3. **Trigger** via:
   - AWS SDK (e.g. Python script calls Lambda in a loop)
   - AWS Step Functions (for chaining or managing parallelism)
   - CloudWatch if you want to do it on schedule

4. **Each Lambda**:
   - Gets a `start` (0, 100, 200...9900)
   - Makes 1–5 API calls (loop inside Lambda)
   - Pushes result to Supabase

---

## 🛠️ Step-by-Step Setup

### 1. **Write the Lambda Function (`lambda_function.py`)**

```python
import requests
from supabase import create_client, Client

# Supabase config
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "your_anon_or_service_role_key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def lambda_handler(event, context):
    start = event["start"]  # e.g. 0, 100, 200...
    count = event.get("count", 100)

    api_url = f"https://steamapi.url/path?start={start}&count={count}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        # Batch insert to Supabase (assuming "skins" table)
        supabase.table("skins").insert(data["items"]).execute()
        return {"status": "success", "start": start}
    else:
        return {"status": "error", "start": start, "code": response.status_code}
```

---

### 2. **Prepare for Deployment**

- Create a folder: `lambda_scraper/`
- Add: `lambda_function.py`, `requirements.txt`

```txt
# requirements.txt
requests
supabase
```

- Zip it:
```bash
pip install -t ./package -r requirements.txt
cd package
zip -r ../lambda_scraper.zip .
cd ..
zip -g lambda_scraper.zip lambda_function.py
```

---

### 3. **Deploy to AWS Lambda**

- Go to AWS Console → Lambda → Create Function → Upload ZIP
- Set runtime: Python 3.11+
- Set timeout: e.g. 5 minutes
- Add environment variables or secrets if needed

---

### 4. **Trigger Multiple Lambda Calls (to handle all 10,000)**

You can do this **in a script** (from local machine, EC2, or even another Lambda):

```python
import boto3

lambda_client = boto3.client("lambda", region_name="us-east-1")

for start in range(0, 10000, 100):
    lambda_client.invoke(
        FunctionName="YourLambdaFunctionName",
        InvocationType="Event",  # async
        Payload=json.dumps({"start": start})
    )
```

⚠️ Free tier gives **1M requests + 400,000 GB-seconds/month**, so you’re good unless you go crazy.

---

### ✅ Done!

Each Lambda does:
- Pull 100 skins
- Insert into Supabase
- Exit

In total, you'll scrape **10,000 items fast, in parallel**, and **stay free-tier compliant**.

---

## 🔥 Optional Enhancements

| Feature | How |
|--------|------|
| 📆 Schedule | Use **CloudWatch Events** to auto-run |
| 🧠 Retry logic | Catch and retry failed inserts |
| 📡 Static IP | Use **NAT Gateway** (not free) |
| 🧪 Testing | Run one test Lambda with `{"start": 0}` to validate |

---

Wanna copy-paste a ready-made ZIP + deploy guide or make it work with Step Functions? Just say the word 🙌
