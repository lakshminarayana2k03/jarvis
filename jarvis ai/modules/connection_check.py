import requests

def check_online_status():
    try:
        requests.get("https://www.google.com", timeout=2)
        return True
    except:
        return False
