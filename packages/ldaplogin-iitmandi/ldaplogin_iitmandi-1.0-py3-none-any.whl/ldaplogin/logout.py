import httpx
from bs4 import BeautifulSoup

def ldap_logout():
    url = httpx.get('https://login.iitmandi.ac.in:1003/portal?')
    soup = BeautifulSoup(url.text, 'html.parser')
    form_header = soup.find(class_='form-header').text

    verify_login = 'Login to access the IT Services'
    auth_login = 'Authentication Successful'

    if auth_login in form_header:
        print('Logging you out ...')
        logout = httpx.get('https://login.iitmandi.ac.in:1003/logout?')
        new_url = httpx.get('https://login.iitmandi.ac.in:1003/portal?')
        post_soup = BeautifulSoup(new_url.text, 'html.parser')
        post_form_header = post_soup.find(class_='form-header').text
        if verify_login in post_form_header:
            print('Successfully Logged out.')
        else:
            print('Logout Failed')
    elif verify_login in form_header:
        print('Already logged out!')
