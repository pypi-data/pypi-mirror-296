import requests
from Crlfi.utils import url


def sendmessage(vuln):
    data = {"chat_id": 1075128712,"text":f"Bug Name: CRLFI\n{vuln}\nBlog:{url.data.blog}\nPriority: Medium"}
    header = {
        "Content-Type":"application/json"
    }
    try:
        response = requests.post(url.data.telegram,json=data,headers=header)
        if response.status_code == 200:
            print("Message send Successfully")
        else:
            print(f"Failed to send message:{response.status_code}-{response.text}")
    except Exception as e:
        print(f"Bot Error:{e}")