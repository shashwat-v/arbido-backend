# from fyers_apiv3 import fyersModel
# from dotenv import load_dotenv
# import os
# import json

# # Load secrets from .env
# load_dotenv()
# client_id = os.getenv("CLIENT_ID")

# # Load token from access_token.json
# with open("access_token.json", "r") as f:
#     access_token = json.load(f)["access_token"]

# # Create and export fyers client instance
# fyers = fyersModel.FyersModel(
#     client_id=client_id,
#     is_async=False,
#     token=access_token,
#     log_path="logs"
# )