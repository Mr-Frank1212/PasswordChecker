import requests
import hashlib
import sys

# Func that takes in the first 5 Hash character of the Password
# and returns its request.get()
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}, Check the API')
    return res

#Func takes in first 5 char hashes match and tail of actual password
# and return the password's count after searching for it from hashes
def get_password_leaks_count(resp_hashes, hash_to_check ):
    hashes=(lines.split(':') for lines in resp_hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

#fuction does the hashing and slicing of the hash between tail and first 5 char
# it returns the function 'get_password_leaks_count' which returns count
def pwned_api_check(password):
    sha1_password= hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char, tail=sha1_password[:5],sha1_password[5:]
    response= request_api_data(first5char)
    return get_password_leaks_count(response,tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'\nPassword: {password} was found {count} times.. You should probably change your password')
        else:
            print(f'\nPassword: {password} was NOT found, carry on')
    return '\ndone!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))