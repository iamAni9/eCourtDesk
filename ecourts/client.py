import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class ECourtsClient:
    BASE_URL = 'https://services.ecourts.gov.in/ecourtindia_v6/'

    def __init__(self):
        self.session = requests.Session()
        self.header = {}              

    def _get_ajax_headers(self, html: str) -> dict[str, str]:
        """Extract the portal's current AJAX headers from components.js."""

        soup = BeautifulSoup(html, 'html.parser')

        script = next(
            (
                tag for tag in soup.find_all('script', src=True)
                if re.search(r'components\.js(?:\?|$)', tag['src'], re.I)
            ),
            None,
        )

        if script is None:
            raise RuntimeError(
                'Could not find components.js in the homepage.'
            )

        script_url = urljoin(self.BASE_URL, script['src'])

        response = self.session.get(script_url, timeout=30)
        response.raise_for_status()
        js = response.text

        # Extract the rotating secret from its JavaScript assignment.
        secret_match = re.search(
            r"""\bdelimeter\s*=\s*(['"])(.*?)\1""",
            js,
        )

        if secret_match is None:
            raise RuntimeError(
                'Could not find the delimeter assignment in components.js.'
            )

        secret = secret_match.group(2)

        # Find the AJAX headers object that uses the secret.
        block_match = re.search(
            r"""\bheaders\s*:\s*\{([^{}]*\bdelimeter\b[^{}]*)\}""",
            js,
            re.I | re.S,
        )

        if block_match is None:
            raise RuntimeError(
                'Could not find the AJAX headers definition.'
            )

        headers = {}

        for item in block_match.group(1).split(','):
            if ':' not in item:
                continue

            key_text, value_text = item.split(':', 1)

            key_match = re.fullmatch(
                r"""\s*(['"])(.*?)\1\s*""",
                key_text,
            )

            if key_match is None:
                continue

            key = key_match.group(2)
            value = value_text.strip().rstrip(';').strip()

            if value == 'delimeter':
                headers[key] = secret
            else:
                literal_match = re.fullmatch(
                    r"""(['"])(.*?)\1""",
                    value,
                )

                if literal_match:
                    headers[key] = literal_match.group(2)

        if 'delimeter' not in headers:
            raise RuntimeError(
                'The current AJAX headers could not be extracted.'
            )

        return headers

    # Open the eCourts portal and stablish a session
    def _open_portal(self):
        try: 
            response = self.session.get(
                self.BASE_URL,
                timeout=30,
            )
            response.raise_for_status()
            
            return response.text  # Return the HTML content of the portal page
        except requests.RequestException as e:
            print(f"Error opening eCourts portal: {e}")
            return None

    
    def get_captcha(self) -> dict | None:
        url = url = self.BASE_URL + "?p=casestatus/getCaptcha"
        try:
            # Open homepage and establish session
            html = self._open_portal()
            if not html:
                raise RuntimeError('Could not open the eCourts portal.')

            # Dynamically extract rotating AJAX headers from components.js
            self.headers = self._get_ajax_headers(html)

            response = self.session.post(
                url,
                data={
                    'ajax_req': 'true',
                    'app_token': '',
                },
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            if result.get('errormsg'):
                print('CAPTCHA initialization rejected by the portal.')
                print('Response keys:', list(result.keys()))
                return None

            if not result.get('app_token'):
                print('No app_token returned by the portal.')
                print('Response keys:', list(result.keys()))
                return None

            return result

        except requests.exceptions.JSONDecodeError:
            print('The CAPTCHA endpoint returned invalid JSON.')
            return None

        except requests.RequestException as exc:
            print(f'Network error fetching CAPTCHA: {exc}')
            return None

        except RuntimeError as exc:
            print(f'CAPTCHA initialization failed: {exc}')
            return None


    def get_captcha_image(self, captcha_html: str) -> bytes:
        soup = BeautifulSoup(captcha_html, 'html.parser')

        captcha = soup.find('img', id='captcha_image')

        if not captcha or not captcha.get('src'):
            raise RuntimeError(
                'CAPTCHA image URL was not found in the response.'
            )

        captcha_url = urljoin(self.BASE_URL, captcha['src'])

        response = self.session.get(
            captcha_url,
            headers={'Referer': self.BASE_URL},
            timeout=30,
        )
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')

        if not content_type.startswith('image/'):
            raise RuntimeError(
                'The portal did not return a valid CAPTCHA image.'
            )

        # self.captcha_content_type = content_type.split(';', 1)[0]

        return response.content

    
    # Search for a case using CNR number
    def search_with_cnr(self, cnr_number, captcha_code, app_token):
        url = self.BASE_URL + "?p=cnr_status/searchByCNR/"
        try: 
            cnr = cnr_number.strip()
            if not cnr:
                raise ValueError('CNR number is required.')
            payload = {
                'cino': cnr,
                'fcaptcha_code': captcha_code,
                'ajax_req': 'true',
                'app_token': app_token,
            }
            
            response = self.session.post(
                url,
                data=payload,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()

            return result
        
        except requests.exceptions.JSONDecodeError as exc:
            print('The portal returned a response that was not valid JSON.', exc)

        except requests.RequestException as e:
            print(f"Error searching with CNR number: {e}")
            return None

    # Get the list of districts using state_code
    def get_districts(self, state_code: str, app_token: str):
        url = self.BASE_URL + "?p=casestatus/fillDistrict"
       
        payload = {
            'state_code': state_code,
            'ajax_req': 'true',
            'app_token': app_token,
        }

        try:
            response = self.session.post(
                url,
                data=payload,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            return result
        
        except requests.exceptions.JSONDecodeError as exc:
            print('The portal returned a response that was not valid JSON.', exc)
            return None
        except requests.RequestException as e:
            print(f"Error fetching court complexes: {e}")
            return None

    # Get list of court complexes using state and district code
    def get_court_complexes(self, state_code: str, dist_code: str, app_token: str,):
        url = self.BASE_URL + "?p=casestatus/fillcomplex"
        payload = {
            'state_code': state_code,
            'dist_code': dist_code,
            'ajax_req': 'true',
            'app_token': app_token,
        }
        try:
            response = self.session.post(
                url,
                data=payload,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            
            return result
        
        except requests.exceptions.JSONDecodeError as exc:
            print('The portal returned a response that was not valid JSON.', exc)
            return None
        except requests.RequestException as e:
            print(f"Error fetching court complexes: {e}")
            return None

    # Get list of court establisments using state, district and complex code
    def get_court_establishments(self, state_code: str, dist_code: str, court_complex_code: str, app_token: str):
        url = self.BASE_URL + "?p=casestatus/fillCourtEstablishment"

        payload = {
            'state_code': state_code,
            'dist_code': dist_code,
            'court_complex_code': court_complex_code,
            'ajax_req': 'true',
            'app_token': app_token,
        }

        try:
            response = self.session.post(
                url,
                data=payload,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()
            
            return result
        
        except requests.exceptions.JSONDecodeError as exc:
            print('The portal returned a response that was not valid JSON.', exc)
            return None
        except requests.RequestException as e:
            print(f"Error fetching court complexes: {e}")
            return None

    # Get list of case type
    def get_case_types(self, state_code: str, dist_code: str, court_complex_code: str, est_code: str, app_token: str):
        url = self.BASE_URL + "?p=casestatus/fillCaseType"
        payload = {
            'state_code': state_code,
            'dist_code': dist_code,
            'court_complex_code': court_complex_code,
            'est_code': est_code,
            'search_type': 'c_no',
            'ajax_req': 'true',
            'app_token': app_token,
        }

        try:
            response = self.session.post(
                url,
                data=payload,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            print(result)
            return result

        except requests.exceptions.JSONDecodeError as exc:
            print('The portal returned a response that was not valid JSON.', exc)
            return None
        except requests.RequestException as e:
            print(f"Error fetching court complexes: {e}")
            return None

    def search_with_case_number(self, case_type: str, case_number: str, year: str, captcha_code: str, state_code: str, dist_code: str, court_complex_code: str, est_code: str, app_token: str):
        url = self.BASE_URL + "?p=casestatus/submitCaseNo"
        payload = {
            'case_type': case_type,
            'search_case_no': case_number,
            'rgyear': year,
            'case_captcha_code': captcha_code,
            'state_code': state_code,
            'dist_code': dist_code,
            'court_complex_code': court_complex_code,
            'est_code': est_code,
            'case_type': case_type,
            'case_no': case_number,
            'rgyear': year,
            'ajax_req': 'true',
            'app_token': app_token,
        }

        try:
            response = self.session.post(
                url,
                data=payload,
                headers=self.headers,
                timeout=30,
            )
                
            response.raise_for_status()
            result = response.json()
            print(result)
            return result

        except requests.exceptions.JSONDecodeError as exc:
            print('The portal returned a response that was not valid JSON.', exc)
            return None
        except requests.RequestException as e:
            print(f"Error fetching court complexes: {e}")
            return None