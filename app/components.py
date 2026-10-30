from nicegui import ui

# Components for builing UI

def page_header(active: str = 'search'):
    with ui.header().style(
        'background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);'
    ).classes('items-center justify-between px-6 py-2 shadow-lg'):
        
        # Brand logo and title
        with ui.link(target='/').classes('no-underline text-white flex items-center gap-3 cursor-pointer'):
            ui.icon('balance').classes('text-3xl text-white')
            with ui.column().classes('gap-0'):
                ui.label('eCourtDesk').classes(
                    'text-xl font-bold text-white leading-tight'
                )
                ui.label(
                    'Search court cases & generate legal drafts'
                ).classes('text-xs text-indigo-200 leading-tight')

        # Navigation buttons (Case Search and Legal Draft Generator)
        with ui.row().classes('items-center gap-2'):
            search_btn = ui.button(
                'Case Search',
                icon='search',
                on_click=lambda: ui.navigate.to('/'),
            )
            if active == 'search':
                search_btn.props('unelevated no-caps text-color=white').classes('bg-white/25 font-semibold')
            else:
                search_btn.props('flat no-caps text-color=indigo-2')

            draft_btn = ui.button(
                'Legal Draft Generator',
                icon='description',
                on_click=lambda: ui.navigate.to('/legal-draft-generator'),
            )
            if active == 'draft':
                draft_btn.props('unelevated no-caps text-color=white').classes('bg-white/25 font-semibold')
            else:
                draft_btn.props('flat no-caps text-color=indigo-2')


def section_title(text: str, icon: str = None):
    with ui.row().classes('items-center gap-2'):
        if icon:
            ui.icon(icon).classes('text-indigo-800 text-xl')
        ui.label(text).classes('text-lg font-semibold text-gray-800')


def sub_label(text: str):
    ui.label(text).classes('text-sm text-gray-500')


def styled_input(label: str, placeholder: str = '', **kwargs):
    return (
        ui.input(label=label, placeholder=placeholder, **kwargs)
        .props('outlined dense')
        .classes('w-full')
    )


def styled_textarea(label: str, placeholder: str = '', **kwargs):
    return (
        ui.textarea(label=label, placeholder=placeholder, **kwargs)
        .props('outlined autogrow')
        .classes('w-full')
    )


def styled_select(options, label: str, **kwargs):
    return (
        ui.select(options=options, label=label, **kwargs)
        .props('outlined dense clearable')
        .classes('w-full')
    )


def primary_button(text: str, icon: str = None):
    btn = ui.button(text, icon=icon)
    btn.props('unelevated no-caps color=indigo-9')
    btn.classes('px-6')
    return btn


def secondary_button(text: str, icon: str = None):
    btn = ui.button(text, icon=icon)
    btn.props('outline no-caps color=indigo-9')
    btn.classes('px-4')
    return btn
