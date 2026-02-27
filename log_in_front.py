from flet import *
from log_in_back import login, register, init_db

# ═══════════════════════════════════════════════════════════════════════════
# CULORI
# ═══════════════════════════════════════════════════════════════════════════
PRIMARY_GREEN = "#2d5016"
ACCENT_GREEN = "#00573F"
LIGHT_BG = "#f1free"
SOIL_BROWN = "#8b6f47"
WARM_ACCENT = "#F0E68C"
TEXT_DARK = "#1b3a1b"
TEXT_LIGHT = "#666666"
TEXT_ERROR = "red"
TEXT_SUCCESS = PRIMARY_GREEN


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚII HELPER - Validări
# ═══════════════════════════════════════════════════════════════════════════

def validate_email(email: str) -> tuple[bool, str]:
    """
    Validează un email.

    Returnează: (este_valid: bool, mesaj_eroare: str)

    De ce e separată?
    - Reutilizabil (login și register o folosesc amândoi)
    - Ușor de testat (poți verifica validări separat)
    - Ușor de modificat (schimbi logica în un singur loc)
    """
    if not email:
        return False, "Email este obligatoriu!"

    if "@" not in email:
        return False, "Email invalid! (lipsește @)"

    if "." not in email.split("@")[1]:
        return False, "Email invalid! (lipsește domeniu)"

    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validează o parolă.

    Returnează: (este_valida: bool, mesaj_eroare: str)

    De ce e separată?
    - Poți schimba cerințe (lungime, caractere speciale) în un loc
    - Clar ce se verifică
    - Ușor de testat
    """
    if not password:
        return False, "Parolă este obligatorie!"

    if len(password) < 4:
        return False, "Parolă prea scurtă (minim 4 caractere)"

    return True, ""


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚIE PENTRU STARE PAGINĂ
# ═══════════════════════════════════════════════════════════════════════════

class PageState:
    """
    Clasă pentru a ține starea paginii.

    De ce e util?
    - Centralizează toate elementele UI (input-uri, mesaje, etc)
    - Ușor de access din orice funcție
    - Clar ce elemente și stări sunt pe pagină
    - Evită să pierzi referință la elemente
    """

    def __init__(self):
        self.email_input = None
        self.password_input = None
        self.status_message = None

    def create_inputs(self):
        """Creează elementele input o singură dată"""
        self.email_input = TextField(
            width=280,
            height=50,
            hint_text='Adresă de email',
            border=InputBorder.UNDERLINE,
            prefix_icon=Icons.EMAIL,
            color='black'
        )

        self.password_input = TextField(
            width=280,
            height=50,
            hint_text='Parolă',
            border=InputBorder.UNDERLINE,
            prefix_icon=Icons.LOCK,
            password=True,
            can_reveal_password=True,
            color='black'
        )

        self.status_message = Text(
            value="",
            size=14,
            text_align=TextAlign.CENTER,
            width=280
        )

    def clear_inputs(self):
        """Golește input-urile și mesajele"""
        self.email_input.value = ""
        self.password_input.value = ""
        self.status_message.value = ""

    def show_error(self, message: str):
        """Afișează mesaj de eroare"""
        self.status_message.value = message
        self.status_message.color = TEXT_ERROR

    def show_success(self, message: str):
        """Afișează mesaj de succes"""
        self.status_message.value = message
        self.status_message.color = TEXT_SUCCESS


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚIA MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main(page: Page):
    """
    Funcția principală a aplicației.
    """

    # ───────────────────────────────────────────────────────────────────────
    # INIȚIALIZĂRI
    # ───────────────────────────────────────────────────────────────────────
    init_db()

    # Configurare pagină
    page.window_width = 500
    page.window_height = 740
    page.window_min_width = 500
    page.window_max_width = 500
    page.window_min_height = 740
    page.window_max_height = 740
    page.window_resizable = False
    page.padding = 0
    page.title = "Garden App - Autentificare"
    page.bgcolor = "#ffffff"

    # ───────────────────────────────────────────────────────────────────────
    # HELPER: Template Pagină (Gradient + Card)
    # ───────────────────────────────────────────────────────────────────────

    def create_page_template(card_content, card_height=560):
        """
        Construiește template-ul paginii (gradient + card alb).

        Parametri:
            card_content: Column cu input-uri, butoane, etc
            card_height: Înălțimea cardului (implicit 560px)

        Returnează:
            Container cu structura completa

        DE CE E EFICIENT?
        - Repetabil: ambele pagini (login și register) o folosesc
        - DRY (Don't Repeat Yourself): design-ul e scris UNA SINGURĂ DATĂ
        - Modular: dacă vrei să schimbi gradient/design, editezi AICI
        - Testabil: poți testa template separat de conținut
        """
        return Container(
            alignment=Alignment(0, 0),
            width=500,
            height=740,
            content=Stack(
                alignment=Alignment(0, 0),
                controls=[
                    # LAYER 1: Gradient Background
                    Container(
                        width=500,
                        height=740,
                        gradient=LinearGradient(
                            colors=[ACCENT_GREEN, WARM_ACCENT],
                            begin=Alignment(-1, -1),
                            end=Alignment(1, 1),
                        ),
                    ),

                    # LAYER 2: White Card (apare deasupra)
                    Container(
                        bgcolor="#ffffff",
                        opacity=0.85,
                        border_radius=20,
                        width=360,
                        height=card_height,  # Variabil!
                        alignment=Alignment(0, 0),
                        padding=Padding.symmetric(horizontal=20),
                        content=card_content,  # Conținut variabil
                    ),
                ]
            )
        )

    # ───────────────────────────────────────────────────────────────────────
    # PAGINA DE LOGIN
    # ───────────────────────────────────────────────────────────────────────

    def build_login_page():
        """
        Construiește și returnează pagina de login.
        """

        # Creează stare pentru aceasta pagină
        state = PageState()
        state.create_inputs()

        # ───────────────────────────────────────────────────────────────────
        # HANDLER: Login Button
        # ───────────────────────────────────────────────────────────────────

        def handle_login(e):
            """
            Se execută când user apasă butonul "Autentificare".

            FLOW:
            1. Validează email
            2. Validează parolă
            3. Apelează backend login()
            4. Afișează mesaj (succes/eroare)
            5. Reîncarcă UI cu page.update()
            """

            # 1. VALIDARE EMAIL
            email_valid, email_error = validate_email(state.email_input.value)
            if not email_valid:
                state.show_error(email_error)
                page.update()
                return  # STOP - nu continua mai departe

            # 2. VALIDARE PAROLĂ
            password_valid, password_error = validate_password(
                state.password_input.value
            )
            if not password_valid:
                state.show_error(password_error)
                page.update()
                return  # STOP

            # 3. APELEAZĂ BACKEND
            result = login(
                state.email_input.value,
                state.password_input.value
            )

            # 4. PROCESEAZĂ RĂSPUNS
            if result["success"]:
                state.show_success("Autentificare reușită!")
                # TODO: Redirecționează la pagina dashboard
            else:
                state.show_error(result["message"])

            # 5. REDESENEAZĂ UI
            page.update()

        # ───────────────────────────────────────────────────────────────────
        # HANDLER: Link "Creează cont"
        # ───────────────────────────────────────────────────────────────────

        def handle_go_register(e):
            """
            Se execută când user apasă "Creează cont".

            Schimbă pagina de LOGIN → REGISTER.
            """
            page.clean()  # Șterge conținut
            page.add(build_register_page())  # Adaugă pagina nouă
            page.update()  # Reîncarcă

        # ───────────────────────────────────────────────────────────────────
        # CONSTRUIEȘTE INTERFAȚA
        # ───────────────────────────────────────────────────────────────────

        card_content = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                # Titlu
                Text(
                    "Bine ai venit",
                    size=34,
                    weight=FontWeight.W_800,
                    color=PRIMARY_GREEN,
                    font_family="Poppins"
                ),

                # Subtitlu
                Text(
                    "Cultivă-ți grădina cu plăcere",
                    color=TEXT_LIGHT,
                    size=14
                ),

                # Spațiu
                Container(height=25),

                # Email Input
                Container(
                    content=state.email_input,
                    alignment=Alignment(0, 0),
                    width=360
                ),
                Container(height=12),

                # Password Input
                Container(
                    content=state.password_input,
                    alignment=Alignment(0, 0),
                    width=360
                ),

                # Link "Ți-ai uitat parola?"
                Row(
                    controls=[
                        TextButton(
                            "Ți-ai uitat parola?",
                            style=ButtonStyle(color=ACCENT_GREEN)
                        )
                    ],
                    alignment=MainAxisAlignment.START,
                ),
                Container(height=5),

                # Status Message (eroare/succes)
                Container(
                    content=state.status_message,
                    alignment=Alignment(0, 0),
                    width=360
                ),
                Container(height=10),

                # Buton Autentificare
                Container(
                    content=ElevatedButton(
                        content=Text(
                            "Autentificare",
                            color='white',
                            weight=FontWeight.W_700,
                            size=16
                        ),
                        width=280,
                        height=50,
                        bgcolor=ACCENT_GREEN,
                        on_click=handle_login  # ← Handler pentru click
                    ),
                    alignment=Alignment(0, 0),
                    width=360,
                ),
                Container(height=14),

                # Link "Creează cont"
                Container(
                    content=Row(
                        spacing=-10,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(
                                "Nu ai cont? ",
                                color=TEXT_LIGHT,
                                size=13
                            ),
                            TextButton(
                                "Creează cont",
                                style=ButtonStyle(color=PRIMARY_GREEN),
                                on_click=handle_go_register  # ← Handler
                            ),
                        ],
                    ),
                    width=360,
                    alignment=Alignment(0, 0),
                ),
            ],
        )

        # Returnează pagina cu template-ul
        return create_page_template(card_content, card_height=560)

    # ───────────────────────────────────────────────────────────────────────
    # PAGINA DE REGISTER
    # ───────────────────────────────────────────────────────────────────────

    def build_register_page():
        """
        Construiește și returnează pagina de register.

        Similar cu login_page, dar cu 3 input-uri și validări suplimentare.
        """

        # Creează stare pentru aceasta pagină
        state = PageState()
        state.create_inputs()

        # Input suplimentar pentru register
        confirm_password_input = TextField(
            width=280,
            height=50,
            hint_text='Confirmă parolă',
            border=InputBorder.UNDERLINE,
            prefix_icon=Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            color='black'
        )

        # ───────────────────────────────────────────────────────────────────
        # HANDLER: Register Button
        # ───────────────────────────────────────────────────────────────────

        def handle_register(e):
            """
            Se execută când user apasă butonul "Înregistrare".

            FLOW:
            1. Validează email
            2. Validează parolă
            3. Validează că parolele se potrivesc
            4. Apelează backend register()
            5. Afișează mesaj (succes/eroare)
            6. Reîncarcă UI
            """

            # 1. VALIDARE EMAIL
            email_valid, email_error = validate_email(state.email_input.value)
            if not email_valid:
                state.show_error(email_error)
                page.update()
                return

            # 2. VALIDARE PAROLĂ
            password_valid, password_error = validate_password(
                state.password_input.value
            )
            if not password_valid:
                state.show_error(password_error)
                page.update()
                return

            # 3. VALIDARE: Parolele se potrivesc?
            if state.password_input.value != confirm_password_input.value:
                state.show_error("Parolele nu se potrivesc!")
                page.update()
                return

            # 4. APELEAZĂ BACKEND
            result = register(
                state.email_input.value,
                state.password_input.value
            )

            # 5. PROCESEAZĂ RĂSPUNS
            if result["success"]:
                state.show_success("Cont creat cu succes! Te poți autentifica.")
                # TODO: Redirecționează la login
            else:
                state.show_error(result["message"])

            # 6. REDESENEAZĂ UI
            page.update()

        # ───────────────────────────────────────────────────────────────────
        # HANDLER: Link "Conectează-te"
        # ───────────────────────────────────────────────────────────────────

        def handle_go_login(e):
            """
            Se execută când user apasă "Conectează-te".

            Schimbă pagina de REGISTER → LOGIN.
            """
            page.clean()
            page.add(build_login_page())
            page.update()

        # ───────────────────────────────────────────────────────────────────
        # CONSTRUIEȘTE INTERFAȚA
        # ───────────────────────────────────────────────────────────────────

        card_content = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                # Titlu
                Text(
                    "Creează cont",
                    size=34,
                    weight=FontWeight.W_800,
                    color=PRIMARY_GREEN,
                    font_family="Poppins"
                ),

                # Subtitlu
                Text(
                    "Alătură-te comunității grădinare",
                    color=TEXT_LIGHT,
                    size=14
                ),

                # Spațiu
                Container(height=25),

                # Email Input
                Container(
                    content=state.email_input,
                    alignment=Alignment(0, 0),
                    width=360
                ),
                Container(height=12),

                # Password Input
                Container(
                    content=state.password_input,
                    alignment=Alignment(0, 0),
                    width=360
                ),
                Container(height=12),

                # Confirm Password Input
                Container(
                    content=confirm_password_input,
                    alignment=Alignment(0, 0),
                    width=360
                ),
                Container(height=12),

                # Status Message
                Container(
                    content=state.status_message,
                    alignment=Alignment(0, 0),
                    width=360
                ),
                Container(height=10),

                # Buton Înregistrare
                Container(
                    content=ElevatedButton(
                        content=Text(
                            "Înregistrare",
                            color='white',
                            weight=FontWeight.W_700,
                            size=16
                        ),
                        width=280,
                        height=50,
                        bgcolor=ACCENT_GREEN,
                        on_click=handle_register  # ← Handler
                    ),
                    alignment=Alignment(0, 0),
                    width=360,
                ),
                Container(height=14),

                # Link "Conectează-te"
                Container(
                    content=Row(
                        spacing=-10,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(
                                "Ai deja cont? ",
                                color=TEXT_LIGHT,
                                size=13
                            ),
                            TextButton(
                                "Conectează-te",
                                style=ButtonStyle(color=PRIMARY_GREEN),
                                on_click=handle_go_login  # ← Handler
                            ),
                        ],
                    ),
                    width=360,
                    alignment=Alignment(0, 0),
                ),
            ],
        )

        # Returnează pagina cu template-ul (card mai înalt pentru 3 input-uri)
        return create_page_template(card_content, card_height=600)

    # ───────────────────────────────────────────────────────────────────────
    # INIȚIALIZARE: Afișează pagina de LOGIN
    # ───────────────────────────────────────────────────────────────────────

    page.add(build_login_page())


# ═══════════════════════════════════════════════════════════════════════════
# PORNIRE APLICAȚIE
# ═══════════════════════════════════════════════════════════════════════════

app(target=main, view=AppView.WEB_BROWSER)