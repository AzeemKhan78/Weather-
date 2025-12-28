import requests
import time
import sys

print("Bot starting...")
sys.stdout.flush()

BOT_TOKEN = "8438796872:AAEtrjfPgsjIEYjRdjWnJRkfqu6CGC4KQxk"
API_KEY = "11f04d652b2e45259d5144428252812"
CITY = "Dehradun"

telegram = f"https://api.telegram.org/bot{BOT_TOKEN}"
last_id = 0

print("Bot running...")
sys.stdout.flush()

while True:
    try:
        updates = requests.get(
            telegram + "/getUpdates",
            params={"offset": last_id + 1},
            timeout=10
        ).json()

        for update in updates.get("result", []):
            last_id = update["update_id"]

            msg = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]

            if msg == "/weather":
                w = requests.get(
                    "https://api.weatherapi.com/v1/current.json",
                    params={"key": API_KEY, "q": CITY},
                    timeout=10
                ).json()

                text = (
                    f"🌤 Weather\n"
                    f"City: {w['location']['name']}\n"
                    f"Temp: {w['current']['temp_c']}°C\n"
                    f"Humidity: {w['current']['humidity']}%"
                )

                requests.post(
                    telegram + "/sendMessage",
                    data={"chat_id": chat_id, "text": text},
                    timeout=10
                )

        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        sys.stdout.flush()
        time.sleep(5)
