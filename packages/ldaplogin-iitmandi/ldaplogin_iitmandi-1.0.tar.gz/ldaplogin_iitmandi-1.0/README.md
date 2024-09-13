To create a package that includes the functions `ldap_login`, `ldap_logout`, and `ldap --setup`, you can organize your code into a Python package structure and define entry points for these commands. Here's a step-by-step guide to achieve this:

### Step 1: Organize the Package Structure
Ensure your package structure is organized as follows:

```
ldaplogin/
├── ldaplogin
│   ├── __init__.py
│   ├── login.py
│   ├── logout.py
│   ├── setup_credentials.py
├── setup.py
```

### Step 2: Write the Code for Each Function

#### login.py

```python
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
```

#### logout.py

```python
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
```

#### setup_credentials.py

```python
import keyring

def setup_credentials():
    import getpass
    username = input("Enter your LDAP username: ")
    password = getpass.getpass("Enter your LDAP password: ")
    # Store the credentials in the keyring
    keyring.set_password("ldaplogin", "username", username)
    keyring.set_password("ldaplogin", "password", password)
    print("Credentials have been securely stored.")
```

### Step 3: Define the Package Configuration in `setup.py`

```python
from setuptools import setup, find_packages

setup(
    name='ldaplogin',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'beautifulsoup4',
        'keyring',
    ],
    entry_points={
        'console_scripts': [
            'ldaplogin=ldaplogin.login:ldap_login',
            'ldaplogout=ldaplogin.logout:ldap_logout',
            'ldapsetup=ldaplogin.setup_credentials:setup_credentials',
        ],
    },
)
```

### Step 4: Create `__init__.py` (Optional)

An empty `__init__.py` file is typically included to indicate that the directory is a Python package:

```python
# ldaplogin/__init__.py
```

### Step 5: Build and Install the Package

Build your package:

```bash
python setup.py sdist bdist_wheel
```

Install your package locally to test it:

```bash
pip install .
```

### Step 6: Use the Commands

After installation, you can use the commands from the terminal:

- `ldapsetup` to store your credentials.
- `ldaplogin` to log in using the stored credentials.
- `ldaplogout` to log out.

By organizing your package this way, you provide clear separation of concerns for each function, making it easy to maintain and expand.
