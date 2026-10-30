from nicegui import run, ui
from app.state import PageState
from app.components import (
    section_title,
    sub_label,
    styled_input,
    styled_select,
    primary_button,
    secondary_button,
)
from app.captcha import update_captcha_display
from app.results import display_case_number_results
from app.constants import INDIAN_STATES
from ecourts.parser import parse_dropdown_options, parse_case_number_results


# ------------------------------------------------------------------
# Section builder
# ------------------------------------------------------------------

def build_case_section(state: PageState):
    with ui.column().classes('w-full gap-4') as section:
        sub_label('Select court details to find a case by its number.')

        # Court location dropdowns
        state.state_select = styled_select(INDIAN_STATES, 'State')

        state.district_select = styled_select({}, 'District')
        state.district_select.disable()

        state.court_complex_select = styled_select({}, 'Court Complex')
        state.court_complex_select.disable()

        state.court_est_select = styled_select({}, 'Court Establishment')
        state.court_est_select.disable()

        # Case details — hidden until an establishment is selected
        with ui.column().classes('w-full gap-3') as details:
            state.case_details_section = details

            ui.separator()
            section_title('Case Information', 'folder_open')

            state.case_type_select = styled_select({}, 'Case Type')

            with ui.row().classes('w-full gap-3'):
                state.case_number_input = styled_input(
                    'Case Number',
                    placeholder='Enter case number',
                )
                state.case_year_input = styled_input(
                    'Year',
                    placeholder='e.g. 2024',
                ).props('maxlength=4')

            # CAPTCHA for case number search
            with ui.card().style(
                'background: #fffbeb; border: 1px solid #fde68a;'
            ).classes('w-full shadow-none'):
                section_title('CAPTCHA Verification', 'verified_user')

                state.case_captcha_container = ui.column().classes(
                    'min-h-14 justify-center'
                )
                with state.case_captcha_container:
                    ui.label('Loading CAPTCHA...').classes(
                        'text-sm text-gray-500'
                    )

                state.case_captcha_answer = styled_input(
                    'CAPTCHA Answer',
                    placeholder='Type the characters shown above',
                ).props('autocomplete=off')

                state.case_captcha_status = ui.label('').classes(
                    'text-sm text-gray-500'
                )

                with ui.row().classes('gap-2'):
                    state.case_refresh_btn = secondary_button(
                        'Refresh', icon='refresh',
                    )
                    state.case_search_btn = primary_button(
                        'Search Case', icon='search',
                    )
                    state.case_search_btn.disable()

        details.set_visibility(False)

    return section


# ------------------------------------------------------------------
# Cascade dropdown handlers
# ------------------------------------------------------------------

async def on_state_change(state: PageState, event):
    """Load districts when the user selects a state."""
    state_code = event.value

    state.district_select.set_value(None)
    state.district_select.options = {}
    state.district_select.update()
    state.district_select.disable()
    _reset_complex(state)

    if not state_code:
        return

    if not state.app_token:
        ui.notify('Please refresh the CAPTCHA first.', type='warning')
        return

    try:
        result = await run.io_bound(
            state.client.get_districts,
            str(state_code),
            state.app_token,
        )
        state.app_token = result['app_token']
        state.district_select.options = parse_dropdown_options(
            result['dist_list'],
        )
        state.district_select.update()
        state.district_select.enable()

        if not result['dist_list']:
            ui.notify('No districts found for this state.', type='warning')

    except Exception as exc:
        ui.notify(f'Could not load districts: {exc}', type='negative')
        print(f'District loading error: {exc}')


async def on_district_change(state: PageState, event):
    """Load court complexes when the user selects a district."""
    dist_code = event.value
    _reset_complex(state)

    if not dist_code:
        return

    state_code = state.state_select.value
    if not state_code or not state.app_token:
        ui.notify(
            'Select a state and ensure the session is active.',
            type='warning',
        )
        return

    try:
        result = await run.io_bound(
            state.client.get_court_complexes,
            str(state_code),
            str(dist_code),
            state.app_token,
        )
        state.app_token = result['app_token']
        state.court_complex_select.options = parse_dropdown_options(
            result['complex_list'],
        )
        state.court_complex_select.update()
        state.court_complex_select.enable()

        if not result['complex_list']:
            ui.notify('No court complexes found.', type='warning')

    except Exception as exc:
        ui.notify(
            f'Could not load court complexes: {exc}', type='negative',
        )
        print(f'Court complex loading error: {exc}')


async def on_complex_change(state: PageState, event):
    """Load court establishments when the user selects a complex."""
    complex_value = event.value
    _reset_establishment(state)

    if not complex_value:
        return

    state_code = state.state_select.value
    dist_code = state.district_select.value

    if not state_code or not dist_code or not state.app_token:
        ui.notify('Select the state and district first.', type='warning')
        return

    complex_code = str(complex_value).split('@')[0]

    try:
        result = await run.io_bound(
            state.client.get_court_establishments,
            str(state_code),
            str(dist_code),
            complex_code,
            state.app_token,
        )
        state.app_token = result['app_token']
        state.court_est_select.options = parse_dropdown_options(
            result['establishment_list'],
        )
        state.court_est_select.update()
        state.court_est_select.enable()

        if not result['establishment_list']:
            ui.notify('No court establishments found.', type='warning')

    except Exception as exc:
        ui.notify(
            f'Could not load court establishments: {exc}',
            type='negative',
        )
        print(f'Court establishment loading error: {exc}')


async def on_establishment_change(state: PageState, event):
    """Load case types and reveal the case detail fields."""
    est_code = event.value
    has_est = bool(est_code)

    state.case_details_section.set_visibility(has_est)

    state.case_type_select.set_value(None)
    state.case_type_select.options = {}
    state.case_type_select.update()

    if not est_code:
        return

    state_code = state.state_select.value
    dist_code = state.district_select.value
    complex_value = state.court_complex_select.value

    if not all([state_code, dist_code, complex_value, state.app_token]):
        ui.notify('Complete all court selections first.', type='warning')
        return

    complex_code = str(complex_value).split('@')[0]

    try:
        result = await run.io_bound(
            state.client.get_case_types,
            str(state_code),
            str(dist_code),
            complex_code,
            str(est_code),
            state.app_token,
        )
        state.app_token = result['app_token']
        state.case_type_select.options = parse_dropdown_options(
            result['casetype_list'],
        )
        state.case_type_select.update()

        if not result['casetype_list']:
            ui.notify('No case types found.', type='warning')

    except Exception as exc:
        ui.notify(f'Could not load case types: {exc}', type='negative')
        print(f'Case type loading error: {exc}')


# ------------------------------------------------------------------
# Case Number search handler
# ------------------------------------------------------------------

async def handle_case_search(state: PageState):
    """Validate inputs and execute a Case Number search."""
    captcha_code = (state.case_captcha_answer.value or '').strip()
    case_no = (state.case_number_input.value or '').strip()
    year = (state.case_year_input.value or '').strip()

    required = {
        'State': state.state_select.value,
        'District': state.district_select.value,
        'Court Complex': state.court_complex_select.value,
        'Establishment': state.court_est_select.value,
        'Case Type': state.case_type_select.value,
        'Case Number': case_no,
        'Year': year,
        'CAPTCHA': captcha_code,
    }
    missing = [name for name, value in required.items() if not value]

    if missing:
        ui.notify(
            'Please fill in: ' + ', '.join(missing), type='warning',
        )
        return

    if not year.isdigit() or len(year) != 4:
        ui.notify(
            'Please enter a valid four-digit year.', type='warning',
        )
        return

    if not state.app_token:
        ui.notify(
            'Please refresh the CAPTCHA and try again.', type='warning',
        )
        return

    for btn in (state.case_search_btn, state.case_refresh_btn,
                state.search_btn, state.refresh_btn):
        btn.disable()

    state.results_container.clear()
    state.case_captcha_status.set_text('Searching…')

    try:
        complex_code = str(state.court_complex_select.value).split('@')[0]

        result = await run.io_bound(
            state.client.search_with_case_number,
            str(state.case_type_select.value),
            case_no,
            year,
            captcha_code,
            str(state.state_select.value),
            str(state.district_select.value),
            complex_code,
            str(state.court_est_select.value),
            state.app_token,
        )

        # Save the rotated token.
        state.app_token = result.get('app_token', state.app_token)

        if result.get('div_captcha'):
            await update_captcha_display(state, result['div_captcha'])

        if result.get('status') != 1:
            ui.notify(
                'Search failed. Check the CAPTCHA and case details.',
                type='warning',
            )
            return

        html = result.get('case_data')
        if not html:
            ui.notify('No case results returned.', type='warning')
            return

        case_results = parse_case_number_results(html)
        display_case_number_results(state.results_container, case_results, state=state)

    except Exception as exc:
        ui.notify(f'Case Number search error: {exc}', type='negative')
        print(f'Case Number search error: {exc}')

    finally:
        for btn in (state.case_search_btn, state.case_refresh_btn,
                    state.search_btn, state.refresh_btn):
            btn.enable()


# ------------------------------------------------------------------
# Internal reset helpers
# ------------------------------------------------------------------

def _reset_complex(state: PageState):
    """Reset the court complex dropdown and everything below it."""
    state.court_complex_select.set_value(None)
    state.court_complex_select.options = {}
    state.court_complex_select.update()
    state.court_complex_select.disable()
    _reset_establishment(state)


def _reset_establishment(state: PageState):
    """Reset the court establishment dropdown and hide case details."""
    state.court_est_select.set_value(None)
    state.court_est_select.options = {}
    state.court_est_select.update()
    state.court_est_select.disable()
    if state.case_details_section is not None:
        state.case_details_section.set_visibility(False)

