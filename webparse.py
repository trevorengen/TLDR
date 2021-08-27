import requests
from bs4 import BeautifulSoup
from requests.models import Response

def parse_body(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup(["script", "style"]):                   
        script.decompose()     
    tag = soup.body
    string_arr = []
    for string in tag.strings:
        string_arr.append(string)
    return string_arr