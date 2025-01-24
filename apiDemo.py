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
    
    rsp = "[TSLA_US_EQ] Tesla, Inc. Given your high-risk tolerance and interest in the tech sector, Tesla presents an attractive investment opportunity. With a current price around £200, you could purchase approximately [115] shares for a total investment of £23,000, aiming for a short-term gain over the next three months as the EV market continues to grow and Tesla releases new production updates."
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