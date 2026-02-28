# import requests

# def send_instagram_message(recipient_id, text):
#     url = f"https://graph.facebook.com/v19.0/me/messages?access_token={INSTAGRAM_TOKEN}"

#     payload = {
#         "recipient": {"id": recipient_id},
#         "message": {"text": text}
#     }

#     requests.post(url, json=payload)