import requests
from bs4 import BeautifulSoup

ROOT_URL = 'library root url goes here (e.g. https://my-lib.myschool.ac.uk)'
START_URL = 'permalink of the My Account page goes here (click on My Account then Permalink)'
USERNAME = 'library username goes here (can be found in "username" hidden form field)'
PASSWORD = '4 digit library PIN goes here (can be found in "password" hidden form field)'

login_page = requests.get(START_URL)
login_soup = BeautifulSoup(login_page.content, 'html.parser')
very_definitely_secure_cookie = login_page.cookies['session_number']
login_target = login_soup.find_all(attrs={'name': 'loginform'})[0]['action']
login_response = requests.post(ROOT_URL + login_target, data = {'user_id' : USERNAME, 'password' : PASSWORD},
                               cookies = {'session_number' : very_definitely_secure_cookie,
                                          'session_security' : very_definitely_secure_cookie})
loggedin_soup = BeautifulSoup(login_response.content, 'html.parser')
renew_target = loggedin_soup.find_all(text='Renew My Loans')[0].parent['href']
renew_response = requests.get(ROOT_URL + renew_target,
                              cookies = {'session_number' : very_definitely_secure_cookie,
                                         'session_security' : very_definitely_secure_cookie})
renew_soup = BeautifulSoup(renew_response.content, 'html.parser')
submission_target = renew_soup.find_all(attrs={'name' : 'renewitems'})[0]['action']
requests.post(ROOT_URL + submission_target, data = {'selection_type' : 'all'},
              cookies = {'session_number' : very_definitely_secure_cookie,
                         'session_security' : very_definitely_secure_cookie})
