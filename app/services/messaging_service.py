import requests

def send_whatsapp(company, phone, message):
    url = f"https://graph.facebook.com/v19.0/{company.phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {company.whatsapp_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=payload)