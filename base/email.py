
from twilio.rest import Client

client = Client("AC78a600694d3dedfbd98a42c2c8efb727","6d0e62f41eaf2d95820baffe87396072")
phone = 9815430168
twilio_phone = "+14325294960"

client.messages.create(
    to = phone,
    from_ = twilio_phone,
    body = "hello Ritsh"
)
print('hello')