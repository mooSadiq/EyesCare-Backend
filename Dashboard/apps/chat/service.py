from onesignal_sdk.client import Client
from config import settings

def send_notification(receiver, sender_name, content, chat_id):
    onesignal_client  = Client(app_id=settings.ONESIGNAL_APP_ID, 
                    rest_api_key=settings.ONESIGNAL_API_KEY)
    
    notification_data = {
        "headings": {
            "ar": f"رسالة من {sender_name}",
            "en": f"Message from {sender_name}"
        },
        "contents": {
            "ar": content if content else "لقد أرسل ملفاً.",
            "en": content if content else "File has been sent."
        },
        "data": {
            "type": "message",
            "chatId": chat_id
        },
        "android_sound": "welcome_sound",
        "target_channel": "push",
        "include_external_user_ids": [str(receiver)]
    }
    try:
        response = onesignal_client.send_notification(notification_data)
        if response.status_code == 200:
            print(f"Notification sent successfully: {response.body}")
        else:
            print(f"Failed to send notification, status code: {response.status_code}, response: {response.body}")
        
    except Exception as e:
        print(f"Failed to send notification: {e}")
