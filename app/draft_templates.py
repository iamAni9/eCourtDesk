from datetime import datetime


DRAFT_TYPES = [
    'Bail Application',
    'Legal Notice',
    'Civil Suit (Plaint)',
    'Writ Petition',
    'General Application',
    'Affidavit',
]


SAMPLE_PRESETS = {
    'Bail Application': {
        'court_name': 'IN THE COURT OF PRINCIPAL DISTRICT & SESSIONS JUDGE, PATIALA HOUSE COURTS',
        'court_place': 'NEW DELHI',
        'case_number': 'BAIL APPLN. NO. 1042 OF 2024',
        'fir_details': 'FIR No. 128/2024, PS Connaught Place, U/s 420/406/120B IPC',
        'petitioner_name': 'Rohan Sharma',
        'petitioner_parent': 'Shri Ram Sharma',
        'petitioner_age': '34',
        'petitioner_address': 'A-12, Sector 15, Rohini, New Delhi - 110085',
        'petitioner_role': 'Applicant / Accused',
        'respondent_name': 'State (NCT of Delhi)',
        'respondent_parent': 'Through Public Prosecutor, Patiala House Courts',
        'respondent_age': '',
        'respondent_address': 'New Delhi',
        'respondent_role': 'Respondent / State',
        'advocate_name': 'Adv. Aniket Chaudhary',
        'advocate_enrollment': 'D/1425/2018',
        'advocate_chamber': 'Chamber No. 412, Lawyers Chambers, Patiala House Courts, New Delhi',
        'legal_sections': 'APPLICATION UNDER SECTION 439 OF THE CODE OF CRIMINAL PROCEDURE, 1973 (READ WITH SECTION 483 OF BNSS, 2023) FOR GRANT OF REGULAR BAIL',
        'facts': (
            '1. That the Applicant is a peaceful, law-abiding citizen of India residing at the aforesaid address with his family and has clean antecedents.\n'
            '2. That the Applicant has been falsely implicated in FIR No. 128/2024 registered at PS Connaught Place under Sections 420, 406 and 120B IPC at the behest of commercial rivals.\n'
            '3. That the dispute in question is purely civil and contractual in nature arising out of a commercial memorandum of understanding dated 15.01.2023.\n'
            '4. That the Applicant was arrested on 10.10.2024 and has been in judicial custody since then. All relevant records, laptops, and bank accounts have already been seized by the Investigating Agency.\n'
            '5. That the investigation qua the Applicant is substantially complete and no custodial interrogation is required any longer.'
        ),
        'grounds': (
            'A. That the Applicant is innocent and has not committed any cognizable offence as alleged in the impugned FIR.\n'
            'B. That the offenses alleged are triable by a Magistrate of the First Class and are not punishable with death or imprisonment for life.\n'
            'C. That the Applicant is a permanent resident of Delhi having deep roots in society, with dependent aged parents, wife, and minor school-going children, eliminating any flight risk.\n'
            'D. That all documentary evidence is already in possession of the investigating officer, ruling out any possibility of tampering with evidence.\n'
            'E. That the Applicant undertakes to abide by all stringent terms and conditions that this Hon\'ble Court may deem fit to impose and shall cooperate fully with the ongoing trial.'
        ),
        'prayers': (
            'a) Admit the Applicant/Accused to regular bail in connection with FIR No. 128/2024 registered at Police Station Connaught Place, New Delhi, pending before the Ld. Trial Court;\n'
            'b) Pass such other or further order(s) as this Hon\'ble Court may deem fit and proper in the interest of justice and equity.'
        ),
        'place': 'New Delhi',
        'date': datetime.now().strftime('%d.%m.%Y'),
    },
    'Legal Notice': {
        'court_name': 'OFFICE OF ADVOCATE',
        'court_place': 'NEW DELHI',
        'case_number': 'REF: LN/2024/098',
        'fir_details': '',
        'petitioner_name': 'M/s Apex Infotech Solutions Pvt. Ltd.',
        'petitioner_parent': 'Represented by its Director Mr. Vivek Singhal',
        'petitioner_age': '',
        'petitioner_address': 'Plot No. 45, Okhla Industrial Area Phase-III, New Delhi - 110020',
        'petitioner_role': 'Complainant / Sender',
        'respondent_name': 'M/s Global Trading Enterprises',
        'respondent_parent': 'Through its Managing Partner Mr. Rakesh Verma',
        'respondent_age': '',
        'respondent_address': 'Shop No. 12, Ground Floor, Commercial Complex, Barakhamba Road, New Delhi - 110001',
        'respondent_role': 'Noticee / Defaulter',
        'advocate_name': 'Adv. Aniket Chaudhary',
        'advocate_enrollment': 'D/1425/2018',
        'advocate_chamber': 'Chamber No. 412, Lawyers Chambers, Patiala House Courts, New Delhi',
        'legal_sections': 'LEGAL NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 FOR DISHONOUR OF CHEQUE AND RECOVERY OF OUTSTANDING DUES',
        'facts': (
            '1. That my client is a reputed private limited company engaged in providing enterprise software solutions.\n'
            '2. That under Invoice No. INV-2024-512 dated 10.05.2024, my client supplied customized software licenses and consultancy services to you the Noticee for an agreed sum of Rs. 14,50,000/- (Rupees Fourteen Lakhs Fifty Thousand only).\n'
            '3. That towards discharge of your admitted legally enforceable debt and liability, you the Noticee issued Cheque bearing No. 045129 dated 15.09.2024 for Rs. 14,50,000/- drawn on HDFC Bank, Connaught Place Branch, New Delhi in favor of my client.\n'
            '4. That when my client presented the said cheque for encashment, the same was returned unpaid by your banker with the memo remarks "FUNDS INSUFFICIENT" dated 20.09.2024.'
        ),
        'grounds': (
            'A. That you the Noticee deliberately and dishonestly issued the aforesaid cheque knowing fully well that you lacked sufficient balance in your bank account, thereby committing an offence under Section 138 of the Negotiable Instruments Act, 1881.\n'
            'B. That you have also committed criminal breach of trust and cheating punishable under the Indian Penal Code / Bharatiya Nyaya Sanhita.'
        ),
        'prayers': (
            'a) Pay the entire dishonoured cheque amount of Rs. 14,50,000/- (Rupees Fourteen Lakhs Fifty Thousand only) along with interest @ 18% per annum within 15 days from the receipt of this notice;\n'
            'b) Pay Rs. 25,000/- towards the legal expenses incurred for issuing this legal notice.'
        ),
        'place': 'New Delhi',
        'date': datetime.now().strftime('%d.%m.%Y'),
    },
    'Civil Suit (Plaint)': {
        'court_name': 'IN THE COURT OF LD. DISTRICT JUDGE (COMMERCIAL COURT), PATIALA HOUSE COURTS',
        'court_place': 'NEW DELHI',
        'case_number': 'COMMERCIAL SUIT NO. _____ OF 2024',
        'fir_details': '',
        'petitioner_name': 'Pankaj Kohli',
        'petitioner_parent': 'Late Shri M. L. Kohli',
        'petitioner_age': '48',
        'petitioner_address': 'Flat No. 302, Green Park Apartments, New Delhi - 110016',
        'petitioner_role': 'Plaintiff',
        'respondent_name': 'Subhash Chand',
        'respondent_parent': 'Shri Om Prakash',
        'respondent_age': '52',
        'respondent_address': 'Property No. B-74, Defence Colony, New Delhi - 110024',
        'respondent_role': 'Defendant',
        'advocate_name': 'Adv. Aniket Chaudhary',
        'advocate_enrollment': 'D/1425/2018',
        'advocate_chamber': 'Chamber No. 412, Lawyers Chambers, Patiala House Courts, New Delhi',
        'legal_sections': 'SUIT UNDER ORDER VII RULE 1 READ WITH SECTION 26 OF THE CODE OF CIVIL PROCEDURE, 1908 FOR RECOVERY OF MONEY AND PERMANENT INJUNCTION',
        'facts': (
            '1. That the Plaintiff is a registered merchant and proprietor carrying on business in New Delhi.\n'
            '2. That the Defendant approached the Plaintiff in January 2024 for wholesale purchase of commercial goods and promised payment within 30 days of invoice.\n'
            '3. That the Plaintiff supplied goods valued at Rs. 8,75,000/- under delivery challans and invoices duly acknowledged by the Defendant.\n'
            '4. That despite repeated demands, reminders, and visits, the Defendant has failed and neglected to pay the principal balance amount.'
        ),
        'grounds': (
            'A. That the Defendant has wrongfully retained the Plaintiff\'s funds without any just or lawful cause.\n'
            'B. That this Hon\'ble Court has territorial and pecuniary jurisdiction to entertain and try the present suit as the transactions occurred within the local limits of this Court.\n'
            'C. That the suit is well within the period of limitation prescribed under the Limitation Act, 1963.'
        ),
        'prayers': (
            'a) Pass a decree for recovery of Rs. 8,75,000/- along with pendente lite and future interest @ 18% p.a. in favor of the Plaintiff and against the Defendant;\n'
            'b) Award costs of the suit in favor of the Plaintiff.'
        ),
        'place': 'New Delhi',
        'date': datetime.now().strftime('%d.%m.%Y'),
    },
}


def _split_into_numbered_items(text: str, prefix_type: str = 'num') -> list[str]:
    """Clean and split text into normalized numbered lines."""
    if not text:
        return []
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    cleaned = []
    for line in lines:
        # Strip leading numbers or bullets like '1.', 'A.', '-', '*'
        cleaned_line = line.lstrip('0123456789.ABCDEFGHIJKLMNOPQRSTUVWXYZ)-*• ').strip()
        if cleaned_line:
            cleaned.append(cleaned_line)
    return cleaned


def generate_legal_draft(data: dict) -> str:
    draft_type = data.get('draft_type', 'Bail Application')
    court_name = (data.get('court_name') or 'IN THE COURT OF COMPETENT JURISDICTION').strip().upper()
    court_place = (data.get('court_place') or 'DELHI').strip().upper()
    case_no = (data.get('case_number') or 'CASE NO. _____ OF 2024').strip().upper()
    fir_details = (data.get('fir_details') or '').strip()

    pet_name = (data.get('petitioner_name') or 'PETITIONER NAME').strip()
    pet_parent = (data.get('petitioner_parent') or '').strip()
    pet_age = (data.get('petitioner_age') or '').strip()
    pet_address = (data.get('petitioner_address') or 'ADDRESS').strip()
    pet_role = (data.get('petitioner_role') or 'Petitioner / Applicant').strip().upper()

    resp_name = (data.get('respondent_name') or 'RESPONDENT NAME').strip()
    resp_parent = (data.get('respondent_parent') or '').strip()
    resp_age = (data.get('respondent_age') or '').strip()
    resp_address = (data.get('respondent_address') or 'ADDRESS').strip()
    resp_role = (data.get('respondent_role') or 'Respondent').strip().upper()

    adv_name = (data.get('advocate_name') or 'ADVOCATE NAME').strip()
    adv_enroll = (data.get('advocate_enrollment') or 'ENROLLMENT NO.').strip()
    adv_chamber = (data.get('advocate_chamber') or 'CHAMBER ADDRESS').strip()

    legal_sections = (data.get('legal_sections') or 'LEGAL APPLICATION').strip().upper()
    place = (data.get('place') or 'New Delhi').strip()
    date = (data.get('date') or datetime.now().strftime('%d.%m.%Y')).strip()

    raw_facts = data.get('facts', '')
    raw_grounds = data.get('grounds', '')
    raw_prayers = data.get('prayers', '')

    fact_items = _split_into_numbered_items(raw_facts, 'num')
    ground_items = _split_into_numbered_items(raw_grounds, 'alpha')
    prayer_items = _split_into_numbered_items(raw_prayers, 'alpha_lower')

    
    if draft_type == 'Legal Notice':
        return _format_legal_notice(
            date=date,
            case_no=case_no,
            pet_name=pet_name,
            pet_parent=pet_parent,
            pet_address=pet_address,
            resp_name=resp_name,
            resp_parent=resp_parent,
            resp_address=resp_address,
            adv_name=adv_name,
            adv_enroll=adv_enroll,
            adv_chamber=adv_chamber,
            legal_sections=legal_sections,
            fact_items=fact_items,
            ground_items=ground_items,
            prayer_items=prayer_items,
            place=place,
        )

    # Format Petitioner details block
    pet_desc = pet_name
    if pet_parent:
        pet_desc += f"\nS/o, D/o, W/o {pet_parent}"
    if pet_age:
        pet_desc += f", Aged about {pet_age} years"
    if pet_address:
        pet_desc += f"\nR/o {pet_address}"

    # Format Respondent details block
    resp_desc = resp_name
    if resp_parent:
        resp_desc += f"\nS/o, D/o, W/o {resp_parent}"
    if resp_age:
        resp_desc += f", Aged about {resp_age} years"
    if resp_address:
        resp_desc += f"\nR/o {resp_address}"

    # Numbered facts
    facts_formatted = []
    for i, item in enumerate(fact_items, 1):
        prefix = f"{i}. That " if not item.lower().startswith('that ') else f"{i}. "
        facts_formatted.append(f"{prefix}{item}")
    facts_block = "\n\n".join(facts_formatted) if facts_formatted else "1. That the facts of the case are as set forth herein."

    # Numbered grounds
    grounds_formatted = []
    alpha_labels = [chr(65 + j) for j in range(26)]
    for j, item in enumerate(ground_items):
        prefix = f"{alpha_labels[j % 26]}. That " if not item.lower().startswith('that ') else f"{alpha_labels[j % 26]}. "
        grounds_formatted.append(f"{prefix}{item}")
    grounds_block = "\n\n".join(grounds_formatted) if grounds_formatted else "A. That the balance of convenience lies entirely in favor of the Applicant."

    # Numbered prayers
    prayers_formatted = []
    prayer_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for k, item in enumerate(prayer_items):
        lbl = prayer_letters[k % len(prayer_letters)]
        prayers_formatted.append(f"({lbl}) {item}")
    if not prayers_formatted:
        prayers_formatted = [
            "(a) Pass appropriate orders grant relief in the interest of justice;",
            "(b) Pass such other or further order(s) as this Hon'ble Court may deem fit.",
        ]
    prayers_block = "\n\n".join(prayers_formatted)

    fir_block = f"\nIN RE: {fir_details}\n" if fir_details else ""

    draft = f"""{court_name}, AT {court_place}

{case_no}
{fir_block}
IN THE MATTER OF:

{pet_desc}
                                                    ... {pet_role}

                                VERSUS

{resp_desc}
                                                    ... {resp_role}

____________________________________________________________________________________

{legal_sections}
____________________________________________________________________________________

MOST RESPECTFULLY SHOWETH:

{facts_block}

GROUNDS:

{grounds_block}

PRAYER:

Wherefore, in light of the facts and circumstances stated hereinabove, it is most
respectfully prayed that this Hon'ble Court may graciously be pleased to:

{prayers_block}

AND FOR THIS ACT OF KINDNESS, THE APPLICANT AS IN DUTY BOUND SHALL EVER PRAY.


FILED BY:

                                                    {pet_role.title()}
                                                    THROUGH

PLACE: {place}                                      {adv_name}
DATE:  {date}                                       Advocate for the {pet_role.title()}
                                                    Enrollment No.: {adv_enroll}
                                                    {adv_chamber}

====================================================================================
                                 VERIFICATION
====================================================================================

I, {pet_name}, the Deponent/Applicant above-named, do hereby solemnly declare and
verify that the contents of paragraphs 1 to {len(fact_items) or 1} of the accompanying application
are true and correct to my knowledge and belief based on court/official records,
and nothing material has been concealed therefrom.

Verified at {place} on this {date}.


                                                    DEPONENT / APPLICANT

====================================================================================
                        AFFIDAVIT IN SUPPORT OF APPLICATION
====================================================================================

{court_name}, AT {court_place}

IN THE MATTER OF:
{pet_name}                                          ... {pet_role}
                                VERSUS
{resp_name}                                         ... {resp_role}

AFFIDAVIT of {pet_desc.replace(chr(10), ', ')}.

I, the deponent above-named, do hereby solemnly affirm and state as under:

1. That I am the {pet_role.title()} in the above-titled matter and as such am fully conversant
   with the facts and circumstances of the case, and competent to swear this affidavit.

2. That the accompanying {draft_type} has been drafted under my instructions and the contents
   thereof have been read over and explained to me in vernacular, which I admit as true and correct.

3. That the contents of the accompanying application may kindly be read as part and parcel
   of this affidavit for the sake of brevity and to avoid repetition.


                                                    DEPONENT

VERIFICATION:
Verified at {place} on this {date} that the contents of paragraphs 1 to 3 of the above
affidavit are true and correct to my knowledge. No part of it is false and nothing material
has been concealed therefrom.


                                                    DEPONENT
"""
    return draft.strip()


def _format_legal_notice(
    date: str,
    case_no: str,
    pet_name: str,
    pet_parent: str,
    pet_address: str,
    resp_name: str,
    resp_parent: str,
    resp_address: str,
    adv_name: str,
    adv_enroll: str,
    adv_chamber: str,
    legal_sections: str,
    fact_items: list[str],
    ground_items: list[str],
    prayer_items: list[str],
    place: str,
) -> str:
    """Format an Indian standard advocate legal notice."""
    facts_block = "\n\n".join(
        f"{i}. {f}" for i, f in enumerate(fact_items, 1)
    ) if fact_items else "1. That my client has valid legal claims against you."

    grounds_block = "\n\n".join(
        f"{chr(65 + j)}. {g}" for j, g in enumerate(ground_items)
    ) if ground_items else "A. That you are in breach of your legal obligations."

    prayers_block = "\n\n".join(
        f"({chr(97 + k)}) {p}" for k, p in enumerate(prayer_items)
    ) if prayer_items else "(a) Discharge the outstanding liability within 15 days."

    return f"""LEGAL NOTICE
BY REGISTERED POST WITH A.D. / SPEED POST / EMAIL

REF: {case_no}                                      DATE: {date}

TO,
{resp_name}
{f'S/o, D/o {resp_parent}' if resp_parent else ''}
{resp_address}

FROM:
{adv_name}, Advocate
Enrollment No.: {adv_enroll}
{adv_chamber}

UNDER INSTRUCTIONS FROM MY CLIENT:
{pet_name}
{f'S/o, D/o {pet_parent}' if pet_parent else ''}
{pet_address}
(Hereinafter referred to as "My Client")

SUBJECT:
{legal_sections}

SIR / MADAM,

Under instructions from and on behalf of my client aforesaid, I hereby serve upon
you this Legal Notice as follows:

{facts_block}

LEGAL GROUNDS:

{grounds_block}

NOW THEREFORE, I HEREBY CALL UPON YOU, BY WAY OF THIS NOTICE:

{prayers_block}

Please take notice that in the event of your failure to comply with the requisitions
contained in this Notice within fifteen (15) days from the date of its receipt, my client
has issued strict instructions to initiate appropriate civil as well as criminal
proceedings against you in the competent court of law, entirely at your risk, cost,
and consequences.

A copy of this Legal Notice has been retained in my office for record and future
legal proceedings.


Yours faithfully,



{adv_name}
Advocate for the Client
Enrollment No.: {adv_enroll}
Place: {place}
Date: {date}
""".strip()

