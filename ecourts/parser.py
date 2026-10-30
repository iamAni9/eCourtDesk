from bs4 import BeautifulSoup
import re

def clean_text(element):
    """Extract clean text from an HTML element."""
    if not element:
        return None

    text = element.get_text(" ", strip=True)
    return text or None


def parse_case_details(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    data = {
        "court_name": None,
        "case_details": {},
        "case_status": {},
        "parties": {
            "petitioners": [],
            "respondents": [],
        },
        "acts": [],
        "fir_details": {},
        "case_history": [],
        "orders": [],
        "transfers": [],
    }

    # Court name
    data["court_name"] = clean_text(
        soup.find(id="chHeading")
    )

    # Case details table
    case_table = soup.select_one("table.case_details_table")

    if case_table:
        rows = case_table.find_all("tr")

        for row in rows:
            cells = row.find_all(["th", "td"], recursive=False)

            i = 0
            while i < len(cells):
                if cells[i].name != "th":
                    i += 1
                    continue

                label = clean_text(cells[i])
                value = clean_text(cells[i + 1]) if i + 1 < len(cells) else None

                if label:
                    key = label.lower().replace(" ", "_")
                    data["case_details"][key] = value

                i += 2

    # Case status table
    status_table = soup.select_one("table.case_status_table")

    if status_table:
        for row in status_table.find_all("tr"):
            cells = row.find_all(["th", "td"], recursive=False)

            if len(cells) >= 2:
                label = clean_text(cells[0])
                value = clean_text(cells[1])

                if label:
                    key = label.lower().replace(" ", "_")
                    data["case_status"][key] = value

    # Petitioner and respondent lists
    for selector, key in [
        ("ul.petitioner-advocate-list", "petitioners"),
        ("ul.respondent-advocate-list", "respondents"),
    ]:
        element = soup.select_one(selector)

        if element:
            data["parties"][key] = [
                clean_text(item)
                for item in element.find_all("li", recursive=False)
                if clean_text(item)
            ]

    # Acts and sections
    acts_table = soup.select_one("table.acts_table")

    if acts_table:
        for row in acts_table.find_all("tr")[1:]:
            cells = row.find_all(["th", "td"], recursive=False)

            if len(cells) >= 2:
                data["acts"].append({
                    "act": clean_text(cells[0]),
                    "sections": clean_text(cells[1]),
                })

    # FIR details
    fir_table = soup.select_one("table.FIR_details_table")

    if fir_table:
        for row in fir_table.find_all("tr"):
            cells = row.find_all(["th", "td"], recursive=False)

            if len(cells) >= 2:
                label = clean_text(cells[0])
                value = clean_text(cells[1])

                if label and label.lower() != "field":
                    key = label.lower().replace(" ", "_")
                    data["fir_details"][key] = value

    # Case hearing history
    history_table = soup.select_one("table.history_table")

    if history_table:
        rows = history_table.find_all("tr")

        for row in rows[1:]:
            cells = row.find_all(["th", "td"], recursive=False)

            if len(cells) >= 4:
                data["case_history"].append({
                    "judge": clean_text(cells[0]),
                    "business_on_date": clean_text(cells[1]),
                    "hearing_date": clean_text(cells[2]),
                    "purpose": clean_text(cells[3]),
                })

    # Interim orders
    order_table = soup.select_one("table.order_table")

    if order_table:
        for row in order_table.find_all("tr")[1:]:
            cells = row.find_all(["th", "td"], recursive=False)

            if len(cells) >= 3:
                link = cells[2].find("a")

                data["orders"].append({
                    "order_number": clean_text(cells[0]),
                    "order_date": clean_text(cells[1]),
                    "description": clean_text(link or cells[2]),
                })

    # Transfers within the establishment
    transfer_table = soup.select_one("table.transfer_table")

    if transfer_table:
        for row in transfer_table.find_all("tr")[1:]:
            cells = row.find_all(["th", "td"], recursive=False)

            if len(cells) >= 4:
                data["transfers"].append({
                    "registration_number": clean_text(cells[0]),
                    "transfer_date": clean_text(cells[1]),
                    "from_court": clean_text(cells[2]),
                    "to_court": clean_text(cells[3]),
                })

    return data

def parse_dropdown_options(html: str) -> dict[str, str]:
    """Convert an eCourts dropdown HTML fragment into {value: label}."""
    soup = BeautifulSoup(html or '', 'html.parser')
    options = {}

    for option in soup.select('option'):
        value = option.get('value')
        label = option.get_text(' ', strip=True)

        # Ignore the placeholder option.
        if value and label:
            options[str(value)] = label

    return options



def parse_case_number_results(html: str) -> dict:
    """Parse the case list HTML returned by the eCourts Case Number API."""
    soup = BeautifulSoup(html or '', 'html.parser')

    def clean_text(element):
        if not element:
            return None

        # Preserve readable text across <br> and nested tags.
        text = element.get_text(' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        return text.strip() or None

    data = {
        'summary': {
            'total_establishments': None,
            'total_cases': None,
        },
        'establishments': [],
        'table_headers': [],
        'cases': [],
    }

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    summary_element = soup.select_one('#courtSummary')
    summary_text = clean_text(summary_element) or ''

    establishments_match = re.search(
        r'Total Number of Establishments in Court Complex\s*:\s*(\d+)',
        summary_text,
        re.IGNORECASE,
    )
    cases_match = re.search(
        r'Total number of cases\s*:\s*(\d+)',
        summary_text,
        re.IGNORECASE,
    )

    if establishments_match:
        data['summary']['total_establishments'] = int(
            establishments_match.group(1)
        )

    if cases_match:
        data['summary']['total_cases'] = int(
            cases_match.group(1)
        )

    # --------------------------------------------------
    # Establishment list
    # Example: District and Sessions Judge, North, RHC: 1
    # --------------------------------------------------
    for item in soup.select('#showList2 ul li'):
        link = item.find('a')
        if not link:
            continue

        label = clean_text(link) or ''
        count_match = re.search(r':\s*(\d+)\s*$', label)

        court_name = (
            label[:count_match.start()].strip()
            if count_match
            else label
        )

        data['establishments'].append({
            'court_name': court_name,
            'case_count': (
                int(count_match.group(1))
                if count_match else None
            ),
            'href': link.get('href'),
            'css_class': link.get('class', []),
        })

    # --------------------------------------------------
    # Case results table headers
    # --------------------------------------------------
    # eCourts HTML sometimes has duplicate id attributes like
    # <table id='dispTable' ... id='titlehid'> which causes
    # html.parser to overwrite 'dispTable' with 'titlehid'.
    table = (
        soup.select_one('table#dispTable')
        or soup.select_one('table#titlehid')
        or soup.find('table', class_=lambda c: c and 'table' in c)
        or soup.find('table')
    )

    if not table:
        return data

    header_row = table.select_one('thead tr')

    if header_row:
        data['table_headers'] = [
            clean_text(cell)
            for cell in header_row.find_all(
                ['th', 'td'],
                recursive=False,
            )
        ]
    else:
        data['table_headers'] = [
            'Sr No',
            'Case Type/Case Number/Case Year',
            'Petitioner Name versus Respondent Name',
            'View',
        ]

    # --------------------------------------------------
    # Case rows
    # --------------------------------------------------
    current_court = None

    for row in table.select('tbody tr'):
        # Court heading rows have a <th colspan="3"> or similar.
        court_heading = row.find(
            'th',
            attrs={'colspan': True},
        )

        if court_heading:
            current_court = clean_text(court_heading)
            continue

        cells = row.find_all(
            ['th', 'td'],
            recursive=False,
        )

        if not cells:
            continue

        # Read every cell based on the table headers.
        column_data = {}

        for index, cell in enumerate(cells):
            if index < len(data['table_headers']):
                header = data['table_headers'][index]
            else:
                header = f'column_{index + 1}'

            column_data[header] = clean_text(cell)

        # The supplied table has four columns:
        # Sr No | Case Type/Case Number/Case Year |
        # Petitioner versus Respondent | View
        if len(cells) < 4:
            continue

        parties_cell = cells[2]
        parties_text = clean_text(parties_cell) or ''

        # Handle formatting like <br>Vs</br> which may produce "VsSubhash" without spaces
        fixed_parties = re.sub(r'(?i)\bvs\.?\s*', ' Vs ', parties_text)
        fixed_parties = re.sub(r'\s+', ' ', fixed_parties).strip()

        parties_match = re.split(
            r'\s+Vs\.?\s+',
            fixed_parties,
            maxsplit=1,
            flags=re.IGNORECASE,
        )

        petitioner = parties_match[0].strip() if parties_match else None
        respondent = (
            parties_match[1].strip()
            if len(parties_match) > 1 else None
        )

        view_link = cells[3].find('a')

        view_data = None
        cnr_number = None
        if view_link:
            onclick_val = view_link.get('onclick') or ''
            cnr_match = re.search(r"viewHistory\([^,]+,\s*'([^']+)'", onclick_val)
            if cnr_match:
                cnr_number = cnr_match.group(1).strip()

            view_data = {
                'text': clean_text(view_link) or 'View',
                'href': view_link.get('href'),
                'aria_label': view_link.get('aria-label'),
                'onclick': onclick_val,
                'css_class': view_link.get('class', []),
                'cnr': cnr_number,
            }

        data['cases'].append({
            'court_name': current_court,
            'serial_number': clean_text(cells[0]),
            'case_type_case_number_case_year': clean_text(cells[1]),
            'petitioner_versus_respondent': (
                f"{petitioner} Vs {respondent}" if petitioner and respondent else parties_text
            ),
            'petitioner': petitioner,
            'respondent': respondent,
            'cnr': cnr_number,
            'view': view_data,
            'columns': column_data,
        })

    # Fallback if the summary did not provide a case count.
    if data['summary']['total_cases'] is None:
        data['summary']['total_cases'] = len(data['cases'])

    return data