from matplotlib import pyplot as plt
import requests

def calculate_volume(order_book):
    total_volume = 0
    for order in order_book:
        total_volume += order["pricePerUnit"] * order["amount"]
    return total_volume

def get_volume():
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    lowest_volume_list = {}
    if response.status_code == 200:
        data = response.json()
        for product in data["products"]:
            lowest_volume_list[product] = calculate_volume(data["products"][product]["sell_summary"]) + calculate_volume(data["products"][product]["buy_summary"])
        return lowest_volume_list
if __name__ == "__main__":
    min_volume = input("Enter the minimum volume: ")
    volume_list = get_volume()
    sorted_list = sorted(volume_list.items(), key=lambda x: x[1])
    sorted_list = [(item, value) for item, value in sorted_list if value > int(min_volume)]
    with open ("volume_list.txt", "w") as f:
        for item in sorted_list:
            f.write(f"{item[0]}: {item[1]}\n")