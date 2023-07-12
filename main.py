import os
import configparser
import datetime
import asyncio
import requests
import threading as th

config = configparser.ConfigParser()

dir_conf = str(os.path.dirname(__file__)+"\config.txt")
config.read(dir_conf)

domains = (config["default"]["Domains"])
domains = domains.replace(" ","")
domains = domains.split(",")
account_id = config["default"]["Account_id"]
contact_id = config["default"]["Contact_id"]
auth_token = config["default"]["Auth_token"]
time_start = config["default"]["Time_start"]
time_start = time_start.split(":")
time_end = config["default"]["Time_end"]
time_end = time_end.split(":")
retry_rate = config["default"]["Retry_rate"]
testmode = config["default"]["Test"]
timer = config["default"]["Timer"]

def countdown():
    print("timer hit 0")  
    os._exit(1)
   
S = th.Timer(int(timer)*60, countdown) 

with open(str(os.path.dirname(__file__)+"\log_success.txt"), "w") as s:
    s.write("created " + str(datetime.datetime.now()) + "\n")
    s.close()    

with open(str(os.path.dirname(__file__)+"\log_fail.txt"), "w") as f:
    f.write("created " + str(datetime.datetime.now())+ "\n")
    f.close()

async def test(dom):
    url = "https://api.sandbox.dnsimple.com/v2/" + str(account_id) + "/registrar/domains/" + str(dom) + "/registrations"
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
    "registrant_id": int(contact_id)
    }
    r = requests.post(url, data=data, headers=headers)
    print(dom, r.json)
    if r.status_code == 201 or r.status_code == 202:
        with open(str(os.path.dirname(__file__)+"\log_success.txt"), "a") as s:
            s.write(f"{datetime.datetime.now()} : {dom} successfully registered" + "\n")
            s.close()
    else:
        with open(str(os.path.dirname(__file__)+"\log_fail.txt"), "a") as f:
            f.write(f"{datetime.datetime.now()} : failed to register {dom}" + "\n")
            f.close()
        
    await asyncio.sleep(float(retry_rate))
        
async def request(dom):
    url = "https://api.dnsimple.com/v2/" + str(account_id) + "/registrar/domains/" + str(dom) + "/registrations"
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
    "registrant_id": int(contact_id)
    }
    r = requests.post(url, data=data, headers=headers)
    print(dom, r.json)
    if r.status_code == 201 or r.status_code == 202:
        with open(str(os.path.dirname(__file__)+"\log_success.txt"), "a") as s:
            s.write(f"{datetime.datetime.now()} : {dom} successfully registered" + "\n")
            s.close()
    else:
        with open(str(os.path.dirname(__file__)+"\log_fail.txt"), "a") as f:
            f.write(f"{datetime.datetime.now()} : failed to register {dom}" + "\n")
            f.close()
            
    await asyncio.sleep(float(retry_rate))

async def spawn_task():
    task_list = []
    for domain in domains:
        with open(str(os.path.dirname(__file__)+"\log_success.txt"), "r") as s:
            success = s.read()
            if domain not in success:
                if testmode == True:
                    task_list.append(asyncio.create_task(test(domain)))
                else:
                    task_list.append(asyncio.create_task(request(domain)))
        
    await asyncio.gather(*task_list)

if __name__ == "__main__":
    now = datetime.datetime.now()
    start_at = now.replace(hour=int(time_start[0]), minute=int(time_start[1]), second=int(time_start[2]), microsecond=0)
    end_at = now.replace(hour=int(time_end[0]), minute=int(time_end[1]), second=int(time_end[2]), microsecond=0)
    while now < start_at and now < end_at:
        now = datetime.datetime.now()
    if (now > start_at) and (now < end_at) and (int(timer) != 0):
        S.start() 
    while now > start_at and now < end_at:
        asyncio.run(spawn_task())