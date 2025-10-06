from fyers_apiv3 import fyersModel
from dotenv import load_dotenv
import os
import json
import getpass

load_dotenv()

client_id = os.getenv("CLIENT_ID")
secret_key = os.getenv("SECRET_KEY")
redirect_uri = os.getenv("REDIRECT_URL")
response_type = os.getenv("RESPONSE_TYPE")
grant_type = os.getenv("GRANT_TYPE")

session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
)

response = session.generate_authcode()
print(response)

auth_code = getpass.getpass("Enter the Authorization Code: ")

session.set_token(auth_code)
response = session.generate_token()

access_token = response['access_token']

with open("access_token.json", "w") as f:
    json.dump({"access_token": access_token}, f)
    
print("✅ Access token saved successfully!.")