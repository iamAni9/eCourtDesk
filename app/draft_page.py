from datetime import datetime
from nicegui import ui
from app.components import *
from app.draft_templates import DRAFT_TYPES, SAMPLE_PRESETS, generate_legal_draft


def render_draft_page(
    initial_court: str = '',
    initial_case_no: str = '',
    initial_petitioner: str = '',
    initial_respondent: str = '',
    initial_type: str = 'Bail Application',
):
    ui.colors(primary='#283593')
    ui.add_css('''
        body { background: #f0f2f5; }
        .q-card { border-radius: 12px !important; }
        .legal-document {
            font-family: 'Times New Roman', Times, serif;
            line-height: 1.6;
            white-space: pre-wrap;
            background: #ffffff;
            color: #1a1a1a;
        }
    ''')

    # Top header with 'draft' active state
    page_header(active='draft')

    # Default values from sample or parameters
    preset = SAMPLE_PRESETS.get(initial_type, SAMPLE_PRESETS['Bail Application'])

    with ui.column().classes('w-full max-w-7xl mx-auto px-4 py-6 gap-6'):
        # Page Title Banner
        with ui.row().classes('w-full items-center justify-between'):
            with ui.column().classes('gap-1'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('gavel').classes('text-indigo-900 text-3xl')
                    ui.label('Legal Draft Template Generator').classes(
                        'text-2xl font-bold text-gray-900'
                    )
                sub_label(
                    'Input case facts, parties, and court details to produce a structured, court-standard legal draft.'
                )

        with ui.grid().classes('w-full grid-cols-1 lg:grid-cols-12 gap-6 items-start'):
            
            # Input Section
            with ui.column().classes('lg:col-span-6 w-full gap-4'):
                
                # Card 0: Template Selection & Quick Presets
                with ui.card().classes('w-full shadow-md'):
                    section_title('Draft Type & Presets', 'tune')

                    template_select = styled_select(
                        DRAFT_TYPES,
                        label='Select Legal Document Type',
                        value=initial_type if initial_type in DRAFT_TYPES else 'Bail Application',
                    )

                    ui.label('Quick Fill Samples:').classes('text-xs font-semibold text-gray-500 mt-1')
                    with ui.row().classes('gap-2 flex-wrap'):
                        bail_sample_btn = ui.button('Bail Appln Sample').props(
                            'outline dense no-caps size=sm color=indigo-9'
                        )
                        notice_sample_btn = ui.button('Legal Notice Sample').props(
                            'outline dense no-caps size=sm color=indigo-9'
                        )
                        civil_sample_btn = ui.button('Civil Plaint Sample').props(
                            'outline dense no-caps size=sm color=indigo-9'
                        )
                        clear_btn = ui.button('Clear Form').props(
                            'flat dense no-caps size=sm color=negative'
                        )

                # Card 1: Court & Case Information
                with ui.card().classes('w-full shadow-md'):
                    section_title('1. Court & Case Information', 'account_balance')

                    court_input = styled_input(
                        'Court Name / Forum',
                        placeholder='e.g. IN THE COURT OF PRINCIPAL DISTRICT & SESSIONS JUDGE',
                        value=initial_court or preset['court_name'],
                    )

                    with ui.row().classes('w-full gap-3'):
                        place_input = styled_input(
                            'Court Location / City',
                            placeholder='e.g. New Delhi',
                            value=preset['court_place'],
                        ).classes('w-1/2')

                        case_no_input = styled_input(
                            'Case / Application Number',
                            placeholder='e.g. Bail Appln. No. 1042/2024',
                            value=initial_case_no or preset['case_number'],
                        ).classes('w-1/2')

                    fir_input = styled_input(
                        'FIR / Police Station / Reference (if applicable)',
                        placeholder='e.g. FIR No. 128/2024, PS Connaught Place, U/s 420/406 IPC',
                        value=preset.get('fir_details', ''),
                    )

                # Card 2: Parties Information
                with ui.card().classes('w-full shadow-md'):
                    section_title('2. Parties Information', 'groups')

                    # Petitioner Section
                    ui.label('Petitioner / Applicant / Plaintiff Details:').classes(
                        'text-xs font-bold text-indigo-900 uppercase tracking-wide'
                    )
                    pet_name_input = styled_input(
                        'Petitioner / Applicant Name',
                        placeholder='e.g. Rohan Sharma',
                        value=initial_petitioner or preset['petitioner_name'],
                    )
                    with ui.row().classes('w-full gap-3'):
                        pet_parent_input = styled_input(
                            'Parent / Spouse Name',
                            placeholder='e.g. Shri Ram Sharma',
                            value=preset['petitioner_parent'],
                        ).classes('w-2/3')
                        pet_age_input = styled_input(
                            'Age (Years)',
                            placeholder='e.g. 34',
                            value=preset['petitioner_age'],
                        ).classes('w-1/3')

                    pet_address_input = styled_input(
                        'Complete Address',
                        placeholder='Full residential address',
                        value=preset['petitioner_address'],
                    )
                    pet_role_input = styled_input(
                        'Role in Cause Title',
                        placeholder='e.g. Applicant / Accused',
                        value=preset['petitioner_role'],
                    )

                    ui.separator().classes('my-2')

                    # Respondent Section
                    ui.label('Respondent / Defendant / Opposite Party Details:').classes(
                        'text-xs font-bold text-red-900 uppercase tracking-wide'
                    )
                    resp_name_input = styled_input(
                        'Respondent Name / Authority',
                        placeholder='e.g. State (NCT of Delhi)',
                        value=initial_respondent or preset['respondent_name'],
                    )
                    with ui.row().classes('w-full gap-3'):
                        resp_parent_input = styled_input(
                            'Parent / Official Department',
                            placeholder='e.g. Through Public Prosecutor',
                            value=preset['respondent_parent'],
                        ).classes('w-2/3')
                        resp_age_input = styled_input(
                            'Age (optional)',
                            placeholder='e.g. 45',
                            value=preset['respondent_age'],
                        ).classes('w-1/3')

                    resp_address_input = styled_input(
                        'Address / Location',
                        placeholder='Address of respondent',
                        value=preset['respondent_address'],
                    )
                    resp_role_input = styled_input(
                        'Role in Cause Title',
                        placeholder='e.g. Respondent / State',
                        value=preset['respondent_role'],
                    )

                    ui.separator().classes('my-2')

                    # Advocate Section
                    ui.label('Counsel / Advocate for Applicant:').classes(
                        'text-xs font-bold text-gray-700 uppercase tracking-wide'
                    )
                    with ui.row().classes('w-full gap-3'):
                        adv_name_input = styled_input(
                            'Advocate Name',
                            value=preset['advocate_name'],
                        ).classes('w-1/2')
                        adv_enroll_input = styled_input(
                            'Bar Enrollment No.',
                            value=preset['advocate_enrollment'],
                        ).classes('w-1/2')

                    adv_chamber_input = styled_input(
                        'Chamber / Office Address',
                        value=preset['advocate_chamber'],
                    )

                # Card 3: Facts, Grounds & Prayers
                with ui.card().classes('w-full shadow-md'):
                    section_title('3. Subject, Facts, Grounds & Relief', 'article')

                    sections_input = styled_input(
                        'Application Title / Legal Sections & Acts',
                        placeholder='e.g. APPLICATION UNDER SECTION 439 CrPC FOR REGULAR BAIL',
                        value=preset['legal_sections'],
                    )

                    facts_input = styled_textarea(
                        'Statement of Facts (1 per line)',
                        placeholder='Enter chronological facts of the case...',
                        value=preset['facts'],
                    ).props('rows=5')

                    grounds_input = styled_textarea(
                        'Legal Grounds & Submissions (1 per line)',
                        placeholder='Enter legal grounds supporting the prayer...',
                        value=preset['grounds'],
                    ).props('rows=5')

                    prayers_input = styled_textarea(
                        'Prayers / Relief Sought (1 per line)',
                        placeholder='Specify the exact orders/reliefs requested from the court...',
                        value=preset['prayers'],
                    ).props('rows=4')

                    with ui.row().classes('w-full gap-3'):
                        place_sign_input = styled_input(
                            'Place of Verification',
                            value=preset['place'],
                        ).classes('w-1/2')
                        date_sign_input = styled_input(
                            'Date',
                            value=preset['date'],
                        ).classes('w-1/2')

                # Generate Action Button
                generate_btn = primary_button('Generate Legal Draft', icon='description').classes(
                    'w-full py-3 text-base font-bold shadow-md'
                )

            # Document Section
            with ui.column().classes('lg:col-span-6 w-full gap-4'):
                with ui.card().classes('w-full shadow-lg border border-gray-200'):
                    
                    # Top action bar
                    with ui.row().classes('w-full items-center justify-between pb-2 border-b border-gray-200'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('description').classes('text-indigo-800 text-2xl')
                            ui.label('Structured Legal Draft').classes(
                                'text-lg font-bold text-gray-900'
                            )

                        with ui.row().classes('gap-2 items-center'):
                            copy_btn = ui.button('Copy', icon='content_copy').props(
                                'unelevated dense size=sm color=indigo-9 no-caps'
                            ).classes('px-3')

                            download_btn = ui.button('Download', icon='download').props(
                                'outline dense size=sm color=indigo-9 no-caps'
                            ).classes('px-3')

                    # Document view container
                    draft_editor = ui.textarea().props(
                        'outlined autogrow'
                    ).classes('w-full legal-document text-sm p-4 border rounded-md')

                    # Stats footer
                    stats_label = ui.label('Ready to generate.').classes(
                        'text-xs text-gray-500 italic'
                    )

        # Footer
        ui.label('eCourts Legal Draft Generator • Formats comply with Indian Court Standards').classes(
            'text-xs text-gray-400 text-center w-full py-4'
        )

    # -------------------------------------------------------------
    # Logic / Event Handlers
    # -------------------------------------------------------------
    def collect_data():
        """Collect all current input values into a dictionary."""
        return {
            'draft_type': template_select.value or 'Bail Application',
            'court_name': court_input.value or '',
            'court_place': place_input.value or '',
            'case_number': case_no_input.value or '',
            'fir_details': fir_input.value or '',
            'petitioner_name': pet_name_input.value or '',
            'petitioner_parent': pet_parent_input.value or '',
            'petitioner_age': pet_age_input.value or '',
            'petitioner_address': pet_address_input.value or '',
            'petitioner_role': pet_role_input.value or '',
            'respondent_name': resp_name_input.value or '',
            'respondent_parent': resp_parent_input.value or '',
            'respondent_age': resp_age_input.value or '',
            'respondent_address': resp_address_input.value or '',
            'respondent_role': resp_role_input.value or '',
            'advocate_name': adv_name_input.value or '',
            'advocate_enrollment': adv_enroll_input.value or '',
            'advocate_chamber': adv_chamber_input.value or '',
            'legal_sections': sections_input.value or '',
            'facts': facts_input.value or '',
            'grounds': grounds_input.value or '',
            'prayers': prayers_input.value or '',
            'place': place_sign_input.value or '',
            'date': date_sign_input.value or datetime.now().strftime('%d.%m.%Y'),
        }

    def do_generate():
        data = collect_data()
        draft_text = generate_legal_draft(data)
        draft_editor.set_value(draft_text)

        word_count = len(draft_text.split())
        line_count = len(draft_text.splitlines())
        stats_label.set_text(
            f'Generated {data["draft_type"]} • {word_count} words • {line_count} lines • Ready for court filing'
        )
        ui.notify('Legal draft generated successfully!', type='positive')

    def apply_preset(name: str):
        sample = SAMPLE_PRESETS.get(name)
        if not sample:
            return

        template_select.set_value(name if name in DRAFT_TYPES else 'Bail Application')
        court_input.set_value(sample.get('court_name', ''))
        place_input.set_value(sample.get('court_place', ''))
        case_no_input.set_value(sample.get('case_number', ''))
        fir_input.set_value(sample.get('fir_details', ''))
        pet_name_input.set_value(sample.get('petitioner_name', ''))
        pet_parent_input.set_value(sample.get('petitioner_parent', ''))
        pet_age_input.set_value(sample.get('petitioner_age', ''))
        pet_address_input.set_value(sample.get('petitioner_address', ''))
        pet_role_input.set_value(sample.get('petitioner_role', ''))
        resp_name_input.set_value(sample.get('respondent_name', ''))
        resp_parent_input.set_value(sample.get('respondent_parent', ''))
        resp_age_input.set_value(sample.get('respondent_age', ''))
        resp_address_input.set_value(sample.get('respondent_address', ''))
        resp_role_input.set_value(sample.get('respondent_role', ''))
        adv_name_input.set_value(sample.get('advocate_name', ''))
        adv_enroll_input.set_value(sample.get('advocate_enrollment', ''))
        adv_chamber_input.set_value(sample.get('advocate_chamber', ''))
        sections_input.set_value(sample.get('legal_sections', ''))
        facts_input.set_value(sample.get('facts', ''))
        grounds_input.set_value(sample.get('grounds', ''))
        prayers_input.set_value(sample.get('prayers', ''))
        place_sign_input.set_value(sample.get('place', ''))
        date_sign_input.set_value(sample.get('date', ''))

        do_generate()
        ui.notify(f'Loaded {name} preset!', type='info')

    def clear_all():
        for inp in [
            court_input, place_input, case_no_input, fir_input,
            pet_name_input, pet_parent_input, pet_age_input, pet_address_input, pet_role_input,
            resp_name_input, resp_parent_input, resp_age_input, resp_address_input, resp_role_input,
            sections_input, facts_input, grounds_input, prayers_input,
        ]:
            inp.set_value('')
        draft_editor.set_value('')
        stats_label.set_text('Form cleared.')
        ui.notify('Form cleared.', type='warning')

    async def copy_draft():
        text = draft_editor.value or ''
        if not text:
            ui.notify('No draft to copy! Please generate first.', type='warning')
            return
        await ui.run_javascript(
            f'navigator.clipboard.writeText({repr(text)})'
        )
        ui.notify('Legal draft copied to clipboard!', type='positive')

    def download_draft():
        text = draft_editor.value or ''
        if not text:
            ui.notify('No draft to download! Please generate first.', type='warning')
            return
        doc_type = (template_select.value or 'legal_draft').lower().replace(' ', '_').replace('/', '_')
        filename = f'{doc_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        ui.download(text.encode('utf-8'), filename)
        ui.notify(f'Downloading {filename}...', type='positive')

    generate_btn.on_click(do_generate)
    bail_sample_btn.on_click(lambda: apply_preset('Bail Application'))
    notice_sample_btn.on_click(lambda: apply_preset('Legal Notice'))
    civil_sample_btn.on_click(lambda: apply_preset('Civil Suit (Plaint)'))
    clear_btn.on_click(clear_all)
    copy_btn.on_click(copy_draft)
    download_btn.on_click(download_draft)

    template_select.on_value_change(lambda e: apply_preset(e.value) if e.value in SAMPLE_PRESETS else None)

    # # Initial generation on load
    # ui.timer(0.1, do_generate, once=True)