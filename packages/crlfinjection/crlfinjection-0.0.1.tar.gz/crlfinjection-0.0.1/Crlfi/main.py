from Crlfi.utils import internet_checker
from Crlfi.utils import banner
from Crlfi.utils import url
from Crlfi.inculdes import file
from Crlfi.inculdes import scan
import argparse
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument('-u',"--url",help="Enter URL")
parser.add_argument('-l',"--list",help="Enter File")
parser.add_argument('-o',"--output",help="Enter Output File name")
parser.add_argument('-b',"--blog",action='store_true',help="FOR MORE INFO")
args = parser.parse_args()

def main():
    if args.url:
        banner.banner()
        scan.crlfscan(args.url,args.output)
    if args.list:
        banner.banner()
        file.reader(args.list,args.output)
    if args.blog:
        webbrowser.open(url.data.blog)

if __name__ == "__main__":
    if internet_checker.net():
        main()
    else:
        print("check internet")