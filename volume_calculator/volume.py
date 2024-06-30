import requests
response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
data = response.json()

def get_fair_value(item):
    sellPrice = data["products"][item]["quick_status"]["sellPrice"]
    buyPrice = data["products"][item]["quick_status"]["buyPrice"]
    fair_value = (sellPrice + buyPrice) / 2
    return fair_value
    
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
    min_volume = int(input("Enter the minimum volume: "))
    min_price = int(input("Enter the minimum price: "))
    volume_list = get_volume()
    sorted_list = dict(sorted(volume_list.items(), key=lambda x: x[1]))
    #print(sorted_list)
    #print(type(sorted_list))
    for item in sorted_list.copy():
        item = (item, sorted_list[item])
        #print(f"item: {item}")
        #print(f"item: {item} item[1]: {item[1]} min_volume: {min_volume} min_price: {min_price} get_fair_value: {get_fair_value(item[0])}")
        
        if int(item[1]) < min_volume or get_fair_value(item[0]) < min_price:
            del sorted_list[item[0]]
            print("niggger")
    #print(sorted_list)
    with open ("volume_calculator/volume_list.txt", "w") as f:
        for item in sorted_list:
            item = (item, sorted_list[item])
            f.write(f"{item[0]}: {item[1]}\n")