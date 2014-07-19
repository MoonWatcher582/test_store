from twilio.rest import TwilioRestClient

account_sid = "AC6a2ed3970fc467269387ac7d044a498b"
auth_token = "cccc0ca6c80adb61d27ab2ec1ec0e9aa"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body="Hello World!", to="+17327963185", from_="+17328123770")
print message.sid
