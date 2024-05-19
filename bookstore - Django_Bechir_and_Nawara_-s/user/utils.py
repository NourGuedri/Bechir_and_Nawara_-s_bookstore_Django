from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


from dotenv import load_dotenv
load_dotenv()
import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')


def send_verification_code(phone_number, code,first_name):
    print("===============================================> code: ",code)
    print(TWILIO_ACCOUNT_SID)
    print(TWILIO_AUTH_TOKEN)
    print(TWILIO_NUMBER)
    print(phone_number)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Hello {first_name}, Your Bechir And Nawara's verification code is {code}",
        from_=TWILIO_NUMBER,  
        to=phone_number
    )

    return message.sid


