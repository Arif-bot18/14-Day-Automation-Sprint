import requests , os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("url")

if not url:
    raise ValueError("Enter The URL Correctly ")
try:
    result = requests.get(url)
    if result.status_code == 200 :

        res = result.json()
        currency = res["conversion_rates"]
        try:
            have_currency = input("Enter Your Currency Name: ").upper() 
            want_change = input("Enter The Currency You Want To Change: ").upper()
        except ValueError:
            print("Enter The currency name like [INR,USD,EUR]")
        try:
            amount_currency = float(input(f"Enter The Amount In {have_currency} : "))
            target_currency = amount_currency*currency[want_change]/currency[have_currency]     
            print(target_currency)
        except ValueError:
            print("Enter Amount In Int Like (100,2000) ")
    else :
        print("Failed To Feach The Data")
            
except Exception as e:
    print(f"The Error Is {e}")