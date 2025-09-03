from SmartApi.smartConnect import SmartConnect
import pyotp
import os


def angel_login():
    api_key = os.getenv("ANGEL_API_KEY")
    client_id = os.getenv("ANGEL_CLIENT_ID")
    mpin = os.getenv("ANGEL_MPIN")
    totp_secret = os.getenv("ANGEL_TOTP_SECRET")

    if not api_key or not client_id or not mpin or not totp_secret:
        print("⚠️ Missing login environment variables.")
        return None, None

    smartApi = SmartConnect(api_key=api_key)

    # Generate TOTP dynamically
    totp = pyotp.TOTP(totp_secret).now()

    try:
        data = smartApi.generateSession(client_id, mpin=mpin, totp=totp)
        print("✅ Login success")
        return smartApi, data
    except Exception as e:
        print(f"⚠️ Login Error: {e}")
        return None, None
