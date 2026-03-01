import requests

def send_whatsapp_message(phone_number, text):
    url = "https://graph.facebook.com/v19.0/YOUR_PHONE_NUMBER_ID/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": text}
    }

    requests.post(url, headers=headers, json=payload)