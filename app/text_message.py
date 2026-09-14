import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_PRIMARY_AUTH_TOKEN"))

message = client.messages.create(
    to="+16693361328",       # your verified personal number
    from_=os.getenv("TWILIO_PHONE_NUMBER"),
    body="Test message from my news digest project!"
)

print(message.sid)
