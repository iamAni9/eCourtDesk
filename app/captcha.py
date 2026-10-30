import base64
from nicegui import run, ui
from app.state import PageState


async def update_captcha_display(state: PageState, div_captcha: str):
    """Fetch the CAPTCHA image and update both CAPTCHA containers."""
    image_bytes = await run.io_bound(
        state.client.get_captcha_image,
        div_captcha,
    )

    content_type = getattr(
        state.client, 'captcha_content_type', 'image/png',
    )
    encoded = base64.b64encode(image_bytes).decode('ascii')
    src = f'data:{content_type};base64,{encoded}'

    for container in (state.captcha_container, state.case_captcha_container):
        container.clear()
        with container:
            ui.image(src).style(
                'width: 180px; height: auto; border-radius: 6px; '
                'border: 1px solid #e0e0e0;'
            )

    # Clear all answer fields on image change
    state.captcha_answer.set_value('')
    state.case_captcha_answer.set_value('')
    state.captcha_status.set_text('')
    state.case_captcha_status.set_text('')


async def load_captcha(state: PageState):
    for btn in (state.refresh_btn, state.case_refresh_btn, state.search_btn, state.case_search_btn):
        btn.disable()

    state.app_token = None
    state.captcha_status.set_text('Loading CAPTCHA...')
    state.case_captcha_status.set_text('Loading CAPTCHA...')

    try:
        result = await run.io_bound(state.client.get_captcha)

        if not result:
            raise RuntimeError(
                'The portal did not initialize the CAPTCHA.'
            )

        if not result.get('div_captcha') or not result.get('app_token'):
            raise RuntimeError(
                'CAPTCHA image or session token is missing.'
            )

        await update_captcha_display(state, result['div_captcha'])

        # Update the app token in the state for future requests. 'app_token' is the most import parameter as it will pass in all post requests as payload.
        state.app_token = result['app_token']

        # Enable search buttons after a successful CAPTCHA load.
        state.search_btn.enable()
        state.case_search_btn.enable()

    except Exception as exc:
        state.app_token = None

        for container in (state.captcha_container, state.case_captcha_container):
            container.clear()
            with container:
                ui.label('CAPTCHA could not be loaded.').classes(
                    'text-red-700 text-sm'
                )

        msg = f'Could not load CAPTCHA: {exc}'
        state.captcha_status.set_text(msg)
        state.case_captcha_status.set_text(msg)
        print(f'CAPTCHA UI error: {exc}')

    finally:
        state.refresh_btn.enable()
        state.case_refresh_btn.enable()

