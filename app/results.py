from nicegui import ui


# Result view wrapper (Both Structured and JSON)
def _result_tabs(data: dict, build_formatted_fn):
    with ui.tabs().classes('w-full').props('dense inline-label active-color=indigo-9 indicator-color=indigo-9') as tabs:
        fmt_tab = ui.tab('Formatted', icon='view_agenda')
        json_tab = ui.tab('JSON', icon='data_object')

    with ui.tab_panels(tabs, value=fmt_tab).classes('w-full'):
        with ui.tab_panel(fmt_tab).classes('p-0 pt-2'):
            build_formatted_fn()

        with ui.tab_panel(json_tab).classes('p-0 pt-2'):
            ui.json_editor(
                {'content': {'json': data}, 'readOnly': True},
            ).classes('w-full')



def display_cnr_results(container, case_data: dict):
    container.clear()

    with container:
        _result_tabs(case_data, lambda: _build_cnr_formatted(case_data))


def _build_cnr_formatted(case_data: dict):

    # Court name banner
    court_name = case_data.get('court_name')
    if court_name:
        with ui.row().classes('w-full items-center gap-2 py-2'):
            ui.icon('account_balance').classes(
                'text-indigo-800 text-2xl'
            )
            ui.label(court_name).classes(
                'text-lg font-bold text-indigo-900'
            )

    # Case Details
    details = case_data.get('case_details', {})
    if details:
        _render_kv_card('Case Details', 'description', details)

    # Case Status
    status = case_data.get('case_status', {})
    if status:
        _render_kv_card('Case Status', 'info', status)

    # Parties
    parties = case_data.get('parties', {})
    petitioners = parties.get('petitioners', [])
    respondents = parties.get('respondents', [])
    if petitioners or respondents:
        with ui.card().props('flat bordered').classes('w-full'):
            _card_header('Parties', 'groups')
            with ui.grid(columns=2).classes('w-full gap-4'):
                with ui.column().classes('gap-1'):
                    ui.label('Petitioners').classes(
                        'text-sm font-semibold text-blue-800'
                    )
                    for p in petitioners:
                        ui.label(f'• {p}').classes(
                            'text-sm text-gray-700'
                        )
                    if not petitioners:
                        ui.label('—').classes('text-sm text-gray-400')

                with ui.column().classes('gap-1'):
                    ui.label('Respondents').classes(
                        'text-sm font-semibold text-red-800'
                    )
                    for r in respondents:
                        ui.label(f'• {r}').classes(
                            'text-sm text-gray-700'
                        )
                    if not respondents:
                        ui.label('—').classes('text-sm text-gray-400')

    # Acts & Sections
    acts = case_data.get('acts', [])
    if acts:
        with ui.card().props('flat bordered').classes('w-full'):
            _card_header('Acts & Sections', 'gavel')
            columns = [
                {'name': 'act', 'label': 'Act',
                 'field': 'act', 'align': 'left'},
                {'name': 'sections', 'label': 'Sections',
                 'field': 'sections', 'align': 'left'},
            ]
            rows = [
                {'id': i, 'act': a.get('act', '—'),
                 'sections': a.get('sections', '—')}
                for i, a in enumerate(acts)
            ]
            ui.table(columns=columns, rows=rows).props(
                'flat dense bordered'
            ).classes('w-full')

    # FIR Details
    fir = case_data.get('fir_details', {})
    if fir:
        _render_kv_card('FIR Details', 'report', fir)

    # Hearing History
    history = case_data.get('case_history', [])
    if history:
        with ui.card().props('flat bordered').classes('w-full'):
            _card_header('Hearing History', 'history')
            columns = [
                {'name': 'judge', 'label': 'Judge',
                 'field': 'judge', 'align': 'left'},
                {'name': 'date', 'label': 'Business Date',
                 'field': 'date', 'align': 'left'},
                {'name': 'hearing', 'label': 'Hearing Date',
                 'field': 'hearing', 'align': 'left'},
                {'name': 'purpose', 'label': 'Purpose',
                 'field': 'purpose', 'align': 'left'},
            ]
            rows = [
                {
                    'id': i,
                    'judge': h.get('judge', '—'),
                    'date': h.get('business_on_date', '—'),
                    'hearing': h.get('hearing_date', '—'),
                    'purpose': h.get('purpose', '—'),
                }
                for i, h in enumerate(history)
            ]
            ui.table(columns=columns, rows=rows).props(
                'flat dense bordered'
            ).classes('w-full')

    # Orders
    orders = case_data.get('orders', [])
    if orders:
        with ui.card().props('flat bordered').classes('w-full'):
            _card_header('Orders', 'article')
            columns = [
                {'name': 'num', 'label': '#',
                 'field': 'num', 'align': 'left'},
                {'name': 'date', 'label': 'Date',
                 'field': 'date', 'align': 'left'},
                {'name': 'desc', 'label': 'Description',
                 'field': 'desc', 'align': 'left'},
            ]
            rows = [
                {
                    'id': i,
                    'num': o.get('order_number', '—'),
                    'date': o.get('order_date', '—'),
                    'desc': o.get('description', '—'),
                }
                for i, o in enumerate(orders)
            ]
            ui.table(columns=columns, rows=rows).props(
                'flat dense bordered'
            ).classes('w-full')

    # Transfers
    transfers = case_data.get('transfers', [])
    if transfers:
        with ui.card().props('flat bordered').classes('w-full'):
            _card_header('Transfers', 'swap_horiz')
            columns = [
                {'name': 'reg', 'label': 'Reg. No.',
                 'field': 'reg', 'align': 'left'},
                {'name': 'date', 'label': 'Date',
                 'field': 'date', 'align': 'left'},
                {'name': 'from_c', 'label': 'From Court',
                 'field': 'from_c', 'align': 'left'},
                {'name': 'to_c', 'label': 'To Court',
                 'field': 'to_c', 'align': 'left'},
            ]
            rows = [
                {
                    'id': i,
                    'reg': t.get('registration_number', '—'),
                    'date': t.get('transfer_date', '—'),
                    'from_c': t.get('from_court', '—'),
                    'to_c': t.get('to_court', '—'),
                }
                for i, t in enumerate(transfers)
            ]
            ui.table(columns=columns, rows=rows).props(
                'flat dense bordered'
            ).classes('w-full')

    # Empty fallback
    if not any([
        details, status, petitioners, respondents,
        acts, fir, history, orders, transfers,
    ]):
        _empty_message('No case data found.')



# -------------------------------------------------------------------

def display_case_number_results(container, case_results: dict, state=None):
    container.clear()

    with container:
        _result_tabs(
            case_results,
            lambda: _build_case_number_formatted(case_results, state=state),
        )


def _build_case_number_formatted(case_results: dict, state=None):
    summary = case_results.get('summary', {})
    total = summary.get('total_cases', 0)
    est_count = summary.get('total_establishments')

    # Summary header (matching eCourts style)
    with ui.column().classes('w-full items-center py-3 gap-1'):
        with ui.row().classes('items-center justify-center gap-2 text-red-700 font-bold text-sm'):
            if est_count is not None:
                ui.label(f'Total Number of Establishments in Court Complex :  {est_count}')
                ui.label('|').classes('text-red-400 mx-1')
            ui.label(f'Total number of cases : {total or 0}')

        # Establishment link
        for est in case_results.get('establishments', []):
            court_title = est.get('court_name', '')
            c_count = est.get('case_count')
            if court_title:
                label_txt = f'{court_title}: {c_count}' if c_count is not None else court_title
                ui.label(label_txt).classes(
                    'text-blue-800 font-bold text-sm underline cursor-pointer'
                )

    cases = case_results.get('cases', [])
    if not cases:
        _empty_message('No cases matched your search.')
        return

    # Sr No | Case Type/Case Number/Case Year | Petitioner Name versus Respondent Name | View
    with ui.card().props('flat bordered').classes('w-full p-0 overflow-hidden shadow-sm'):
        # Table Header
        with ui.row().classes(
            'w-full bg-[#16325c] text-white font-bold text-sm px-4 py-3 items-center'
        ):
            ui.label('Sr No').classes('w-16')
            ui.label('Case Type/Case Number/Case Year').classes('w-64')
            ui.label('Petitioner Name versus Respondent Name').classes('flex-1')
            ui.label('View').classes('w-24 text-center')

        # Table Rows grouped by court
        current_court = None
        for index, c in enumerate(cases):
            court = c.get('court_name')
            if court and court != current_court:
                current_court = court
                with ui.row().classes(
                    'w-full bg-slate-100 px-4 py-2 font-bold text-sm text-gray-800 '
                    'border-b border-t border-slate-200'
                ):
                    ui.label(court)

            with ui.row().classes(
                'w-full px-4 py-3 items-center border-b border-gray-100 '
                'hover:bg-blue-50 transition-colors'
            ):
                # Sr No
                ui.label(c.get('serial_number') or str(index + 1)).classes(
                    'w-16 font-medium text-gray-700'
                )

                # Case Type/Case Number/Case Year
                ui.label(c.get('case_type_case_number_case_year') or '—').classes(
                    'w-64 font-semibold text-gray-900'
                )

                # Petitioner Name versus Respondent Name
                with ui.column().classes('flex-1 gap-0'):
                    petitioner = c.get('petitioner')
                    respondent = c.get('respondent')
                    if petitioner and respondent:
                        ui.label(petitioner).classes('font-medium text-gray-800')
                        ui.label('Vs').classes('text-xs font-bold text-gray-400 my-0.5')
                        ui.label(respondent).classes('font-medium text-gray-800')
                    else:
                        ui.label(
                            c.get('petitioner_versus_respondent') or '—'
                        ).classes('text-gray-800')

                # View Button
                with ui.row().classes('w-24 justify-center'):
                    ui.button(
                        'View',
                        on_click=lambda case=c: _show_case_dialog(case, state),
                    ).props('unelevated dense size=sm color=indigo-9').classes('px-3')


def _show_case_dialog(case: dict, state=None):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-lg p-6 gap-4'):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('balance').classes('text-indigo-800 text-2xl')
                ui.label(
                    case.get('case_type_case_number_case_year') or 'Case Details'
                ).classes('text-lg font-bold text-gray-800')
            ui.button(icon='close', on_click=dialog.close).props('flat dense round')

        ui.separator()

        with ui.column().classes('w-full gap-3'):
            if case.get('court_name'):
                with ui.row().classes('items-start gap-2'):
                    ui.label('Court:').classes('text-sm font-semibold text-gray-600 w-28')
                    ui.label(case['court_name']).classes('text-sm text-gray-900 flex-1')

            if case.get('cnr'):
                with ui.row().classes('items-center gap-2'):
                    ui.label('CNR Number:').classes('text-sm font-semibold text-gray-600 w-28')
                    ui.label(case['cnr']).classes(
                        'text-sm font-mono font-bold bg-indigo-50 text-indigo-900 px-2 py-0.5 rounded'
                    )
                    cnr_val = case['cnr']

                    async def copy_cnr():
                        await ui.run_javascript(f'navigator.clipboard.writeText("{cnr_val}")')
                        ui.notify(f'Copied CNR: {cnr_val}', type='positive')

                    ui.button(icon='content_copy', on_click=copy_cnr).props(
                        'flat dense size=sm color=indigo-9'
                    ).tooltip('Copy CNR Number')

            if case.get('petitioner'):
                with ui.row().classes('items-start gap-2'):
                    ui.label('Petitioner:').classes('text-sm font-semibold text-gray-600 w-28')
                    ui.label(case['petitioner']).classes('text-sm text-gray-900 flex-1')

            if case.get('respondent'):
                with ui.row().classes('items-start gap-2'):
                    ui.label('Respondent:').classes('text-sm font-semibold text-gray-600 w-28')
                    ui.label(case['respondent']).classes('text-sm text-gray-900 flex-1')

        ui.separator()

        with ui.row().classes('w-full justify-end gap-2 flex-wrap'):
            import urllib.parse
            court_q = urllib.parse.quote(case.get('court_name') or '')
            case_q = urllib.parse.quote(case.get('case_type_case_number_case_year') or '')
            pet_q = urllib.parse.quote(case.get('petitioner') or '')
            resp_q = urllib.parse.quote(case.get('respondent') or '')
            draft_url = (
                f'/legal-draft-generator?court={court_q}&case_no={case_q}'
                f'&petitioner={pet_q}&respondent={resp_q}'
            )

            ui.button(
                'Draft Document',
                icon='description',
                on_click=lambda: ui.navigate.to(draft_url),
            ).props('outline color=indigo-9 no-caps')

            if case.get('cnr') and state and hasattr(state, 'cnr_input') and state.cnr_input:
                async def use_cnr():
                    dialog.close()
                    state.cnr_input.set_value(case['cnr'])
                    ui.notify(
                        f'CNR {case["cnr"]} filled in CNR Search tab!',
                        type='info',
                    )

                ui.button(
                    'Use this CNR',
                    icon='arrow_forward',
                    on_click=use_cnr,
                ).props('unelevated color=indigo-9 no-caps')

            ui.button('Close', on_click=dialog.close).props('flat color=grey-8 no-caps')

    dialog.open()





# ------------------------------------------------------------------
# Shared helpers
# ------------------------------------------------------------------

def _card_header(title: str, icon: str):
    """Section header inside a result card."""
    with ui.row().classes('items-center gap-2 pb-2'):
        ui.icon(icon).classes('text-indigo-700')
        ui.label(title).classes('text-base font-semibold text-gray-800')


def _render_kv_card(title: str, icon: str, data: dict):
    """Render a key-value dictionary inside a bordered card."""
    with ui.card().props('flat bordered').classes('w-full'):
        _card_header(title, icon)
        with ui.grid(columns=2).classes('w-full gap-x-6 gap-y-1'):
            for key, value in data.items():
                label = key.replace('_', ' ').title()
                ui.label(label).classes(
                    'text-sm font-medium text-gray-500'
                )
                ui.label(value or '—').classes('text-sm text-gray-800')


def _empty_message(text: str):
    """A centered empty-state placeholder."""
    with ui.column().classes('w-full items-center py-6 gap-2'):
        ui.icon('info_outline').classes('text-4xl text-gray-300')
        ui.label(text).classes('text-sm text-gray-400 italic')
