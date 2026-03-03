from flet import *
from log_in_back import login, register, init_db

# =============================================================================
# CULORI
# =============================================================================
PRIMARY_GREEN = "#2d5016"
ACCENT_GREEN  = "#00573F"
ACCENT_MID    = "#3a8a50"
TEXT_LIGHT    = "#444444"
TEXT_DARK     = "#1b3a1b"
TEXT_SUB      = "#4a7a4a"
TEXT_ERROR    = "#cc0000"
TEXT_SUCCESS  = "#2d5016"
GLASS_BG      = "#d9ffffff"
GLASS_CARD    = "#c2ffffff"
GLASS_CHIP    = "#aaffffff"
GLASS_BORDER  = "#66ffffff"
OVERLAY       = "#66000000"
HUM_GREEN     = "#27ae60"
HUM_AMBER     = "#f39c12"
HUM_RED       = "#e74c3c"
AMBER_W       = "#f39c12"

# =============================================================================
# BAZA DE DATE PLANTE ROMANESTI
# =============================================================================
ROMANIAN_PLANTS_DB = [
    {"name": "Afine",            "emoji": "🫐", "hum_threshold": 65},
    {"name": "Anghinare",        "emoji": "🌿", "hum_threshold": 60},
    {"name": "Ardei",            "emoji": "🫑", "hum_threshold": 60},
    {"name": "Ardei iuti",       "emoji": "🌶", "hum_threshold": 55},
    {"name": "Broccoli",         "emoji": "🥦", "hum_threshold": 65},
    {"name": "Busuioc",          "emoji": "🌿", "hum_threshold": 60},
    {"name": "Capsuni",          "emoji": "🍓", "hum_threshold": 65},
    {"name": "Cartofi",          "emoji": "🥔", "hum_threshold": 60},
    {"name": "Castraveti",       "emoji": "🥒", "hum_threshold": 70},
    {"name": "Ceapa",            "emoji": "🧅", "hum_threshold": 50},
    {"name": "Cimbru",           "emoji": "🌿", "hum_threshold": 40},
    {"name": "Cires",            "emoji": "🍒", "hum_threshold": 55},
    {"name": "Conopida",         "emoji": "🥦", "hum_threshold": 65},
    {"name": "Dovleac",          "emoji": "🎃", "hum_threshold": 60},
    {"name": "Dovlecel",         "emoji": "🥒", "hum_threshold": 65},
    {"name": "Fasole",           "emoji": "🫘", "hum_threshold": 60},
    {"name": "Floarea soarelui", "emoji": "🌻", "hum_threshold": 50},
    {"name": "Lavanda",          "emoji": "💜", "hum_threshold": 35},
    {"name": "Loboda",           "emoji": "🌿", "hum_threshold": 65},
    {"name": "Marar",            "emoji": "🌿", "hum_threshold": 55},
    {"name": "Mazare",           "emoji": "🟢", "hum_threshold": 65},
    {"name": "Menta",            "emoji": "🌿", "hum_threshold": 65},
    {"name": "Mere",             "emoji": "🍎", "hum_threshold": 50},
    {"name": "Morcovi",          "emoji": "🥕", "hum_threshold": 55},
    {"name": "Patrunjel",        "emoji": "🌿", "hum_threshold": 55},
    {"name": "Pere",             "emoji": "🍐", "hum_threshold": 55},
    {"name": "Porumb",           "emoji": "🌽", "hum_threshold": 65},
    {"name": "Prune",            "emoji": "🍑", "hum_threshold": 55},
    {"name": "Ridichi",          "emoji": "🔴", "hum_threshold": 60},
    {"name": "Rosii",            "emoji": "🍅", "hum_threshold": 65},
    {"name": "Rozmarin",         "emoji": "🌿", "hum_threshold": 40},
    {"name": "Salata",           "emoji": "🥬", "hum_threshold": 70},
    {"name": "Sfecla rosie",     "emoji": "🔴", "hum_threshold": 60},
    {"name": "Spanac",           "emoji": "🥬", "hum_threshold": 65},
    {"name": "Struguri",         "emoji": "🍇", "hum_threshold": 55},
    {"name": "Telina",           "emoji": "🌿", "hum_threshold": 70},
    {"name": "Usturoi",          "emoji": "🧄", "hum_threshold": 45},
    {"name": "Varza",            "emoji": "🥬", "hum_threshold": 65},
    {"name": "Vinete",           "emoji": "🍆", "hum_threshold": 60},
    {"name": "Zmeura",           "emoji": "🍓", "hum_threshold": 60},
]

# =============================================================================
# VALIDARI
# =============================================================================

def validate_email(email: str) -> tuple[bool, str]:
    if not email:
        return False, "Email este obligatoriu!"
    if "@" not in email:
        return False, "Email invalid! (lipseste @)"
    if "." not in email.split("@")[1]:
        return False, "Email invalid! (lipseste domeniu)"
    return True, ""

def validate_password(password: str) -> tuple[bool, str]:
    if not password:
        return False, "Parola este obligatorie!"
    if len(password) < 4:
        return False, "Parola prea scurta (minim 4 caractere)"
    return True, ""

# =============================================================================
# STARE PAGINA
# =============================================================================

class PageState:
    def __init__(self):
        self.email_input    = None
        self.password_input = None
        self.status_message = None

    def create_inputs(self):
        self.email_input = TextField(
            width=290, height=50, hint_text="Adresa de email",
            border=InputBorder.UNDERLINE, border_color="#992d5016",
            focused_border_color=ACCENT_GREEN, prefix_icon=Icons.EMAIL_OUTLINED,
            color=TEXT_DARK, text_size=15,
        )
        self.password_input = TextField(
            width=290, height=50, hint_text="Parola",
            border=InputBorder.UNDERLINE, border_color="#992d5016",
            focused_border_color=ACCENT_GREEN, prefix_icon=Icons.LOCK_OUTLINE,
            password=True, can_reveal_password=True, color=TEXT_DARK, text_size=15,
        )
        self.status_message = Text(value="", size=13,
                                    text_align=TextAlign.CENTER, width=290)

    def show_error(self, msg: str):
        self.status_message.value = msg
        self.status_message.color = TEXT_ERROR

    def show_success(self, msg: str):
        self.status_message.value = msg
        self.status_message.color = TEXT_SUCCESS

# =============================================================================
# HELPERS
# =============================================================================

def hum_color(h: int) -> str:
    if h >= 55: return HUM_GREEN
    if h >= 40: return HUM_AMBER
    return HUM_RED

def gbox(content, w=360, h=None, rad=24, bg=GLASS_BG,
         pad=padding.symmetric(horizontal=24, vertical=20)) -> Container:
    return Container(
        width=w, height=h, bgcolor=bg, border_radius=rad,
        blur=20, border=border.all(1.5, GLASS_BORDER),
        padding=pad, content=content,
    )

# =============================================================================
# AI ADVICE ENGINE
# =============================================================================

def advice_engine(temp, hum, a_hum, b_hum) -> str:
    lines = []
    if temp >= 34:
        lines.append(f"Alerta: stres termic extrem ({temp}C)! Activati irigarea de urgenta.")
    elif temp >= 29:
        if hum < 50:
            lines.append("Caldura + umiditate scazuta - cresteti udarea cu 30%, evitati orele 11-16.")
        else:
            lines.append(f"Temperaturi ridicate ({temp}C). Umiditate acceptabila - monitorizati la 3h.")
    elif temp <= 11:
        lines.append(f"Temperaturi scazute ({temp}C) - reduceti irigarea, risc de inghet.")
    else:
        lines.append(f"Conditii optime ({temp}C, {hum}%). Mentineti programul curent.")
    if hum > 85:
        lines.append("Suprasaturare detectata - suspendati irigarea 24h.")
    elif hum < 38:
        lines.append("Umiditate critica globala - irigare imediata necesara.")
    if abs(a_hum - b_hum) > 20:
        low = "prima planta" if a_hum < b_hum else "a doua planta"
        lines.append(f"Dezechilibru hidric - {low} are nevoie de atentie suplimentara.")
    return "  ".join(lines)

# =============================================================================
# DATE MOCK
# =============================================================================
SOLAR_TEMP   = 28
AVG_HUMIDITY = 64

# =============================================================================
# MAIN
# =============================================================================

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
    page.title             = "ROA - Smart Garden"
    page.bgcolor           = "#1b3a1b"

    # ── Lista plante (stare globala in sesiune) ────────────────────────────────
    user_plants = [
        {"name": "Rosii",      "emoji": "🍅", "humidity": 60, "temp": 27, "hum_threshold": 65},
        {"name": "Busuioc",    "emoji": "🌿", "humidity": 70, "temp": 26, "hum_threshold": 60},
        {"name": "Ardei iuti", "emoji": "🌶", "humidity": 50, "temp": 29, "hum_threshold": 55},
        {"name": "Capsuni",    "emoji": "🍓", "humidity": 65, "temp": 25, "hum_threshold": 65},
    ]

    # ── Shell comun ────────────────────────────────────────────────────────────
    def page_shell(body) -> Container:
        return Container(
            width=500, height=740,
            content=Stack(controls=[
                Image(src="pozaFundal.jpg", width=500, height=740, fit="cover"),
                Container(width=500, height=740, bgcolor=OVERLAY),
                Container(width=500, height=740, content=body),
            ]),
        )

    # =========================================================================
    # LOGIN
    # =========================================================================
    def build_login_page():
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
        return page_shell(body)

    # =========================================================================
    # REGISTER
    # =========================================================================
    def build_register_page():
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
        return page_shell(body)

    # =========================================================================
    # ADAUGA PLANTA
    # =========================================================================
    def build_add_plant_page():
        selected = {"plant": None}
        status_msg = Text(value="", size=13, height=20,
                          text_align=TextAlign.CENTER, color=TEXT_ERROR)

        suggestions_list = ListView(height=0, spacing=0, padding=padding.all(0))
        suggestions_wrap = Container(
            bgcolor="white",
            border_radius=BorderRadius(0, 0, 12, 12),
            border=border.all(1, "#cccccc"),
            content=suggestions_list,
            visible=False,
            clip_behavior=ClipBehavior.HARD_EDGE,
        )

        def on_search_change(e):
            q = (e.control.value or "").strip().lower()
            suggestions_list.controls.clear()
            if len(q) >= 1:
                matches = [p for p in ROMANIAN_PLANTS_DB
                           if p["name"].lower().startswith(q)][:6]
                if matches:
                    for plant in matches:
                        def make_select(p):
                            def on_select(ev):
                                search_field.value = p["name"]
                                selected["plant"] = p
                                suggestions_list.controls.clear()
                                suggestions_wrap.visible = False
                                page.update()
                            return on_select

                        item = GestureDetector(
                            on_tap=make_select(plant),
                            content=Container(
                                padding=padding.symmetric(horizontal=14, vertical=9),
                                border=border.only(bottom=BorderSide(1, "#eeeeee")),
                                bgcolor="white",
                                content=Row(
                                    spacing=10,
                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Text(plant["emoji"], size=22),
                                        Column(spacing=1, controls=[
                                            Text(plant["name"], size=14,
                                                 weight=FontWeight.W_600, color=TEXT_DARK),
                                            Text(f"Prag umiditate: {plant['hum_threshold']}%",
                                                 size=11, color=TEXT_SUB),
                                        ]),
                                    ],
                                ),
                            ),
                        )
                        suggestions_list.controls.append(item)
                    suggestions_list.height = min(len(matches), 4) * 52
                    suggestions_wrap.visible = True
                else:
                    suggestions_wrap.visible = False
                    selected["plant"] = None
            else:
                suggestions_wrap.visible = False
                selected["plant"] = None
            page.update()

        search_field = TextField(
            hint_text="Cauta planta (ex: R → Rosii, Ridichi...)",
            hint_style=TextStyle(color="#aaaaaa", size=13),
            border=InputBorder.UNDERLINE,
            border_color="#992d5016",
            focused_border_color=ACCENT_GREEN,
            prefix_icon=Icons.SEARCH_ROUNDED,
            color=TEXT_DARK, text_size=15,
            on_change=on_search_change,
        )

        def handle_add(e):
            if not selected["plant"]:
                status_msg.value = "Selecteaza o planta din lista!"
                page.update(); return
            p = selected["plant"]
            if any(pl["name"] == p["name"] for pl in user_plants):
                status_msg.value = f"{p['name']} este deja in gradina ta!"
                page.update(); return
            user_plants.append({
                "name":          p["name"],
                "emoji":         p["emoji"],
                "humidity":      p["hum_threshold"],
                "temp":          SOLAR_TEMP,
                "hum_threshold": p["hum_threshold"],
            })
            page.clean(); page.add(build_dashboard_page()); page.update()

        def go_back(e):
            page.clean(); page.add(build_dashboard_page()); page.update()

        card_col = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                Row(alignment=MainAxisAlignment.START, controls=[
                    IconButton(
                        icon=Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        icon_color=ACCENT_GREEN, icon_size=20,
                        on_click=go_back,
                        style=ButtonStyle(padding=padding.all(4)),
                    ),
                ]),
                Icon(Icons.ADD_CIRCLE_OUTLINE_ROUNDED, color=ACCENT_GREEN, size=42),
                Container(height=4),
                Text("Adauga planta noua", size=26,
                     weight=FontWeight.W_800, color=PRIMARY_GREEN),
                Text("Scrie primele litere si selecteaza",
                     color=TEXT_LIGHT, size=13),
                Container(height=22),
                Container(
                    width=310,
                    content=Column(spacing=0, controls=[
                        search_field,
                        suggestions_wrap,
                    ]),
                ),
                Container(height=10),
                Container(content=status_msg, alignment=Alignment.CENTER,
                          width=310, height=24),
                Container(height=10),
                Container(
                    alignment=Alignment.CENTER, width=360,
                    content=ElevatedButton(
                        content=Row(
                            alignment=MainAxisAlignment.CENTER, spacing=8,
                            controls=[
                                Icon(Icons.PARK_ROUNDED, size=18, color="white"),
                                Text("Adauga in gradina", color="white",
                                     weight=FontWeight.W_700, size=16),
                            ],
                        ),
                        width=290, height=50, bgcolor=ACCENT_GREEN,
                        style=ButtonStyle(shape=RoundedRectangleBorder(radius=14)),
                        on_click=handle_add,
                    ),
                ),
            ],
        )

        body = Column(alignment=MainAxisAlignment.CENTER,
                      horizontal_alignment=CrossAxisAlignment.CENTER,
                      expand=True, controls=[gbox(card_col, h=510)])
        return page_shell(body)

    # =========================================================================
    # LISTA PLANTE
    # =========================================================================
    def build_plants_list_page():

        def go_back(e):
            page.clean(); page.add(build_dashboard_page()); page.update()

        def go_add(e):
            page.clean(); page.add(build_add_plant_page()); page.update()

        rows = []
        for p in user_plants:
            color = hum_color(p["humidity"])
            rows.append(Container(
                margin=margin.only(bottom=10),
                padding=padding.symmetric(horizontal=16, vertical=12),
                bgcolor=GLASS_CARD, border_radius=16,
                border=border.all(1.2, GLASS_BORDER), blur=10,
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Row(spacing=12, vertical_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(p["emoji"], size=30),
                                Column(spacing=2, controls=[
                                    Text(p["name"], size=15,
                                         weight=FontWeight.W_700, color=TEXT_DARK),
                                    Text(f"Umiditate: {p['humidity']}%  "
                                         f"| Prag: {p['hum_threshold']}%",
                                         size=11, color=TEXT_SUB),
                                ]),
                            ]),
                        Stack(alignment=Alignment.CENTER, controls=[
                            ProgressRing(width=46, height=46,
                                         value=p["humidity"] / 100,
                                         color=color, bgcolor="#22000000",
                                         stroke_width=5),
                            Text(f"{p['humidity']}%", size=10,
                                 weight=FontWeight.W_700, color=TEXT_DARK),
                        ]),
                    ],
                ),
            ))

        if not rows:
            rows.append(Container(padding=padding.all(20),
                                  content=Text("Nu ai plante adaugate inca.",
                                               color=TEXT_SUB, size=14,
                                               text_align=TextAlign.CENTER)))

        card_col = Column(
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0, scroll=ScrollMode.AUTO,
            controls=[
                Row(alignment=MainAxisAlignment.START, controls=[
                    IconButton(icon=Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                               icon_color=ACCENT_GREEN, icon_size=20,
                               on_click=go_back,
                               style=ButtonStyle(padding=padding.all(4))),
                ]),
                Icon(Icons.LOCAL_FLORIST_ROUNDED, color=ACCENT_GREEN, size=38),
                Container(height=4),
                Text("Plantele mele", size=26,
                     weight=FontWeight.W_800, color=PRIMARY_GREEN),
                Text(f"{len(user_plants)} plante active",
                     color=TEXT_LIGHT, size=13),
                Container(height=18),
                *rows,
                Container(height=10),
                ElevatedButton(
                    content=Row(alignment=MainAxisAlignment.CENTER, spacing=6,
                                controls=[
                                    Icon(Icons.ADD_ROUNDED, size=16, color="white"),
                                    Text("Adauga planta noua", color="white",
                                         size=13, weight=FontWeight.W_600),
                                ]),
                    bgcolor=ACCENT_GREEN,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=12),
                        padding=padding.symmetric(vertical=12, horizontal=20)),
                    on_click=go_add,
                ),
                Container(height=8),
            ],
        )

        body = Column(alignment=MainAxisAlignment.CENTER,
                      horizontal_alignment=CrossAxisAlignment.CENTER,
                      expand=True,
                      controls=[gbox(card_col, h=600,
                                     pad=padding.symmetric(horizontal=22, vertical=18))])
        return page_shell(body)

    # =========================================================================
    # DASHBOARD
    # =========================================================================
    def build_dashboard_page():

        scroll_ref = [None]

        def go_home(e):
            if scroll_ref[0]:
                scroll_ref[0].scroll_to(offset=0, duration=300)
                page.update()

        def go_add_plant(e):
            page.clean(); page.add(build_add_plant_page()); page.update()

        def go_plants(e):
            page.clean(); page.add(build_plants_list_page()); page.update()

        # ── Nav button ─────────────────────────────────────────────────────────
        def nav_btn(icon, label, active=False, on_click_fn=None):
            c  = ACCENT_GREEN if active else TEXT_SUB
            bg = GLASS_CHIP   if active else "transparent"
            col = Column(
                horizontal_alignment=CrossAxisAlignment.CENTER, spacing=4,
                controls=[
                    Container(
                        width=44, height=34, border_radius=10, bgcolor=bg,
                        border=border.all(1, GLASS_BORDER) if active
                               else border.all(0, "transparent"),
                        content=Icon(icon, size=20, color=c),
                        alignment=Alignment.CENTER,
                    ),
                    Text(label, size=10, color=c,
                         weight=FontWeight.W_600 if active else FontWeight.W_400),
                ],
            )
            if on_click_fn:
                return GestureDetector(on_tap=on_click_fn, content=col)
            return col

        bottom_bar = gbox(
            w=None, h=72, rad=0, bg=GLASS_BG,
            pad=padding.symmetric(horizontal=24, vertical=8),
            content=Row(
                alignment=MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    nav_btn(Icons.HOME_ROUNDED, "Acasa",
                            active=True, on_click_fn=go_home),
                    nav_btn(Icons.ADD_CIRCLE_OUTLINE_ROUNDED, "Adauga",
                            on_click_fn=go_add_plant),
                    nav_btn(Icons.LOCAL_FLORIST_ROUNDED, "Plantele",
                            on_click_fn=go_plants),
                ],
            ),
        )

        # ── Header ─────────────────────────────────────────────────────────────
        header = gbox(
            w=None, rad=18, bg=GLASS_BG,
            pad=padding.symmetric(horizontal=18, vertical=12),
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(spacing=6, tight=True, controls=[
                        Icon(Icons.WB_SUNNY_ROUNDED, color=AMBER_W, size=20),
                        Text(f"{SOLAR_TEMP}°C", size=17,
                             weight=FontWeight.W_800, color=TEXT_DARK),
                        Text("solar", size=13, color=TEXT_SUB),
                    ]),
                    Text("ROA", size=20, weight=FontWeight.W_800, color=ACCENT_GREEN),
                    Container(
                        width=38, height=38, border_radius=10,
                        bgcolor=GLASS_CHIP, border=border.all(1, GLASS_BORDER),
                        content=Icon(Icons.MENU_ROUNDED, color=TEXT_DARK, size=19),
                        alignment=Alignment.CENTER,
                    ),
                ],
            ),
        )

        # ── Greeting ───────────────────────────────────────────────────────────
        greeting = gbox(
            w=None, rad=18, bg=GLASS_BG,
            pad=padding.symmetric(horizontal=18, vertical=14),
            content=Column(spacing=2, controls=[
                Text("Buna ziua!", size=22, weight=FontWeight.W_800, color=TEXT_DARK),
                Text("Gradina ta este monitorizata in timp real.",
                     size=13, color=TEXT_SUB),
            ]),
        )

        # ── Humidity ring ──────────────────────────────────────────────────────
        humidity_section = gbox(
            w=None, rad=18, bg=GLASS_BG,
            pad=padding.symmetric(horizontal=18, vertical=18),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                spacing=26,
                controls=[
                    Stack(alignment=Alignment.CENTER, controls=[
                        ProgressRing(
                            width=108, height=108,
                            value=AVG_HUMIDITY / 100,
                            color=HUM_GREEN, bgcolor="#22000000", stroke_width=11,
                        ),
                        Column(
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=0,
                            controls=[
                                Text(f"{AVG_HUMIDITY}%", size=26,
                                     weight=FontWeight.W_800, color=TEXT_DARK),
                                Text("umid.", size=11, color=TEXT_SUB),
                            ],
                        ),
                    ]),
                    Column(spacing=10, controls=[
                        Row(spacing=7, controls=[
                            Container(width=8, height=8, border_radius=4,
                                      bgcolor=HUM_GREEN),
                            Text("Umiditate medie globala",
                                 size=13, color=TEXT_DARK, weight=FontWeight.W_600),
                        ]),
                        Row(spacing=7, controls=[
                            Icon(Icons.SENSORS_ROUNDED, size=14, color=ACCENT_MID),
                            Text(f"{len(user_plants)} senzori activi",
                                 size=12, color=TEXT_SUB),
                        ]),
                        Row(spacing=7, controls=[
                            Icon(Icons.WATER_DROP_OUTLINED, size=14, color="#2980b9"),
                            Text("2.4 L consumate astazi", size=12, color=TEXT_SUB),
                        ]),
                        Container(
                            padding=padding.symmetric(horizontal=10, vertical=4),
                            bgcolor="#2227ae60", border_radius=20,
                            border=border.all(1, "#4427ae60"),
                            content=Text("Live", size=11, color=ACCENT_GREEN,
                                         weight=FontWeight.W_700),
                        ),
                    ]),
                ],
            ),
        )

        # ── Plant card ─────────────────────────────────────────────────────────
        def plant_card(plant: dict) -> Container:
            hum   = plant["humidity"]
            color = hum_color(hum)
            return gbox(
                w=None, rad=18, bg=GLASS_CARD, pad=padding.all(14),
                content=Column(
                    spacing=0,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text(plant["emoji"], size=36),
                        Container(height=6),
                        Text(plant["name"], size=13, weight=FontWeight.W_700,
                             color=TEXT_DARK, text_align=TextAlign.CENTER,
                             max_lines=1, overflow=TextOverflow.ELLIPSIS),
                        Container(height=10),
                        Stack(alignment=Alignment.CENTER, controls=[
                            ProgressRing(
                                width=64, height=64,
                                value=hum / 100,
                                color=color, bgcolor="#22000000", stroke_width=6,
                            ),
                            Text(f"{hum}%", size=13, weight=FontWeight.W_800,
                                 color=TEXT_DARK),
                        ]),
                    ],
                ),
            )

        # ── Grid dinamic ───────────────────────────────────────────────────────
        def build_grid() -> Column:
            rows = []
            for i in range(0, len(user_plants), 2):
                pair = user_plants[i: i + 2]
                if len(pair) == 2:
                    rows.append(Row(spacing=12, controls=[
                        Container(expand=True, content=plant_card(pair[0])),
                        Container(expand=True, content=plant_card(pair[1])),
                    ]))
                else:
                    rows.append(Row(spacing=12, controls=[
                        Container(expand=True, content=plant_card(pair[0])),
                        Container(expand=True),
                    ]))
            return Column(spacing=12, controls=rows)

        # ── Advice ─────────────────────────────────────────────────────────────
        a_hum = user_plants[0]["humidity"] if user_plants else 60
        b_hum = user_plants[1]["humidity"] if len(user_plants) > 1 else 60
        advice_text = advice_engine(SOLAR_TEMP, AVG_HUMIDITY, a_hum, b_hum)

        advice_box = gbox(
            w=None, rad=18, bg=GLASS_BG, pad=padding.all(18),
            content=Column(spacing=10, controls=[
                Row(spacing=10, vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            width=32, height=32, border_radius=10,
                            bgcolor=GLASS_CHIP, border=border.all(1, GLASS_BORDER),
                            content=Icon(Icons.AUTO_AWESOME_ROUNDED,
                                         size=15, color=ACCENT_GREEN),
                            alignment=Alignment.CENTER,
                        ),
                        Column(spacing=1, controls=[
                            Text("Sfat zilnic AI", size=14,
                                 weight=FontWeight.W_700, color=TEXT_DARK),
                            Text("Analiza temperatura x umiditate",
                                 size=11, color=TEXT_SUB),
                        ]),
                    ]),
                Divider(height=1, color="#33000000"),
                Text(advice_text, size=12, color=TEXT_SUB),
            ]),
        )

        # ── Scroll column ──────────────────────────────────────────────────────
        scroll_col = Column(
            spacing=12, scroll=ScrollMode.AUTO,
            controls=[
                header, greeting, humidity_section,
                build_grid(), advice_box,
                Container(height=4),
            ],
        )
        scroll_ref[0] = scroll_col

        scroll_body = Container(
            expand=True,
            padding=padding.symmetric(horizontal=18, vertical=14),
            content=scroll_col,
        )

        body = Column(spacing=0, expand=True,
                      controls=[scroll_body, bottom_bar])
        return page_shell(body)

    # ── START ──────────────────────────────────────────────────────────────────
    page.add(build_login_page())


# =============================================================================
app(target=main, assets_dir="assets")