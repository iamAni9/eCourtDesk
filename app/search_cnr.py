"""CNR Number search — UI section and search handler."""

from nicegui import run, ui

from app.state import PageState
from app.components import section_title, styled_input, primary_button, secondary_button
from app.results import display_cnr_results
from ecourts.parser import parse_case_details


def build_cnr_section(state: PageState):
    """Build the CNR Number search UI and populate *state* with element refs."""
    with ui.column().classes('w-full gap-4') as section:
        state.cnr_input = styled_input(
            'CNR Number',
            placeholder='e.g. DLND020000602007',
        )

        # CAPTCHA verification area
        with ui.card().style(
            'background: #fffbeb; border: 1px solid #fde68a;'
        ).classes('w-full shadow-none'):
            section_title('CAPTCHA Verification', 'verified_user')

            state.captcha_container = ui.column().classes(
                'min-h-14 justify-center'
            )
            with state.captcha_container:
                ui.label('Loading CAPTCHA...').classes(
                    'text-sm text-gray-500'
                )

            state.captcha_answer = styled_input(
                'CAPTCHA Answer',
                placeholder='Type the characters shown above',
            ).props('autocomplete=off')

            state.captcha_status = ui.label('Initializing...').classes(
                'text-sm text-gray-500'
            )

            with ui.row().classes('gap-2'):
                state.refresh_btn = secondary_button('Refresh', icon='refresh')
                state.search_btn = primary_button('Search Case', icon='search')
                state.search_btn.disable()

    return section


async def handle_cnr_search(state: PageState):
    """Validate inputs and execute a CNR Number search."""
    cnr = (state.cnr_input.value or '').strip()
    captcha_code = (state.captcha_answer.value or '').strip()

    if not cnr:
        ui.notify('Please enter a CNR number.', type='warning')
        return

    if not captcha_code:
        ui.notify('Please enter the CAPTCHA characters.', type='warning')
        return

    if not state.app_token:
        ui.notify(
            'Please refresh the CAPTCHA and try again.', type='warning',
        )
        return

    state.search_btn.disable()
    state.refresh_btn.disable()
    state.case_refresh_btn.disable()
    state.results_container.clear()
    state.captcha_status.set_text('Searching…')

    try:
        result = await run.io_bound(
            state.client.search_with_cnr,
            cnr,
            captcha_code,
            state.app_token,
        )

        if not result:
            ui.notify('Failed to fetch case details.', type='negative')
            return

        html = result.get('casetype_list')
        if not html:
            ui.notify(
                'Case details not found in response.', type='warning',
            )
            return

        case_data = parse_case_details(html)
        display_cnr_results(state.results_container, case_data)

    except Exception as exc:
        ui.notify(f'Search error: {exc}', type='negative')
        print(f'CNR search error: {exc}')

    finally:
        state.search_btn.enable()
        state.refresh_btn.enable()

