
import requests

BOT_TOKEN = "8887448104:AAHuCySZjxPLmo8s_1g93-LfFWEaGSrjFpM"
CHAT_ID = "1473474086"

message = """
🚨 PRANSTHAMBH TEST ALERT 🚨

✅ Telegram Connected Successfully

System: PRANSTHAMBH AI
Status: ONLINE
Pole ID: POLE_001

This is a test message.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=10
)

print("Status Code:", response.status_code)
print("Response:", response.text)