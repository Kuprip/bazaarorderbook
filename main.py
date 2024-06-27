import requests
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt

def get_order_book(item_name):
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    if response.status_code == 200:
        data = response.json()
        buy_order_book = data["products"][item_name]["buy_summary"]
        sell_order_book = data["products"][item_name]["sell_summary"]
        return buy_order_book, sell_order_book
    elif response.status_code == 503:
        print("The data is not yet populated. Please try again later.")
    else:
        print("Failed to fetch order book data (perhaps the item name is incorrect?)")
    return None, None

def update_graph(frame):
    bob, sob = get_order_book(item_name)
    # if bob is not None and sob is not None:
    plt.cla()  # Clear the current plot
    display_data(bob, sob)
    print("Graph should be updated")
    #else: print("failed to fetch update data")

def display_data(buy_order_book, sell_order_book):
    buy_prices = [order["pricePerUnit"] for order in buy_order_book]
    buy_amounts = [order["amount"] for order in buy_order_book]
    sell_prices = [order["pricePerUnit"] for order in sell_order_book]
    sell_amounts = [order["amount"] for order in sell_order_book]
    # for orders in buy_order_book:
    #     print("buy order: " + str(orders))
    # for orders in sell_order_book:
    #     print("sell order: " + str(orders))
    y_positions = range(len(buy_prices) + len(sell_prices))
    combined_prices = buy_prices + sell_prices

    plt.barh(y_positions[:len(buy_prices)], buy_amounts, height=0.4, label='Buy Orders', color='green')
    plt.barh(y_positions[len(buy_prices):], sell_amounts, height=0.4, label='Sell Orders', color='red')

    plt.yticks(y_positions, labels=[f"${price}" for price in combined_prices])

    plt.xlabel("Amount")
    plt.ylabel("Price Per Unit")
    plt.title("Order Book Data")
    plt.legend()

item_name = input("Enter the item name: ")
bob, sob = get_order_book(item_name)
display_data(bob, sob)

ani = FuncAnimation(plt.gcf(), update_graph, interval=10000, cache_frame_data=False)  # Update every 10 seconds
plt.show()
