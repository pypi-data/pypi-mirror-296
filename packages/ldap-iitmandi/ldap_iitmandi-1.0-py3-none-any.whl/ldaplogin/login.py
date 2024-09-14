import httpx
from bs4 import BeautifulSoup
import keyring

def ldap_login():
    username = keyring.get_password("ldaplogin", "username")
    password = keyring.get_password("ldaplogin", "password")

    if not username or not password:
        print("Credentials not found. Please run ldap --setup to store your credentials.")
        return

    url = httpx.get('https://login.iitmandi.ac.in:1003/portal?')
    soup = BeautifulSoup(url.text, 'html.parser')
    form_header = soup.find(class_='form-header').text

    verify_login = 'Login to access the IT Services'
    auth_login = 'Authentication Successful'

    if verify_login in form_header:
        print('Logging you in ...')
        magic_input = soup.find("input", {"name": "magic"})
        magic_value = magic_input.get("value")

        login_data = {
            '4Tredir': 'https%3A%2F%2Flogin.iitmandi.ac.in%3A1003%2Fportal%3F',
            'magic': magic_value,
            'username': username,
            'password': password
        }
        r = httpx.post("https://login.iitmandi.ac.in:1003/", data=login_data)

        post_login = httpx.get('https://login.iitmandi.ac.in:1003/portal?')
        post_soup = BeautifulSoup(post_login.text, 'html.parser')
        post_form_header = post_soup.find(class_='form-header').text

        if auth_login in post_form_header:
            print('Successfully Logged in.')
        else:
            print('Login Failed')
    elif auth_login in form_header:
        print('Already logged in!')
