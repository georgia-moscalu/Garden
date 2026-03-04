from flet import *
from colors import *
from helpers import hum_color
from ai_engine import advice_engine
from plants_db import SOLAR_TEMP, AVG_HUMIDITY


def build_dashboard_page(page, user_plants, build_add_plant_page, build_plants_list_page):

    # ── State ──────────────────────────────────────────────────────────────────
    is_expanded = [False]

    COLLAPSED_HEIGHT = 520   # inaltimea normala a cardului
    EXPANDED_HEIGHT  = 676   # cat ocupa tot ecranul (740 - 64 nav)

    def go_add_plant(e):
        page.clean(); page.add(build_add_plant_page()); page.update()

    def go_plants(e):
        page.clean(); page.add(build_plants_list_page()); page.update()

    # ── Nav button ─────────────────────────────────────────────────────────────
    def nav_btn(icon, label, active=False, on_click_fn=None):
        c  = "white"     if active else "#dddddd"
        bg = "#44ffffff" if active else "transparent"
        col = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER, spacing=3,
            controls=[
                Container(
                    width=40, height=30, border_radius=10, bgcolor=bg,
                    content=Icon(icon, size=18, color=c),
                    alignment=Alignment.CENTER,
                ),
                Text(label, size=9, color=c,
                     weight=FontWeight.W_600 if active else FontWeight.W_400),
            ],
        )
        if on_click_fn:
            return GestureDetector(on_tap=on_click_fn, content=col)
        return col

    # ── Bottom nav ─────────────────────────────────────────────────────────────
    bottom_nav = Container(
        height=64,
        bgcolor="#88f5faf5",
        blur=18,
        border=border.only(top=BorderSide(1, "#33ffffff")),
        padding=padding.symmetric(horizontal=32, vertical=8),
        content=Row(
            alignment=MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                nav_btn(Icons.HOME_ROUNDED,               "Acasa",  active=True),
                nav_btn(Icons.ADD_CIRCLE_OUTLINE_ROUNDED, "Adauga", on_click_fn=go_add_plant),
                nav_btn(Icons.LOCAL_FLORIST_ROUNDED,      "Plante", on_click_fn=go_plants),
            ],
        ),
    )

    # ── TOP HERO ───────────────────────────────────────────────────────────────
    top_hero = Container(
        height=220,
        padding=padding.only(left=24, right=24, top=48, bottom=20),
        content=Column(
            spacing=0,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.START,
                    controls=[
                        Column(spacing=4, controls=[
                            Text("Gradina mea", size=13,
                                 color="#ccffffff", weight=FontWeight.W_500),
                            Text("Dashboard", size=28,
                                 color="white", weight=FontWeight.W_800),
                        ]),
                        Container(
                            padding=padding.symmetric(horizontal=12, vertical=8),
                            bgcolor="#44ffffff",
                            border_radius=14,
                            border=border.all(1, "#55ffffff"),
                            content=Row(
                                spacing=5,
                                vertical_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Icon(Icons.WB_SUNNY_ROUNDED, color=AMBER_W, size=16),
                                    Text(f"{SOLAR_TEMP}°C", size=15,
                                         weight=FontWeight.W_700, color="white"),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    # ── PLANT ROW ──────────────────────────────────────────────────────────────
    def plant_row(plant: dict) -> Container:
        hum   = plant["humidity"]
        color = hum_color(hum)
        needs = hum < plant["hum_threshold"]
        return Container(
            padding=padding.symmetric(horizontal=20, vertical=14),
            border=border.only(bottom=BorderSide(1, "#11000000")),
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(
                        spacing=14,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=46, height=46,
                                border_radius=14,
                                bgcolor="#f0f7f0",
                                alignment=Alignment.CENTER,
                                content=Text(plant["emoji"], size=24),
                            ),
                            Column(spacing=3, controls=[
                                Text(plant["name"], size=15,
                                     weight=FontWeight.W_700, color=TEXT_DARK),
                                Text("umiditate sol", size=12, color=TEXT_SUB),
                            ]),
                        ],
                    ),
                    Row(
                        spacing=10,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                visible=needs,
                                padding=padding.symmetric(horizontal=7, vertical=3),
                                bgcolor="#fff3f3",
                                border_radius=20,
                                border=border.all(1, "#ffcccc"),
                                content=Text("⚠", size=10, color="#cc0000"),
                            ),
                            Stack(alignment=Alignment.CENTER, controls=[
                                ProgressRing(
                                    width=44, height=44,
                                    value=hum / 100,
                                    color=color,
                                    bgcolor="#18000000",
                                    stroke_width=4,
                                ),
                                Text(f"{hum}%", size=10,
                                     weight=FontWeight.W_700, color=TEXT_DARK),
                            ]),
                        ],
                    ),
                ],
            ),
        )

    # ── AVG FOOTER ─────────────────────────────────────────────────────────────
    avg_hum   = AVG_HUMIDITY
    avg_color = hum_color(avg_hum)

    avg_footer = Container(
        bgcolor="#f5faf5",
        padding=padding.symmetric(horizontal=20, vertical=10),
        content=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(spacing=8, vertical_alignment=CrossAxisAlignment.CENTER, controls=[
                    Icon(Icons.WATER_DROP_OUTLINED, size=14, color=ACCENT_GREEN),
                    Column(spacing=0, controls=[
                        Text("Medie globală", size=11,
                             color=TEXT_SUB, weight=FontWeight.W_500),
                        Text(f"{len(user_plants)} plante",
                             size=10, color="#bbbbbb"),
                    ]),
                ]),
                Row(spacing=8, vertical_alignment=CrossAxisAlignment.CENTER, controls=[
                    Container(
                        width=90, height=6,
                        border_radius=4,
                        bgcolor="#e8e8e8",
                        content=Container(
                            width=90 * avg_hum / 100,
                            height=6,
                            border_radius=4,
                            bgcolor=avg_color,
                        ),
                    ),
                    Text(f"{avg_hum}%", size=12,
                         weight=FontWeight.W_700, color=TEXT_DARK),
                ]),
            ],
        ),
    )

    # ── AI ADVICE (vizibil doar expanded) ──────────────────────────────────────
    a_hum = user_plants[0]["humidity"] if user_plants else 60
    b_hum = user_plants[1]["humidity"] if len(user_plants) > 1 else 60
    advice_text = advice_engine(SOLAR_TEMP, AVG_HUMIDITY, a_hum, b_hum)

    ai_advice = Container(
        bgcolor="#f0f7f0",
        border_radius=BorderRadius(0, 0, 0, 0),
        padding=padding.symmetric(horizontal=20, vertical=14),
        content=Row(
            spacing=12,
            vertical_alignment=CrossAxisAlignment.START,
            controls=[
                Container(
                    width=32, height=32, border_radius=10,
                    bgcolor="#e0f0e0",
                    content=Icon(Icons.AUTO_AWESOME_ROUNDED, size=15, color=ACCENT_GREEN),
                    alignment=Alignment.CENTER,
                ),
                Column(spacing=3, expand=True, controls=[
                    Text("Sfat AI", size=12,
                         weight=FontWeight.W_700, color=TEXT_DARK),
                    Text(advice_text, size=11, color=TEXT_SUB),
                ]),
            ],
        ),
    )

    # ── CARD CONTENT ───────────────────────────────────────────────────────────
    plant_rows = [plant_row(p) for p in user_plants]
    if not plant_rows:
        plant_rows = [Container(
            padding=padding.all(24),
            content=Text("Nu ai plante adaugate inca.",
                         color=TEXT_SUB, size=14,
                         text_align=TextAlign.CENTER),
        )]

    # Handle indicator (arrow schimba directia)
    handle_icon = Icon(Icons.KEYBOARD_ARROW_UP_ROUNDED,
                       size=20, color="#aaaaaa")

    # Card container animat
    card = Container(
        height=COLLAPSED_HEIGHT,
        animate=Animation(350, AnimationCurve.EASE_IN_OUT),
        bgcolor="white",
        border_radius=BorderRadius(top_left=32, top_right=32,
                                   bottom_left=0, bottom_right=0),
        shadow=BoxShadow(blur_radius=30, color="#22000000",
                         offset=Offset(0, -4)),
        content=Column(
            spacing=0,
            expand=True,
            controls=[
                # ── Handle tap ────────────────────────────────────────────────
                GestureDetector(
                    on_tap=lambda e: toggle_card(e),
                    content=Container(
                        padding=padding.only(top=12, bottom=8),
                        alignment=Alignment.CENTER,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=4,
                            controls=[
                                Container(
                                    width=36, height=4,
                                    bgcolor="#dddddd",
                                    border_radius=4,
                                ),
                                handle_icon,
                            ],
                        ),
                    ),
                ),
                # ── Header ────────────────────────────────────────────────────
                Container(
                    padding=padding.symmetric(horizontal=20, vertical=8),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text("Plantele mele", size=17,
                                 weight=FontWeight.W_800, color=TEXT_DARK),
                            GestureDetector(
                                on_tap=go_plants,
                                content=Container(
                                    padding=padding.symmetric(horizontal=12, vertical=6),
                                    bgcolor="#f0f7f0",
                                    border_radius=20,
                                    content=Text("Vezi toate", size=11,
                                                 color=ACCENT_GREEN,
                                                 weight=FontWeight.W_600),
                                ),
                            ),
                        ],
                    ),
                ),
                # ── Lista ─────────────────────────────────────────────────────
                Container(
                    expand=True,
                    content=ListView(expand=True, controls=plant_rows),
                ),
                Divider(height=1, color="#eeeeee"),
                avg_footer,
                # AI advice - vizibil doar cand e expandat
                ai_advice,
            ],
        ),
    )

    # ── TOGGLE LOGIC ───────────────────────────────────────────────────────────
    def toggle_card(e=None):
        is_expanded[0] = not is_expanded[0]
        if is_expanded[0]:
            card.height = EXPANDED_HEIGHT
            handle_icon.name = Icons.KEYBOARD_ARROW_DOWN_ROUNDED
        else:
            card.height = COLLAPSED_HEIGHT
            handle_icon.name = Icons.KEYBOARD_ARROW_UP_ROUNDED
        page.update()

    # ── GRADIENT OVERLAY ───────────────────────────────────────────────────────
    gradient_overlay = Container(
        expand=True,
        gradient=LinearGradient(
            begin=Alignment(0, -1),
            end=Alignment(0, 1),
            colors=["#aa00573F", "#4400573F", "#0000573F"],
            stops=[0.0, 0.35, 0.65],
        ),
    )

    main_stack = Stack(
        expand=True,
        controls=[
            gradient_overlay,
            Column(
                spacing=0,
                expand=True,
                controls=[top_hero, card],
            ),
        ],
    )

    body = Column(
        spacing=0,
        expand=True,
        controls=[
            Container(expand=True, content=main_stack),
            bottom_nav,
        ],
    )

    return body