import dns.resolver
import subprocess
import pyfiglet
import requests
import argparse
import sys

print(pyfiglet.figlet_format(f"{sys.argv[0]}"))

p = argparse.ArgumentParser()
p.add_argument("-u", "--url", type=str, required=True, metavar="", help="URL from target")
p.add_argument("-w", "--wordlist", required=False, metavar="", help="WORDLIST for attack")
a = p.parse_args()

subprocess.check_call("clear")

def resolverIp(url):
    try:
        dns_querys = dns.resolver.query(url, "A")
        for dns_query in dns_querys:
            return dns_query
    except Exception as e:
        print(f"Error: {e}")
        exit()

def main(url, wordlist):
    azul = "\033[1;94m"
    normal = "\033[0;0m"
    header = {"User-Agent":""}
    newUrl = "http://" + url
    newUrlIp = resolverIp(url)
    print(pyfiglet.figlet_format(f"{sys.argv[0]}"))
    print(f"[ {newUrl} => {newUrlIp} ]\n")
    if wordlist == "":
        wordlist = "wordlist.txt"
    try:
        lines = open(wordlist)
    except Exception as e:
        print(f"Error: {e}")
        exit()
    for line in lines.readlines():
        newUrl = "http://" + url + "/" + line.strip()
        try:
            http = requests.get(newUrl, headers=header)
        except Exception as e:
            print(f"Error {e}")
            exit()
        if http.status_code != 404:
            print(f"{azul + '[+]' + normal} {newUrl} => {http.status_code}")
    lines.close()

if __name__ == "__main__":
    main(a.url, a.wordlist)
