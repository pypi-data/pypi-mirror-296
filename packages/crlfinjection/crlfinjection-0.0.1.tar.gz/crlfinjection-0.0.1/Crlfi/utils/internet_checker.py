import requests

def net():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False
