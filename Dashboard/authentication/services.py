# services.py
from twilio.rest import Client
from django.conf import settings

def send_verification_code(phone_number, verification_code):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'رمز التحقق الخاص بك هو: {verification_code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return message.sid
    except Exception as e:
        print(f"فشل ارسال SMS: {e}")
        return None
