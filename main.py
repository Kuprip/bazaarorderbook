import requests
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 12))
def list_items():
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    if response.status_code == 200:
        data = response.json()
        items = data["products"].keys()
        for item in items:
            print(item)
    else:
        print("Failed to fetch item list")
def get_order_book(item_name):
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    if response.status_code == 200:
        data = response.json()
        buy_order_book = data["products"][item_name]["sell_summary"]
        sell_order_book = data["products"][item_name]["buy_summary"]
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
    print(f"Buy Prices: {buy_prices}, sell prices: {sell_prices}")
    y_positions = range(len(buy_prices) + len(sell_prices))
    #print("y positions " + str(y_positions))
    combined_prices = buy_prices + sell_prices
    combined_prices.sort()
    buy_positions = range(len(buy_prices))
    sell_positions = range(len(buy_prices), len(buy_prices) + len(sell_prices))
    #print("combined prices " + str(combined_prices))
    # Plotting the data
    plt.barh(list(buy_positions), buy_amounts, height=0.4, label='Buy Orders', color='green')
    plt.barh(list(sell_positions), sell_amounts, height=0.4, label='Sell Orders', color='red')

    plt.yticks(y_positions, labels=[f"${price}" for price in combined_prices])

    plt.xlabel("Amount")
    plt.ylabel("Price Per Unit")
    plt.title("Order Book Data")
    plt.legend()

ifer = input("Do you want to list all available items? (y/n): ")
if ifer == "y":
    list_items()
item_name = input("Enter the item name: ")
bob, sob = get_order_book(item_name)
display_data(bob, sob)

ani = FuncAnimation(plt.gcf(), update_graph, interval=5000, cache_frame_data=False)  # Update every 5 seconds
plt.show()
