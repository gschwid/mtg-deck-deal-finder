import requests
from proxy_checker import ProxyChecker
import random
import time


def get_proxy():

    # Grabbing all the proxies from a text file that was pulled from github (https://github.com/TheSpeedX/PROXY-List)
    f = open("PROXY-List/http.txt", "r")
    proxies = [line.strip() for line in f]
    print(proxies)
    f.close()

    # Randomly checking proxies until one is found
    for proxy in proxies:
        rand = random.randint(0,len(proxies))
        rand_proxy = proxies[rand]
        rand_ip = rand_proxy.split(":")

        proxies_dict = {
        "http": f"http://{rand_proxy}/",
        "https": f"http://{rand_proxy}/"
        }

        url = 'https://api.ipify.org'

        try:
            response = requests.get(url, proxies=proxies_dict, timeout=2)
            assert response.text==rand_ip[0]
            print(f'{proxy} works! yaaaay')
            return proxy
        except:
            print("Proxy does not work")

    
get_proxy()




