import requests
from datetime import datetime
import time
def get_fair_value(item):
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    if response.status_code == 200:
        data = response.json()
        sellPrice = data["products"][item]["quick_status"]["sellPrice"]
        buyPrice = data["products"][item]["quick_status"]["buyPrice"]
        fair_value = (sellPrice + buyPrice) / 2
        return fair_value, sellPrice, buyPrice
    else:
        print("Failed to fetch fair value")
        return None
def record():
    item = input("Input the item: ")  
    filename = "/home/bazyl/bazaarorderbook/dailyfluctuations/price_records/price_records"  
    
    while True:
        try:
            fair_value, sellprice, buyprice = get_fair_value(item)
            actual_file_name = filename + "_" + item + ".txt"
            with open (actual_file_name, "a") as f:
                f.write(f"{datetime.now()}; sellprice: {sellprice}; buyprice: {buyprice}; avg: {fair_value}")
                time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)
def calculate_fluctuations(filename, ):
    try:
        with open (filename, "r") as f:
            file = f.read()
        
    except Exception as e:
        print(f"japierdole")
    
if __name__ == "__main__":
    record()