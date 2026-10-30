from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from ecourts.client import ECourtsClient
from pathlib import Path

client = ECourtsClient()

try:
    result = client.get_captcha()
    res = client.get_case_status_page()
    file = Path("case_status_page.html")
    file.write_text(res, encoding="utf-8")

except Exception as e:
    print('Error opening portal:', e)