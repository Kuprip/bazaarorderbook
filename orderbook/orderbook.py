import requests
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

#set the size of the window on spawn
plt.figure(figsize=(10, 12))
#function listing the name of all items as categorized by the hypixel api
def calculate_volume(order_book):
    total_volume = 0
    for order in order_book:
        total_volume += order["pricePerUnit"] * order["amount"]
    return total_volume


def list_items():
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    if response.status_code == 200:
        data = response.json()
        items = data["products"].keys()
        for item in items:
            print(item)
    else:
        print("Failed to fetch item list")
#gets the order book data for a specific item
def get_order_book(item_name):
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    if response.status_code == 200:
        data = response.json()
        buy_order_book = data["products"][item_name]["sell_summary"]
        sell_order_book = data["products"][item_name]["buy_summary"]
        return buy_order_book, sell_order_book
    elif response.status_code == 503:
        print("The data is not yet populated. Please try again later.")
        return None, None
    else:
        print("Failed to fetch order book data (perhaps the item name is incorrect?)")
        return None, None

#function to update the graph, called by the animation function
def update_graph(frame):
    #idk what the (frame) is for but it's necessary for the function to work
    bob, sob = get_order_book(item_name)
    plt.cla()  # Clear the graph
    display_data(bob, sob)
    print("Graph updated")

def display_data(buy_order_book, sell_order_book):
    #get the prices and amounts of the orders
    buy_prices = [order["pricePerUnit"] for order in buy_order_book]
    buy_amounts = [order["amount"] for order in buy_order_book]
    sell_prices = [order["pricePerUnit"] for order in sell_order_book]
    sell_amounts = [order["amount"] for order in sell_order_book]  
    #create y positions for the bars
    y_positions = range(len(buy_prices) + len(sell_prices)) 
    
    buy_positions = range(len(buy_prices))
    sell_positions = range(len(buy_prices), len(buy_prices) + len(sell_prices))
    # Plotting the data
    plt.barh(list(buy_positions), buy_amounts, height=0.4, label='Buy Orders', color='green')
    plt.barh(list(sell_positions), sell_amounts, height=0.4, label='Sell Orders', color='red')
    #we needa fuck around a little bit in order to display the prices in 
    #consistnent intervals
    combined_prices = buy_prices + sell_prices
    combined_prices.sort()
    plt.yticks(y_positions, labels=[f"${price}" for price in combined_prices])

    plt.xlabel("Amount")
    plt.ylabel("Price")
    plt.title("Order Book")
    plt.legend()

if input("Do you want to list all available items? (y/n): ") == "y":
    list_items()
item_name = input("Enter the item name: ")
bob, sob = get_order_book(item_name)
display_data(bob, sob)

ani = FuncAnimation(plt.gcf(), update_graph, interval=5000, cache_frame_data=False)  # Update every 5 seconds

plt.show()