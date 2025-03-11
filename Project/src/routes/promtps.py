import re
import requests
from bs4 import BeautifulSoup


def extract_url(text):
    url_pattern = r"https?://\S+"
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

def fetch_page_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return f"Error:{response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")
        text = ' '.join([p.get_text() for p in soup.find_all("p")])
        return text[:4000]
    except Exception as e:
        return f"Error: {e}"

def contains_url(text):
    url_pattern = r"https?://\S+"
    return bool(re.search(url_pattern, text))