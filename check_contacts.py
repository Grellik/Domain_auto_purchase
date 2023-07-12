import os
import configparser
import requests

config = configparser.ConfigParser()

dir_conf = str(os.path.dirname(__file__)+"\config.txt")
dir_script = str(os.path.dirname(__file__)+"\\request.py")
config.read(dir_conf)

account_id = config["default"]["Account_id"]
auth_token = config["default"]["Auth_token"]
testmode = config["default"]["Test"]

print(testmode)
if testmode != True:
    url = "https://api.sandbox.dnsimple.com/v2/" + str(account_id) + "/contacts"
else:
    url = "https://api.dnsimple.com/v2/" + str(account_id) + "/contacts"
headers = {"Authorization": f"Bearer {auth_token}"}

r = requests.get(url,headers=headers).json()
print(r)

input()