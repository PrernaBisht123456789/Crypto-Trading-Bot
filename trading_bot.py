# trading_bot.py

from binance.client import Client
from binance.enums import *
import logging
import sys

# Configure logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        if testnet:
            self.client = Client(api_key, api_secret)
            self.client.API_URL = 'https://testnet.binancefuture.com/fapi/v1'
        else:
            self.client = Client(api_key, api_secret)
        logging.info("Bot initialized")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == ORDER_TYPE_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_LIMIT:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            elif order_type == ORDER_TYPE_STOP_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_STOP_MARKET,
                    stopPrice=price,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_STOP_LOSS_LIMIT:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_STOP_LOSS_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    stopPrice=price,
                    price=price,
                    quantity=quantity
                )
            else:
                raise ValueError("Invalid order type")

            logging.info(f"Order placed: {order}")
            print("Order placed successfully:", order)
        except Exception as e:
            logging.error(f"Error placing order: {str(e)}")
            print("Error placing order:", e)

    def get_balance(self):
        try:
            balance = self.client.futures_account_balance()
            logging.info("Balance fetched")
            return balance
        except Exception as e:
            logging.error(f"Error fetching balance: {str(e)}")
            print("Error fetching balance:", e)

    def get_open_orders(self, symbol):
        try:
            orders = self.client.futures_get_open_orders(symbol=symbol)
            logging.info(f"Open orders fetched: {orders}")
            return orders
        except Exception as e:
            logging.error(f"Error fetching open orders: {str(e)}")
            print("Error fetching open orders:", e)


def main():
    print("=== Binance Futures Testnet Trading Bot ===")
    api_key = input("Enter your API Key: ")
    api_secret = input("Enter your API Secret: ")

    bot = BasicBot(api_key, api_secret)

    while True:
        print("\n1. Place Market Order\n2. Place Limit Order\n3. Place Stop-Market Order\n4. Check Balance\n5. View Open Orders\n6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            symbol = input("Enter symbol (e.g. BTCUSDT): ").upper()
            side = input("Enter side (BUY/SELL): ").upper()
            qty = float(input("Enter quantity: "))
            bot.place_order(symbol, side, ORDER_TYPE_MARKET, qty)

        elif choice == "2":
            symbol = input("Enter symbol (e.g. BTCUSDT): ").upper()
            side = input("Enter side (BUY/SELL): ").upper()
            qty = float(input("Enter quantity: "))
            price = float(input("Enter price: "))
            bot.place_order(symbol, side, ORDER_TYPE_LIMIT, qty, price)

        elif choice == "3":
            symbol = input("Enter symbol (e.g. BTCUSDT): ").upper()
            side = input("Enter side (BUY/SELL): ").upper()
            qty = float(input("Enter quantity: "))
            stop_price = float(input("Enter stop price: "))
            bot.place_order(symbol, side, ORDER_TYPE_STOP_MARKET, qty, stop_price)

        elif choice == "4":
            balance = bot.get_balance()
            print(balance)

        elif choice == "5":
            symbol = input("Enter symbol (e.g. BTCUSDT): ").upper()
            orders = bot.get_open_orders(symbol)
            print(orders)

        elif choice == "6":
            print("Exiting bot...")
            sys.exit()

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
