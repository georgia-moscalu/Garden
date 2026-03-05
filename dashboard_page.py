from flet import *
from colors import *
from helpers import hum_color
from ai_engine import advice_engine
from plants_db import SOLAR_TEMP, AVG_HUMIDITY


def build_dashboard_page(page, user_plants, build_add_plant_page, build_plants_list_page):

    # ── State ──────────────────────────────────────────────────────────────────
    is_expanded = [False]
    menu_open   = [False]

    COLLAPSED_HEIGHT = 570
    EXPANDED_HEIGHT  = 676

    def go_add_plant(e):
        page.clean(); page.add(build_add_plant_page()); page.update()

    def go_plants(e):
        page.clean(); page.add(build_plants_list_page()); page.update()

    # ── NAV BUTTON (bottom) ────────────────────────────────────────────────────
    def nav_btn(icon, label, active=False, on_click_fn=None):
        c = "white" if active else "#99ffffff"
        col = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER, spacing=2,
            controls=[
                Icon(icon, size=20, color=c),
                Text(label, size=9, color=c,
                     weight=FontWeight.W_600 if active else FontWeight.W_400),
            ],
        )
        if on_click_fn:
            return GestureDetector(on_tap=on_click_fn, content=col)
        return col

    # ── BOTTOM NAV ─────────────────────────────────────────────────────────────
    bottom_nav = Container(
        height=64,
        bgcolor="#cc1a1a2e",
        blur=20,
        border=border.only(top=BorderSide(1, "#15ffffff")),
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

    # ── HAMBURGER MENU PANEL ───────────────────────────────────────────────────
    def menu_item(icon, label, on_click_fn=None):
        row = Container(
            padding=padding.symmetric(horizontal=20, vertical=16),
            border=border.only(bottom=BorderSide(1, "#08000000")),
            ink=True,
            on_click=on_click_fn,
            content=Row(
                spacing=16,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=38, height=38, border_radius=12,
                        bgcolor="#f5f7f5",
                        alignment=Alignment.CENTER,
                        content=Icon(icon, size=18, color="#2d5a3d"),
                    ),
                    Text(label, size=14, weight=FontWeight.W_500,
                         color="#2c2c2c"),
                ],
            ),
        )
        return row

    menu_panel = Container(
        width=0,
        animate=Animation(300, AnimationCurve.EASE_IN_OUT),
        bgcolor="white",
        border_radius=BorderRadius(0, 28, 0, 28),
        shadow=BoxShadow(blur_radius=40, color="#33000000",
                         offset=Offset(4, 0)),
        clip_behavior=ClipBehavior.HARD_EDGE,
        content=Container(
            width=260,
            padding=padding.only(top=56, bottom=20),
            content=Column(
                spacing=0,
                controls=[
                    # ── Menu header ───────────────────────────────────────
                    Container(
                        padding=padding.only(left=24, right=24, bottom=24),
                        content=Column(
                            spacing=6,
                            controls=[
                                Container(
                                    width=48, height=48, border_radius=16,
                                    bgcolor="#e8f0e8",
                                    alignment=Alignment.CENTER,
                                    content=Icon(Icons.PERSON_ROUNDED,
                                                 size=24, color="#2d5a3d"),
                                ),
                                Text("Gradina mea", size=18,
                                     weight=FontWeight.W_700, color="#1a1a1a"),
                                Text("Bine ai revenit", size=12,
                                     color="#999999"),
                            ],
                        ),
                    ),
                    Divider(height=1, color="#f0f0f0"),
                    # ── Menu items ────────────────────────────────────────
                    menu_item(Icons.PERSON_OUTLINE_ROUNDED,   "Profil"),
                    menu_item(Icons.CALENDAR_MONTH_ROUNDED,   "Program udare"),
                    menu_item(Icons.MENU_BOOK_ROUNDED,        "Jurnal gradina"),
                    menu_item(Icons.NOTIFICATIONS_NONE_ROUNDED, "Notificari"),
                    menu_item(Icons.SETTINGS_OUTLINED,        "Setari"),
                    # ── Spacer + version ──────────────────────────────────
                    Container(expand=True),
                    Container(
                        padding=padding.symmetric(horizontal=24, vertical=8),
                        content=Text("ROA v1.0", size=10, color="#cccccc"),
                    ),
                ],
            ),
        ),
    )

    # ── Overlay (tap to close) ─────────────────────────────────────────────────
    menu_overlay = Container(
        visible=False,
        bgcolor="#44000000",
        expand=True,
        animate_opacity=Animation(200, AnimationCurve.EASE_IN_OUT),
        opacity=0,
        on_click=lambda e: toggle_menu(e),
    )

    def toggle_menu(e=None):
        menu_open[0] = not menu_open[0]
        if menu_open[0]:
            menu_overlay.visible = True
            menu_overlay.opacity = 1
            menu_panel.width = 260
        else:
            menu_overlay.opacity = 0
            menu_panel.width = 0
            menu_overlay.visible = False
        page.update()

    # ── TOP HERO ───────────────────────────────────────────────────────────────
    top_hero = Container(
        height=170,
        padding=padding.only(left=24, right=24, top=48, bottom=20),
        content=Column(
            spacing=0,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.START,
                    controls=[
                        # ── Hamburger button (3 liniute) ──────────────────
                        GestureDetector(
                            on_tap=lambda e: toggle_menu(e),
                            content=Container(
                                width=40, height=40,
                                border_radius=12,
                                bgcolor="#33ffffff",
                                alignment=Alignment.CENTER,
                                content=Icon(Icons.MENU_ROUNDED,
                                             size=20, color="white"),
                            ),
                        ),
                        # ── Temp badge ────────────────────────────────────
                        Container(
                            padding=padding.symmetric(horizontal=12, vertical=8),
                            bgcolor="#33ffffff",
                            border_radius=14,
                            border=border.all(1, "#22ffffff"),
                            content=Row(
                                spacing=5,
                                vertical_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Icon(Icons.WB_SUNNY_ROUNDED,
                                         color="#f5c842", size=16),
                                    Text(f"{SOLAR_TEMP}°C", size=15,
                                         weight=FontWeight.W_700,
                                         color="white"),
                                ],
                            ),
                        ),
                    ],
                ),
                Container(height=12),
                Text("Buna ziua !", size=28,
                     color="white", weight=FontWeight.W_800),
            ],
        ),
    )

    # ── PLANT ROW (minimal) ────────────────────────────────────────────────────
    def plant_row(plant: dict) -> Container:
        hum   = plant["humidity"]
        color = hum_color(hum)

        bar_width = 80

        return Container(
            padding=padding.symmetric(horizontal=20, vertical=16),
            border=border.only(bottom=BorderSide(1, "#06000000")),
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    # ── Left: emoji + name ────────────────────────────────
                    Row(
                        spacing=14,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=44, height=44,
                                border_radius=14,
                                bgcolor="#f5f7f5",
                                alignment=Alignment.CENTER,
                                content=Text(plant["emoji"], size=22),
                            ),
                            Text(plant["name"], size=15,
                                 weight=FontWeight.W_600, color="#2c2c2c"),
                        ],
                    ),
                    # ── Right: minimal bar + percent ──────────────────────
                    Row(
                        spacing=10,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=bar_width, height=5,
                                border_radius=3,
                                bgcolor="#eeeeee",
                                content=Container(
                                    width=bar_width * hum / 100,
                                    height=5,
                                    border_radius=3,
                                    bgcolor=color,
                                ),
                            ),
                            Text(f"{hum}%", size=12,
                                 weight=FontWeight.W_600, color="#555555"),
                        ],
                    ),
                ],
            ),
        )

    # ── AVG FOOTER ─────────────────────────────────────────────────────────────
    avg_hum   = AVG_HUMIDITY
    avg_color = hum_color(avg_hum)

    avg_footer = Container(
        bgcolor="#fafcfa",
        padding=padding.symmetric(horizontal=20, vertical=12),
        content=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(spacing=8, vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                    Icon(Icons.WATER_DROP_OUTLINED, size=14, color="#88aaaaaa"),
                    Text("Medie", size=12, color="#aaaaaa",
                         weight=FontWeight.W_500),
                ]),
                Row(spacing=8, vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                    Container(
                        width=70, height=5, border_radius=3, bgcolor="#eeeeee",
                        content=Container(
                            width=70 * avg_hum / 100, height=5,
                            border_radius=3, bgcolor=avg_color,
                        ),
                    ),
                    Text(f"{avg_hum}%", size=12,
                         weight=FontWeight.W_600, color="#555555"),
                ]),
            ],
        ),
    )

    # ── AI ADVICE (visible only when expanded) ─────────────────────────────────
    a_hum = user_plants[0]["humidity"] if user_plants else 60
    b_hum = user_plants[1]["humidity"] if len(user_plants) > 1 else 60
    advice_text = advice_engine(SOLAR_TEMP, AVG_HUMIDITY, a_hum, b_hum)

    ai_advice = Container(
        bgcolor="#f7faf7",
        padding=padding.symmetric(horizontal=20, vertical=14),
        content=Row(
            spacing=12,
            vertical_alignment=CrossAxisAlignment.START,
            controls=[
                Container(
                    width=30, height=30, border_radius=10,
                    bgcolor="#edf3ed",
                    content=Icon(Icons.AUTO_AWESOME_ROUNDED,
                                 size=14, color="#5a8a6a"),
                    alignment=Alignment.CENTER,
                ),
                Column(spacing=2, expand=True, controls=[
                    Text("Sfat AI", size=11,
                         weight=FontWeight.W_700, color="#3a3a3a"),
                    Text(advice_text, size=11, color="#888888"),
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
                         color="#aaaaaa", size=14,
                         text_align=TextAlign.CENTER),
        )]

    handle_icon = Icon(Icons.KEYBOARD_ARROW_UP_ROUNDED,
                       size=18, color="#bbbbbb")

    card = Container(
        height=COLLAPSED_HEIGHT,
        animate=Animation(350, AnimationCurve.EASE_IN_OUT),
        bgcolor="white",
        border_radius=BorderRadius(top_left=32, top_right=32,
                                   bottom_left=0, bottom_right=0),
        shadow=BoxShadow(blur_radius=30, color="#18000000",
                         offset=Offset(0, -4)),
        content=Column(
            spacing=0,
            expand=True,
            controls=[
                # ── Handle ────────────────────────────────────────────────
                GestureDetector(
                    on_tap=lambda e: toggle_card(e),
                    content=Container(
                        padding=padding.only(top=12, bottom=6),
                        alignment=Alignment.CENTER,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=4,
                            controls=[
                                Container(
                                    width=32, height=4,
                                    bgcolor="#e0e0e0",
                                    border_radius=4,
                                ),
                                handle_icon,
                            ],
                        ),
                    ),
                ),
                # ── Header ────────────────────────────────────────────────
                Container(
                    padding=padding.symmetric(horizontal=20, vertical=8),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text("Plantele mele", size=17,
                                 weight=FontWeight.W_800, color="#1a1a1a"),
                            GestureDetector(
                                on_tap=go_plants,
                                content=Container(
                                    padding=padding.symmetric(
                                        horizontal=12, vertical=6),
                                    bgcolor="#f5f7f5",
                                    border_radius=20,
                                    content=Text("Vezi toate", size=11,
                                                 color="#5a8a6a",
                                                 weight=FontWeight.W_600),
                                ),
                            ),
                        ],
                    ),
                ),
                # ── Plant list ────────────────────────────────────────────
                Container(
                    expand=True,
                    content=ListView(expand=True, controls=plant_rows),
                ),
                Divider(height=1, color="#f0f0f0"),
                avg_footer,
                ai_advice,
            ],
        ),
    )

    # ── TOGGLE CARD ────────────────────────────────────────────────────────────
    def toggle_card(e=None):
        is_expanded[0] = not is_expanded[0]
        if is_expanded[0]:
            card.height = EXPANDED_HEIGHT
            handle_icon.name = Icons.KEYBOARD_ARROW_DOWN_ROUNDED
        else:
            card.height = COLLAPSED_HEIGHT
            handle_icon.name = Icons.KEYBOARD_ARROW_UP_ROUNDED
        page.update()

    # ── MAIN LAYOUT (no gradient overlay) ──────────────────────────────────────
    main_content = Column(
        spacing=0,
        expand=True,
        controls=[top_hero, card],
    )

    # ── Stack: content + overlay + menu panel ──────────────────────────────────
    main_stack = Stack(
        expand=True,
        controls=[
            main_content,
            menu_overlay,
            menu_panel,
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