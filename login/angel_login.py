from SmartApi.smartConnect import SmartConnect
import pyotp
import os

API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_ID = os.getenv("ANGEL_CLIENT_ID")
PASSWORD = os.getenv("ANGEL_PASSWORD")
TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")

def angel_login():
    try:
        obj = SmartConnect(api_key=API_KEY)
        otp = pyotp.TOTP(TOTP_SECRET).now()
        data = obj.generateSession(CLIENT_ID, PASSWORD, otp)

        if "data" not in data:
            raise Exception("Login failed.")

        jwt_token = data["data"]["jwtToken"]
        refresh_token = data["data"]["refreshToken"]

        print("✅ Angel One Login Successful")
        return obj, jwt_token, refresh_token

    except Exception as e:
        print(f"⚠️ Login Error: {e}")
        return None, None, None
