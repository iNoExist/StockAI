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

def buyStonks(tkr: str, qty: float ):
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


def dessembler2(rsp: str):
    print("analysing response... ... ...")
    
    rsp = """  [NVDA_US_EQ]  
NVIDIA Corporation

NVIDIA is well-positioned in the tech sector, particularly in AI and gaming, which are expected to see significant growth in the coming months. With an investment of £11,000, you could purchase approximately [55] shares at a price of £200 per share, making this a suitable high-risk investment for the 3-month timeframe."""
    # for a given response find the tkr (first set of square brackets)
    indx1 = rsp.find("[")
    indx2 = rsp.find("]")

    # the tkr sub string
    subStrTkr = rsp[indx1+1:indx2+indx1]

    # temporarly remove the first with empty space to find the second
    rsp = rsp.replace(subStrTkr, "")
    rsp = rsp.replace("[]", "")
    # find the qty (second set of square brackets)
    # for a given response find the tkr (first set of square brackets)
    indx1 = rsp.find("[")
    indx2 = rsp.find("]")

    # the qty sub string
    subStrQty = rsp[indx1+1:indx2-1]
    
    print("this is ticker: ", subStrTkr , " this is quantity: " , subStrQty)

    buyStonks(subStrTkr, int(subStrQty))


dessembler2("")