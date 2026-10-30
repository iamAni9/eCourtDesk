import os
from nicegui import ui
from app.state import PageState
from app.components import page_header, section_title
from app.captcha import load_captcha
from app.draft_page import render_draft_page
from app.search_cnr import build_cnr_section, handle_cnr_search
from app.search_case import build_case_section, handle_case_search, on_state_change, on_district_change, on_complex_change, on_establishment_change

# Case Search page
@ui.page('/')
def home():
    state = PageState()

    # -- Theme ----------------------------------------------------------
    ui.colors(primary='#283593')
    ui.add_css('''
        body { background: #f0f2f5; }
        .q-card { border-radius: 12px !important; }
        .q-tab  { text-transform: none !important; font-weight: 600; }
    ''')

    # -- Header ---------------------------------------------------------
    page_header(active='search')

    # -- Main content ---------------------------------------------------
    with ui.column().classes(
        'w-full max-w-4xl mx-auto px-4 py-8 gap-6 items-center'
    ):
        with ui.card().classes('w-full shadow-lg'):
            section_title('Case Search', 'search')

            # Navigation between CNR and Case Number search
            with ui.tabs().classes('w-full') as tabs:
                cnr_tab = ui.tab('CNR Number', icon='tag')
                case_tab = ui.tab('Case Number', icon='folder')

            ui.separator()

            with ui.tab_panels(tabs, value=cnr_tab).classes('w-full'):
                with ui.tab_panel(cnr_tab):
                    build_cnr_section(state)

                with ui.tab_panel(case_tab):
                    build_case_section(state)

            # Results section
            ui.separator()
            with ui.row().classes('items-center gap-2'):
                ui.icon('analytics').classes('text-indigo-800')
                ui.label('Results').classes(
                    'text-lg font-semibold text-gray-800'
                )

            state.results_container = ui.column().classes('w-full gap-3')
            with state.results_container:
                with ui.column().classes(
                    'w-full items-center py-8 gap-2'
                ):
                    ui.icon('search').classes('text-5xl text-gray-300')
                    ui.label(
                        'Search for a case to see results here.'
                    ).classes('text-sm text-gray-400')

        # Footer
        ui.label('Created By Aniket Chaudhary').classes(
            'text-xs text-gray-400 text-center'
        )

    # -- Wire event handlers -------------------------------------------
    state.refresh_btn.on_click(lambda: load_captcha(state))
    state.case_refresh_btn.on_click(lambda: load_captcha(state))
    state.search_btn.on_click(lambda: handle_cnr_search(state))
    state.case_search_btn.on_click(lambda: handle_case_search(state))

    state.state_select.on_value_change(
        lambda e: on_state_change(state, e),
    )
    state.district_select.on_value_change(
        lambda e: on_district_change(state, e),
    )
    state.court_complex_select.on_value_change(
        lambda e: on_complex_change(state, e),
    )
    state.court_est_select.on_value_change(
        lambda e: on_establishment_change(state, e),
    )

    # Loading CAPTCHA on first page visit.
    ui.timer(0.1, lambda: load_captcha(state), once=True)


# Legal Draft Generator page
@ui.page('/legal-draft-generator')
def draft(
    court: str = '',
    case_no: str = '',
    petitioner: str = '',
    respondent: str = '',
    type: str = 'Bail Application',
):
    render_draft_page(
        initial_court=court,
        initial_case_no=case_no,
        initial_petitioner=petitioner,
        initial_respondent=respondent,
        initial_type=type,
    )


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='eCourtDesk',
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080)),
        reload=False,
        show=False,
    )