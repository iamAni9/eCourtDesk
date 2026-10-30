from ecourts.client import ECourtsClient


class PageState:
    def __init__(self):
        self.client = ECourtsClient()
        self.app_token: str | None = None

        # -- CNR Search elements --
        self.cnr_input = None
        self.captcha_container = None
        self.captcha_answer = None
        self.captcha_status = None
        self.refresh_btn = None
        self.search_btn = None

        # -- Case Number Search elements --
        self.state_select = None
        self.district_select = None
        self.court_complex_select = None
        self.court_est_select = None
        self.case_type_select = None
        self.case_number_input = None
        self.case_year_input = None
        self.case_captcha_container = None
        self.case_captcha_answer = None
        self.case_captcha_status = None
        self.case_refresh_btn = None
        self.case_search_btn = None
        self.case_details_section = None

        # -- Shared --
        self.results_container = None

