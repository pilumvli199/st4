import time
from config import INDICES, FNO_STOCKS
from login.angel_login import angel_login
from data.data_fetch import fetch_instruments, fetch_option_chain
from analysis.option_chain_analysis import analyze_option_chain
from ai.gpt_trade import gpt_trade_decision
from alerts.telegram_bot import send_telegram_alert

def run_bot():
    obj, jwt_token, refresh_token = angel_login()
    if not jwt_token:
        print("❌ Login failed, skipping cycle")
        return

    df = fetch_instruments()
    symbols = INDICES + FNO_STOCKS

    for symbol in symbols:
        try:
            expiry = df[df["symbol"] == symbol]["expiry"].min()
            chain = fetch_option_chain(obj.api_key, obj.client_id, jwt_token, symbol, expiry)

            if chain.empty:
                print(f"⚠️ No option chain for {symbol}")
                continue

            summary = analyze_option_chain(chain)
            print(f"\n📊 {symbol} Analysis:", summary)

            gpt_signal = gpt_trade_decision(symbol, summary)
            print(f"⚡ {symbol} Signal:", gpt_signal)

            # ✅ Send Telegram Alert
            alert_msg = f"⚡ {symbol} Trade Signal\n{gpt_signal}"
            send_telegram_alert(alert_msg)

        except Exception as e:
            print(f"⚠️ Error processing {symbol}: {e}")

if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(300)
