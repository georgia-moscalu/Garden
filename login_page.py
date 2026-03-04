from flet import *
from colors import *
from helpers import gbox
from page_state import PageState
from validators import validate_email, validate_password
from log_in_back import login

def build_login_page(page, build_dashboard_page, build_register_page):
    state = PageState()
    state.create_inputs()

    def handle_login(e):
        ok_e, err_e = validate_email(state.email_input.value)
        if not ok_e:
            state.show_error(err_e); page.update(); return
        ok_p, err_p = validate_password(state.password_input.value)
        if not ok_p:
            state.show_error(err_p); page.update(); return
        result = login(state.email_input.value, state.password_input.value)
        if result["success"]:
            page.clean(); page.title = "ROA - Dashboard"
            page.add(build_dashboard_page())
        else:
            state.show_error(result["message"])
        page.update()

    def go_register(e):
        page.clean(); page.add(build_register_page()); page.update()

    card_col = Column(
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=0,
        controls=[
            Icon(Icons.GRASS, color=ACCENT_GREEN, size=44),
            Container(height=4),
            Text("Bine ai venit!", size=30, weight=FontWeight.W_800, color=PRIMARY_GREEN),
            Text("Cultiva-ti gradina cu placere", color=TEXT_LIGHT, size=13),
            Container(height=22),
            Container(content=state.email_input, alignment=Alignment.CENTER, width=360),
            Container(height=8),
            Container(content=state.password_input, alignment=Alignment.CENTER, width=360),
            Row(alignment=MainAxisAlignment.END, controls=[
                TextButton("Ti-ai uitat parola?", style=ButtonStyle(color=ACCENT_GREEN))
            ]),
            Container(content=state.status_message, alignment=Alignment.CENTER,
                      width=360, height=22),
            Container(height=8),
            Container(alignment=Alignment.CENTER, width=360,
                      content=ElevatedButton(
                          content=Text("Autentificare", color="white",
                                       weight=FontWeight.W_700, size=16),
                          width=290, height=50, bgcolor=ACCENT_GREEN,
                          style=ButtonStyle(shape=RoundedRectangleBorder(radius=14)),
                          on_click=handle_login,
                      )),
            Container(height=14),
            Row(spacing=0, alignment=MainAxisAlignment.CENTER, controls=[
                Text("Nu ai cont? ", color=TEXT_LIGHT, size=13),
                TextButton("Creeaza cont",
                           style=ButtonStyle(color=PRIMARY_GREEN),
                           on_click=go_register),
            ]),
        ],
    )
    body = Column(alignment=MainAxisAlignment.CENTER,
                  horizontal_alignment=CrossAxisAlignment.CENTER,
                  expand=True, controls=[gbox(card_col, h=560)])
    return body