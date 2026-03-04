from flet import *
from colors import *
from helpers import gbox
from page_state import PageState
from validators import validate_email, validate_password
from log_in_back import register

def build_register_page(page, build_login_page):
    state = PageState()
    state.create_inputs()
    confirm = TextField(
        width=290, height=50, hint_text="Confirma parola",
        border=InputBorder.UNDERLINE, border_color="#992d5016",
        focused_border_color=ACCENT_GREEN, prefix_icon=Icons.LOCK_OUTLINE,
        password=True, can_reveal_password=True, color=TEXT_DARK, text_size=15,
    )

    def handle_register(e):
        ok_e, err_e = validate_email(state.email_input.value)
        if not ok_e:
            state.show_error(err_e); page.update(); return
        ok_p, err_p = validate_password(state.password_input.value)
        if not ok_p:
            state.show_error(err_p); page.update(); return
        if state.password_input.value != confirm.value:
            state.show_error("Parolele nu se potrivesc!"); page.update(); return
        result = register(state.email_input.value, state.password_input.value)
        if result["success"]:
            state.show_success("Cont creat! Redirectionare...")
            page.update()
            import time; time.sleep(2)
            page.clean(); page.add(build_login_page())
        else:
            state.show_error(result["message"])
        page.update()

    def go_login(e):
        page.clean(); page.add(build_login_page()); page.update()

    card_col = Column(
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=0,
        controls=[
            Icon(Icons.GRASS, color=ACCENT_GREEN, size=40),
            Container(height=4),
            Text("Creeaza cont", size=30, weight=FontWeight.W_800, color=PRIMARY_GREEN),
            Text("Alatura-te comunitatii gradinare", color=TEXT_LIGHT, size=13),
            Container(height=18),
            Container(content=state.email_input, alignment=Alignment.CENTER, width=360),
            Container(height=8),
            Container(content=state.password_input, alignment=Alignment.CENTER, width=360),
            Container(height=8),
            Container(content=confirm, alignment=Alignment.CENTER, width=360),
            Container(height=8),
            Container(content=state.status_message, alignment=Alignment.CENTER,
                      width=360, height=22),
            Container(height=8),
            Container(alignment=Alignment.CENTER, width=360,
                      content=ElevatedButton(
                          content=Text("Inregistrare", color="white",
                                       weight=FontWeight.W_700, size=16),
                          width=290, height=50, bgcolor=ACCENT_GREEN,
                          style=ButtonStyle(shape=RoundedRectangleBorder(radius=14)),
                          on_click=handle_register,
                      )),
            Container(height=12),
            Row(spacing=0, alignment=MainAxisAlignment.CENTER, controls=[
                Text("Ai deja cont? ", color=TEXT_LIGHT, size=13),
                TextButton("Conecteaza-te",
                           style=ButtonStyle(color=PRIMARY_GREEN),
                           on_click=go_login),
            ]),
        ],
    )
    body = Column(alignment=MainAxisAlignment.CENTER,
                  horizontal_alignment=CrossAxisAlignment.CENTER,
                  expand=True, controls=[gbox(card_col, h=610)])
    return body