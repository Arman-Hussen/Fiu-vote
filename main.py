import requests
import json
import random
import time

# Random FIU email generate
def generate_random_email():
    random_number = random.randint(10000, 999999)
    return f"fiu{random_number}@university.edu"

# Step 1: Token neoar jonno request
def get_access_token(email):
    url = "https://uni-cup.abgsportscity.com/api/auth/request-link"
    payload = {"email": email}

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Google Chrome\";v=\"157\", \"Chromium\";v=\"157\"",
        'sec-ch-ua-mobile': "?1",
        'Origin': "https://uni-cup.abgsportscity.com",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://uni-cup.abgsportscity.com/",
        'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=15)

        if response.status_code == 429:
            return "RATE_LIMIT"

        data = response.json()
        if data.get("ok"):
            return data.get("accessToken")
    except Exception as e:
        print(f"   [!] Token error: {e}")
    return None

# Step 2: Vote cast
def cast_vote(access_token, university_id=4):
    url = "https://uni-cup.abgsportscity.com/api/votes"
    payload = {"universityId": university_id}

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=15)

        if response.status_code == 429:
            return "RATE_LIMIT"

        return response.json()
    except Exception as e:
        print(f"   [!] Vote error: {e}")
        return None

# Main loop: ekta ekta vote, 429 ashle 60 sec wait
def main():
    count = 0
    total_success = 0
    total_fail = 0

    print("🔁 Vote Loop Started (one by one)...")
    print("⚠️  429 error hole 60 sec wait korbe.\n")

    while True:
        count += 1
        email = generate_random_email()
        print(f"\n[{count}] Email: {email}")

        token = get_access_token(email)

        # 429 handle — token step
        if token == "RATE_LIMIT":
            print("   ⚠️ 429 Too Many Requests — waiting 60 seconds...")
            time.sleep(60)
            print("   🔄 Retrying same email...")
            token = get_access_token(email)

            if token == "RATE_LIMIT":
                print("   ❌ Still rate-limited, skipping...")
                total_fail += 1
                print(f"   📊 Total — ✅ {total_success} | ❌ {total_fail}")
                continue

        if not token:
            print("   ❌ Token failed")
            total_fail += 1
            print(f"   📊 Total — ✅ {total_success} | ❌ {total_fail}")
            continue

        result = cast_vote(token)

        # 429 handle — vote step
        if result == "RATE_LIMIT":
            print("   ⚠️ 429 Too Many Requests on vote — waiting 60 seconds...")
            time.sleep(60)
            print("   🔄 Retrying vote...")
            result = cast_vote(token)

            if result == "RATE_LIMIT":
                print("   ❌ Still rate-limited, skipping...")
                total_fail += 1
                print(f"   📊 Total — ✅ {total_success} | ❌ {total_fail}")
                continue

        if result and result.get("ok"):
            total_success += 1
            print(f"   ✅ VOTED SUCCESS -> {result.get('universityName')}")
            print(f"   📩 {result.get('message')}")
        else:
            total_fail += 1
            print(f"   ❌ Vote failed: {result}")

        print(f"   📊 Total — ✅ {total_success} | ❌ {total_fail}")

        # prottek vote er por choto delay
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Loop stopped by user.")