# input type: python3 projectname password1 password2 & so on
# output: it will tell if my password has ever been hacked
import requests  # external module
import hashlib
from sys import argv,exit


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res=requests.get(url)
    if res.status_code!=200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the API & try again')
    return res

def get_password_leaks_count(hashes,hash_to_check):
    hashes=(line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h==hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    fitst5_char,tail=sha1password[0:5],sha1password[5:]
    response=request_api_data(fitst5_char)
    return get_password_leaks_count(response,tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times...you should change your password')
        else:
            print(f'{password} was not found. carry on')
    return 'done'

if __name__=='__main__':
    exit(main(argv[1:]))
    #exit brig us back to command line not neccessary to include this

