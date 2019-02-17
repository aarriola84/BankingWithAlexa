# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

customerId = '5c685e91322fa06b677946aa'
Id = '5c6868196759394351bec069'
apiKey = '545cdbbdcc6fba18396e01874ef112e5'

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
urlCREATE = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)
urlALL = 'http://api.reimaginebanking.com/accounts?key={}'.format(apiKey)

def createCustomer():
    firstName = input("Enter Your First Name: ")
    lastName = input("Enter Your Last Name: ")
    streetNumber = input("Enter Your Street Number: ")
    streetName = input("Enter Your Street Name: ")
    city = input("Enter Your City Name: ")
    # NOTE STATE MUST BE TWO LETTERS OTHERWISE STRING DOESN"T WORK
    state = input("Enter Your State (Two letters Tx): ")
    zip = input("Enter Your Zip code: " )

    payload = {
    "first_name": firstName,
    "last_name": lastName,
    "address": {
        "street_number": streetNumber,
        "street_name": streetName,
        "city": city,
        "state": state,
        "zip": zip
        }
    }

    response = request.post(
        urlCREATE,
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        )

    responseOutput = response.json()

    print(responseOutput['code'])
    print(responseOutput['message'])


def createAccount():
    # MAKE SURE EVERY ACCOUNT HAS A UNIQUE NICKNAME
    customerSingle = requests.get(url)
    userAccount = customerSingle.json()

    # customerSingle = requests.get(url)
    #
    # r = customerSingle.json()
    #
    for n in userAccount:
        print(n['nickname'])

    typeAccount = input("Enter Account Type: ")
    nicknameAccount = input("Enter a Nickname for the Account: ")

    for n in userAccount:
        print(n['nickname'])
        if n['nickname'] == nicknameAccount:
            nickname = input("Nickname already exists. Enter a unique nickname for your account: ")

        # rewardsTotal = input("Enter the Rewards Total: ")
        # balanceTotal = input("Enter the Account Balance: ")
        rewardsTotal = 123
        balanceTotal = 321

    for nick in userAccount:
        print("Nickname: ", nick['nickname'] )

    payload = {
        "type": typeAccount,
        "nickname": nicknameAccount,
        "rewards": rewardsTotal,
        "balance": balanceTotal,
        }
    # Create a new Account
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        )

    resonseOutput = response.json()
    print(responseOutput['code'])
    print(responseOutput['message'])

    if response.status_code == 201:
        print('account created')
    if response.status_code == 404:
        print("404 ERROR")

def checkNickname():
    hi = 0

def deleteAccount():
    #figure out how to get account iD before sending the delete request url
    customerSingle = requests.get(url)
    userAccount = customerSingle.json()

    # urlDELETEACCOUNT = 'http://api.reimaginebanking.com/accounts/{}?key={}'.format(Id,apiKey)
    # deleteAccount = requests.delete(urlDELETEACCOUNT)
    # responseOutput = deleteAccount.json()

    # print(responseOutput['code'])
    # print(responseOutput['message'])
    # if deleteAccount.status_code == 204:
    #     print("Account REMOVED")
    # else:
    #     print("ERROR")
#
# customerSingle = requests.get(url)
#
# r = customerSingle.json()
#
# for n in r:
#     print(n['_id'])

# allAccounts = requests.get(urlALL)
#
# i = allAccounts.json()
# print(i)

createAccount()
#deleteAccount()
