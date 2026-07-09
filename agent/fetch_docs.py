import requests
from bs4 import BeautifulSoup


def fetch_documentation(url):

    headers = {
        "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
            allow_redirects=True
        )

        if response.status_code != 200:
            print("Status Code:", response.status_code)
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "noscript",
            "svg"
        ]):
            tag.decompose()

        text = soup.get_text(" ", strip=True)

        words = text.split()

        return " ".join(words[:5000])

    except Exception as e:

        print("Fetch Error:", e)
        return ""