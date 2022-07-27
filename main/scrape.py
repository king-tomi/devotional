import requests
from bs4 import BeautifulSoup

def get_content(url: str) -> BeautifulSoup:
    """gets content from the website and returns a Beautiful soup object"""
    try:
        req = requests.get(url=url, stream=True)
        if req.status_code == 200:
            print("connection successful")
            soup = BeautifulSoup(req.content, 'html.parser')
            return soup
        else:
            print("Site not found")
            return
    except requests.RequestException:
        print("Error establishing request")
        return