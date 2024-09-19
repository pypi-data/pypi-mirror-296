import requests
from requests.utils import requote_uri
from Crlfi.inculdes import writefile
from Crlfi.inculdes import bot

def crlfscan(url,output):
    try:
        with requests.Session() as session:
            payreq = session.get("https://raw.githubusercontent.com/Cappricio-Securities/PayloadAllTheThings/main/crlfi.txt")
            for endpoint in payreq.text.splitlines():
                encode = requote_uri(endpoint)
                fullurl = f'{url}/{endpoint}'
                try:
                    response = session.get(fullurl,verify=False,allow_redirects=False,timeout=5)
                    crlfhead = response.headers.get("crlfi",None)
                    crlfcook = response.headers.get('Set-Cookie',None)
                    if crlfhead or (crlfcook and 'cappriciosec' in crlfcook):
                        outputprint = (f"\n[Vulnerable] ====> "
                                       f"{url}\n"
                                       f"PoC-Url -> ${fullurl}\n")
                        print(outputprint)
                        if output is not None:
                            writefile.write(output,str(f"{fullurl}\n"))
                        if True:
                            bot.sendmessage("vulnerable: "+fullurl)
                        break
                    else:
                        print("not working")
                except requests.exceptions.RequestException as e:
                    print(f'invalid URL ->${fullurl}')
    except requests.exceptions.RequestException as e:
        print(f"Check Network Connect")