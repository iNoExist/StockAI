import requests

import os


# Then retrieve and print the specific variable
api_key1 = os.getenv('API_KEY1')
print(api_key1)



# url = "https://demo.trading212.com/api/v0/equity/metadata/exchanges"

# headers = {"Authorization": str(api_key1)}

# response = requests.get(url, headers=headers)

# data = response.json()
# print(data)







# to set env var $env:API_KEY1 = "API_"

# function to buy stonks

def buyStonks(tkr: str, qty: int ):
    print("Buying Stocks")
    url = "https://demo.trading212.com/api/v0/equity/orders/market"

    payload = {
    "quantity": qty,
    
    "ticker": tkr
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": str(api_key1)
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    print(data)


buyStonks("TSLA_US_EQ", 0.1)