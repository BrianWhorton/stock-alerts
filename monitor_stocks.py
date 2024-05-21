import yfinance as yf
from twilio.rest import Client
import schedule
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
my_phone_number = os.getenv('MY_PHONE_NUMBER')

client = Client(account_sid, auth_token)

# List of stocks with low and high price thresholds
stocks = {
    'INDA': (51.10, 54.11),
    'EWN': (49.50, 52.98),
    'AMLP': (46.07, 47.44),
    'CPER': (28.37, 32.17),
    'SLV': (25.28, 29.67),
    'EWG': (31.38, 33.16),
    'UUP': (28.34, 28.98),
    'GLD': (212.00, 226.00),
    'AAAU': (22.67, 24.37),
    'COPX': (46.90, 52.57),
    'GDX': (33.61, 37.89),
    'IVOL': (18.39, 18.87),
    'CRIT': (19.70, 22.48),
    'URA': (30.55, 34.08),
    'DRLL': (30.38, 32.39),
    'MSOS': (8.75, 11.24),
    'KBA': (22.23, 23.64),
    'HYDR': (5.24, 6.20),
    'IDRV': (30.77, 32.44),
    'EWZ': (31.03, 32.74),
    'DKNG': (42.01, 46.77),
    'DIDIY': (4.50, 5.14),
    'CELH': (75.26, 99.92),
    'CAVA': (71.33, 81.28),
    'MPW': (3.84, 5.84),
}

def send_sms(message):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=my_phone_number
    )

def check_stock_prices():
    for symbol, thresholds in stocks.items():
        stock = yf.Ticker(symbol)
        current_price = stock.history(period="1d")['Close'].iloc[-1]

        low_threshold = thresholds[0] * 1.0005
        high_threshold = thresholds[1] * 0.9995

        if current_price <= low_threshold or current_price >= high_threshold:
            message = f"Alert: {symbol} price is {current_price:.2f}, within 0.05% of threshold."
            send_sms(message)

schedule.every(10).minutes.do(check_stock_prices)

while True:
    schedule.run_pending()
    time.sleep(1)
