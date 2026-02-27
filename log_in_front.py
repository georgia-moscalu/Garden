from flet import *
from log_in_back import login, register, init_db

# ═══════════════════════════════════════════════════════════════════════════
# CULORI
# ═══════════════════════════════════════════════════════════════════════════
PRIMARY_GREEN = "#2d5016"
ACCENT_GREEN  = "#00573F"
TEXT_LIGHT    = "#444444"
TEXT_DARK     = "#1b3a1b"
TEXT_ERROR    = "#cc0000"
TEXT_SUCCESS  = "#2d5016"


# ═══════════════════════════════════════════════════════════════════════════
# VALIDĂRI
# ═══════════════════════════════════════════════════════════════════════════

def validate_email(email: str) -> tuple[bool, str]:
    if not email:
        return False, "Email este obligatoriu!"
    if "@" not in email:
        return False, "Email invalid! (lipsește @)"
    if "." not in email.split("@")[1]:
        return False, "Email invalid! (lipsește domeniu)"
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    if not password:
        return False, "Parola este obligatorie!"
    if len(password) < 4:
        return False, "Parola prea scurtă (minim 4 caractere)"
    return True, ""


# ═══════════════════════════════════════════════════════════════════════════
# STARE PAGINĂ
# ═══════════════════════════════════════════════════════════════════════════

class PageState:
    def __init__(self):
        self.email_input    = None
        self.password_input = None
        self.status_message = None

    def create_inputs(self):
        self.email_input = TextField(
            width=290,
            height=50,
            hint_text="Adresă de email",
            border=InputBorder.UNDERLINE,
            border_color="#992d5016",
            focused_border_color=ACCENT_GREEN,
            prefix_icon=Icons.EMAIL_OUTLINED,
            color=TEXT_DARK,
            text_size=15,
        )

        self.password_input = TextField(
            width=290,
            height=50,
            hint_text="Parolă",
            border=InputBorder.UNDERLINE,
            border_color="#992d5016",
            focused_border_color=ACCENT_GREEN,
            prefix_icon=Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            color=TEXT_DARK,
            text_size=15,
        )

        self.status_message = Text(
            value="",
            size=13,
            text_align=TextAlign.CENTER,
            width=290,
        )

    def show_error(self, message: str):
        self.status_message.value = message
        self.status_message.color = TEXT_ERROR

    def show_success(self, message: str):
        self.status_message.value = message
        self.status_message.color = TEXT_SUCCESS


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚIA MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main(page: Page):

    init_db()

    page.window.width      = 500
    page.window.height     = 740
    page.window.min_width  = 500
    page.window.max_width  = 500
    page.window.min_height = 740
    page.window.max_height = 740
    page.window.resizable  = False
    page.padding           = 0
    page.title             = "Garden App – Autentificare"
    page.bgcolor           = "#1b3a1b"

    # ── Template ───────────────────────────────────────────────────────────

    def create_page_template(card_content, card_height=560):
        return Container(
            width=500,
            height=740,
            alignment=Alignment.CENTER,
            content=Stack(
                controls=[

                    # LAYER 1: Imagine fundal
                    Image(
                        src="pozaFundal.jpg",
                        width=500,
                        height=740,
                        fit="cover",          # ← string simplu, nu ImageFit.COVER
                    ),

                    # LAYER 2: Overlay întunecat
                    Container(
                        width=500,
                        height=740,
                        bgcolor="#77000000",
                    ),

                    # LAYER 3: Card blurat centrat
                    Container(
                        width=500,
                        height=740,
                        alignment=Alignment.CENTER,
                        content=Container(
                            width=360,
                            height=card_height,
                            bgcolor="#ccffffff",
                            border_radius=24,
                            blur=20,              # ← număr simplu, fără Blur()
                            border=border.all(1.5, "#aaffffff"),
                            padding=padding.symmetric(horizontal=24, vertical=20),
                            alignment=Alignment.CENTER,
                            content=card_content,
                        ),
                    ),
                ],
            ),
        )

    # ── Pagina LOGIN ───────────────────────────────────────────────────────

    def build_login_page():
        state = PageState()
        state.create_inputs()

        def handle_login(e):
            email_valid, email_error = validate_email(state.email_input.value)
            if not email_valid:
                state.show_error(email_error)
                page.update()
                return

            password_valid, password_error = validate_password(state.password_input.value)
            if not password_valid:
                state.show_error(password_error)
                page.update()
                return

            result = login(state.email_input.value, state.password_input.value)
            if result["success"]:
                state.show_success("Autentificare reușită!")
            else:
                state.show_error(result["message"])
            page.update()

        def handle_go_register(e):
            page.clean()
            page.add(build_register_page())
            page.update()

        card_content = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                Icon(Icons.GRASS, color=ACCENT_GREEN, size=44),
                Container(height=4),
                Text(
                    "Bine ai venit!",
                    size=30,
                    weight=FontWeight.W_800,
                    color=PRIMARY_GREEN,
                ),
                Text(
                    "Cultivă-ți grădina cu plăcere",
                    color=TEXT_LIGHT,
                    size=13,
                ),
                Container(height=22),
                Container(
                    content=state.email_input,
                    alignment=Alignment.CENTER,
                    width=360,
                ),
                Container(height=8),
                Container(
                    content=state.password_input,
                    alignment=Alignment.CENTER,
                    width=360,
                ),
                Row(
                    controls=[
                        TextButton(
                            "Ți-ai uitat parola?",
                            style=ButtonStyle(color=ACCENT_GREEN),
                        )
                    ],
                    alignment=MainAxisAlignment.END,
                ),
                Container(
                    content=state.status_message,
                    alignment=Alignment.CENTER,
                    width=360,
                    height=22,
                ),
                Container(height=8),
                Container(
                    content=ElevatedButton(
                        content=Text(
                            "Autentificare",
                            color="white",
                            weight=FontWeight.W_700,
                            size=16,
                        ),
                        width=290,
                        height=50,
                        bgcolor=ACCENT_GREEN,
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=14),
                        ),
                        on_click=handle_login,
                    ),
                    alignment=Alignment.CENTER,
                    width=360,
                ),
                Container(height=14),
                Row(
                    spacing=0,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text("Nu ai cont? ", color=TEXT_LIGHT, size=13),
                        TextButton(
                            "Creează cont",
                            style=ButtonStyle(color=PRIMARY_GREEN),
                            on_click=handle_go_register,
                        ),
                    ],
                ),
            ],
        )

        return create_page_template(card_content, card_height=560)

    # ── Pagina REGISTER ────────────────────────────────────────────────────

    def build_register_page():
        state = PageState()
        state.create_inputs()

        confirm_password_input = TextField(
            width=290,
            height=50,
            hint_text="Confirmă parola",
            border=InputBorder.UNDERLINE,
            border_color="#992d5016",
            focused_border_color=ACCENT_GREEN,
            prefix_icon=Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            color=TEXT_DARK,
            text_size=15,
        )

        def handle_register(e):
            email_valid, email_error = validate_email(state.email_input.value)
            if not email_valid:
                state.show_error(email_error)
                page.update()
                return

            password_valid, password_error = validate_password(state.password_input.value)
            if not password_valid:
                state.show_error(password_error)
                page.update()
                return

            if state.password_input.value != confirm_password_input.value:
                state.show_error("Parolele nu se potrivesc!")
                page.update()
                return

            result = register(state.email_input.value, state.password_input.value)
            if result["success"]:
                state.show_success("Cont creat! Redirecționare...")
                page.update()
                import time
                time.sleep(2)
                page.clean()
                page.add(build_login_page())
                page.update()
            else:
                state.show_error(result["message"])
                page.update()

        def handle_go_login(e):
            page.clean()
            page.add(build_login_page())
            page.update()

        card_content = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                Icon(Icons.GRASS, color=ACCENT_GREEN, size=40),
                Container(height=4),
                Text(
                    "Creează cont",
                    size=30,
                    weight=FontWeight.W_800,
                    color=PRIMARY_GREEN,
                ),
                Text(
                    "Alătură-te comunității grădinare",
                    color=TEXT_LIGHT,
                    size=13,
                ),
                Container(height=18),
                Container(
                    content=state.email_input,
                    alignment=Alignment.CENTER,
                    width=360,
                ),
                Container(height=8),
                Container(
                    content=state.password_input,
                    alignment=Alignment.CENTER,
                    width=360,
                ),
                Container(height=8),
                Container(
                    content=confirm_password_input,
                    alignment=Alignment.CENTER,
                    width=360,
                ),
                Container(height=8),
                Container(
                    content=state.status_message,
                    alignment=Alignment.CENTER,
                    width=360,
                    height=22,
                ),
                Container(height=8),
                Container(
                    content=ElevatedButton(
                        content=Text(
                            "Înregistrare",
                            color="white",
                            weight=FontWeight.W_700,
                            size=16,
                        ),
                        width=290,
                        height=50,
                        bgcolor=ACCENT_GREEN,
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=14),
                        ),
                        on_click=handle_register,
                    ),
                    alignment=Alignment.CENTER,
                    width=360,
                ),
                Container(height=12),
                Row(
                    spacing=0,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text("Ai deja cont? ", color=TEXT_LIGHT, size=13),
                        TextButton(
                            "Conectează-te",
                            style=ButtonStyle(color=PRIMARY_GREEN),
                            on_click=handle_go_login,
                        ),
                    ],
                ),
            ],
        )

        return create_page_template(card_content, card_height=610)

    # ── Start ──────────────────────────────────────────────────────────────
    page.add(build_login_page())


# ═══════════════════════════════════════════════════════════════════════════
# PORNIRE APLICAȚIE
# ═══════════════════════════════════════════════════════════════════════════

app(target=main, view=AppView.WEB_BROWSER, assets_dir="assets")