from ecourts.client import ECourtsClient
from bs4 import BeautifulSoup

client = ECourtsClient()

try:
    html = client.open_portal()

    soup = BeautifulSoup(html, 'html.parser')

    # Inspect CAPTCHA image source without printing tokens or cookies
    captcha = soup.find('img', id='captcha_image')

    if captcha:
        src = captcha.get('src', '')
        print('CAPTCHA image source:', src[:250])
    else:
        print('CAPTCHA image not found.')

    # Find references to app_token in the initial HTML
    print('\napp_token references:')

    lines = html.splitlines()
    matches = [
        (index + 1, line.strip()[:250])
        for index, line in enumerate(lines)
        if 'app_token' in line.lower()
    ]

    for line_number, line in matches[:10]:
        print(f'Line {line_number}: {line}')
except Exception as e:
    print('Error opening portal:', e)
