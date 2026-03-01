import requests

# =========================
# SEND INSTAGRAM1
# =========================

def send_instagram(user_id, message):
    url = f"https://graph.facebook.com/v19.0/{os.getenv('IG_BUSINESS_ID')}/messages"

    headers = {
        "Authorization": f"Bearer {INSTAGRAM_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "instagram",
        "recipient": {"id": user_id},
        "message": {"text": message}
    }

    response = requests.post(url, headers=headers, json=data)
    print("INSTAGRAM STATUS:", response.status_code, response.text)