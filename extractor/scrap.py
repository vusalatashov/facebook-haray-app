import httpx
from bs4 import BeautifulSoup

def get_html(url):
    with httpx.Client() as client:
        response = client.get(url, allow_redirects=False)
        if response.status_code == 302:  # Eğer bir yönlendirme varsa
            redirect_url = response.headers['Location']
            response = client.get(redirect_url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()


