# account_sid="AC5c209a35464f309a5578f5c9d8feade6"
# token="64b3581215e998f7cf287e20bfbc124d"

import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+916238935672",
    from_="+17372508034",
    body="Booked successfully",
)

print(message.sid)