from flet import *
from colors import *
from helpers import hum_color
from ai_engine import advice_engine
from pico_service import get_sensor_data
import threading
import time
import asyncio   # ← adaugă asta


def build_dashboard_page(page, user_plants, build_add_plant_page, build_plants_list_page):

    # ── State ──────────────────────────────────────────────────────────────────
    is_expanded = [False]
    menu_open   = [False]

    COLLAPSED_HEIGHT = 570
    EXPANDED_HEIGHT  = 700

    # ── Date live de la Pico ───────────────────────────────────────────────────
    sensor      = [get_sensor_data()]   # dict: umiditate, status, alarma, temp
    live_hum    = lambda: sensor[0].get("umiditate", 0)
    live_temp   = lambda: sensor[0].get("temp", 0)
    live_alarma = lambda: sensor[0].get("alarma", False)
    live_status = lambda: sensor[0].get("status", "offline")

    # ── Nav helpers ────────────────────────────────────────────────────────────
    def go_add_plant(e):
        page.clean(); page.add(build_add_plant_page()); page.update()

    def go_plants(e):
        page.clean(); page.add(build_plants_list_page()); page.update()

    # ── NAV BUTTON ─────────────────────────────────────────────────────────────
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
        return Container(
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
                    Text(label, size=14, weight=FontWeight.W_500, color="#2c2c2c"),
                ],
            ),
        )

    menu_panel = Container(
        width=0,
        animate=Animation(300, AnimationCurve.EASE_IN_OUT),
        bgcolor="white",
        border_radius=BorderRadius(0, 28, 0, 28),
        shadow=BoxShadow(blur_radius=40, color="#33000000", offset=Offset(4, 0)),
        clip_behavior=ClipBehavior.HARD_EDGE,
        content=Container(
            width=260,
            padding=padding.only(top=56, bottom=20),
            content=Column(
                spacing=0,
                controls=[
                    Container(
                        padding=padding.only(left=24, right=24, bottom=24),
                        content=Column(
                            spacing=6,
                            controls=[
                                Container(
                                    width=48, height=48, border_radius=16,
                                    bgcolor="#e8f0e8",
                                    alignment=Alignment.CENTER,
                                    content=Icon(Icons.PERSON_ROUNDED, size=24, color="#2d5a3d"),
                                ),
                                Text("Gradina mea", size=18,
                                     weight=FontWeight.W_700, color="#1a1a1a"),
                                Text("Bine ai revenit", size=12, color="#999999"),
                            ],
                        ),
                    ),
                    Divider(height=1, color="#f0f0f0"),
                    menu_item(Icons.PERSON_OUTLINE_ROUNDED,     "Profil"),
                    menu_item(Icons.CALENDAR_MONTH_ROUNDED,     "Program udare"),
                    menu_item(Icons.MENU_BOOK_ROUNDED,          "Jurnal gradina"),
                    menu_item(Icons.NOTIFICATIONS_NONE_ROUNDED, "Notificari"),
                    menu_item(Icons.SETTINGS_OUTLINED,          "Setari"),
                    Container(expand=True),
                    Container(
                        padding=padding.symmetric(horizontal=24, vertical=8),
                        content=Text("ROA v1.0", size=10, color="#cccccc"),
                    ),
                ],
            ),
        ),
    )

    # ── Overlay ────────────────────────────────────────────────────────────────
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
            menu_panel.width     = 260
        else:
            menu_overlay.opacity = 0
            menu_panel.width     = 0
            menu_overlay.visible = False
        page.update()

    # ── TOP HERO — temperatură live ────────────────────────────────────────────
    temp_text = Text(
        f"{live_temp()}°C" if live_temp() else "--°C",
        size=15, weight=FontWeight.W_700, color="white",
    )

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
                        GestureDetector(
                            on_tap=lambda e: toggle_menu(e),
                            content=Container(
                                width=40, height=40,
                                border_radius=12,
                                bgcolor="#33ffffff",
                                alignment=Alignment.CENTER,
                                content=Icon(Icons.MENU_ROUNDED, size=20, color="white"),
                            ),
                        ),
                        Container(
                            padding=padding.symmetric(horizontal=12, vertical=8),
                            bgcolor="#33ffffff",
                            border_radius=14,
                            border=border.all(1, "#22ffffff"),
                            content=Row(
                                spacing=5,
                                vertical_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Icon(Icons.WB_SUNNY_ROUNDED, color="#f5c842", size=16),
                                    temp_text,
                                ],
                            ),
                        ),
                    ],
                ),
                Container(height=12),
                Text("Buna ziua !", size=28, color="white", weight=FontWeight.W_800),
            ],
        ),
    )

    # ── PLANT ROW ──────────────────────────────────────────────────────────────
    def plant_row(plant: dict) -> Container:
        hum   = plant["humidity"]
        color = hum_color(hum)

        ring = Stack(
            width=54, height=54,
            controls=[
                ProgressRing(
                    value=hum / 100,
                    width=54, height=54,
                    stroke_width=5,
                    color=color,
                    bgcolor="#e8e8e8",
                ),
                Container(
                    width=54, height=54,
                    alignment=Alignment.CENTER,
                    content=Text(f"{hum}%", size=10,
                                 weight=FontWeight.W_700, color="#333333"),
                ),
            ],
        )

        return Container(
            margin=margin.only(left=16, right=16, top=0, bottom=8),
            padding=padding.symmetric(horizontal=16, vertical=14),
            bgcolor="white",
            border_radius=20,
            shadow=BoxShadow(blur_radius=16, spread_radius=0,
                             color="#0a000000", offset=Offset(0, 3)),
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(
                        spacing=14,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=46, height=46, border_radius=14,
                                bgcolor="#f0f5f0",
                                alignment=Alignment.CENTER,
                                content=Text(plant["emoji"], size=24),
                            ),
                            Column(spacing=2, controls=[
                                Text(plant["name"], size=15,
                                     weight=FontWeight.W_700, color="#1a1a1a"),
                                Text(f"Umiditate: {hum}%", size=11, color="#aaaaaa"),
                            ]),
                        ],
                    ),
                    ring,
                ],
            ),
        )

    # ── PICO SENSOR CARD — date live ───────────────────────────────────────────
    def _sensor_color(v):
        if v < 30: return "#ff4444"
        if v < 60: return "#ffaa00"
        return "#2d5a3d"

    def _sensor_label(s):
        if s == "offline":  return "⚫ Senzor offline"
        if s == "uscat":    return "🔴 Prea uscat — pornește apa!"
        if s == "moderat":  return "🟡 Umiditate moderată"
        return "🟢 Umiditate OK"

    sensor_value_text = Text(
        f"{live_hum()}%",
        size=36, weight=FontWeight.W_800,
        color=_sensor_color(live_hum()),
    )
    sensor_status_text = Text(
        _sensor_label(live_status()),
        size=12,
        color=_sensor_color(live_hum()),
    )
    sensor_bar = ProgressBar(
        value=max(live_hum(), 1) / 100,
        color=_sensor_color(live_hum()),
        bgcolor="#e0e0e0",
        height=8,
        border_radius=4,
    )
    sensor_dot = Container(
        width=8, height=8, border_radius=4,
        bgcolor="#00cc66" if live_status() != "offline" else "#888888",
    )

    def refresh_sensor(e=None):
        sensor[0] = get_sensor_data()
        v = live_hum()
        s = live_status()
        c = _sensor_color(v)

        sensor_value_text.value  = f"{v}%"
        sensor_value_text.color  = c
        sensor_status_text.value = _sensor_label(s)
        sensor_status_text.color = c
        sensor_bar.value         = max(v, 1) / 100
        sensor_bar.color         = c
        sensor_dot.bgcolor       = "#00cc66" if s != "offline" else "#888888"
        temp_text.value          = f"{live_temp()}°C" if live_temp() else "--°C"

        # Actualizează și avg footer
        avg_val_text.value       = f"{v}%"
        avg_bar_fill.width       = 70 * v / 100
        avg_bar_fill.bgcolor     = hum_color(v)
        avg_val_text.color       = "#555555"

        page.update()

    pico_card = Container(
        margin=margin.only(left=16, right=16, top=0, bottom=8),
        padding=padding.symmetric(horizontal=16, vertical=14),
        bgcolor="white",
        border_radius=20,
        shadow=BoxShadow(blur_radius=16, color="#0a000000", offset=Offset(0, 3)),
        content=Column(
            spacing=10,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Row(spacing=8, vertical_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                sensor_dot,
                                Icon(Icons.SENSORS_ROUNDED, size=16, color="#2d5a3d"),
                                Text("Senzor Sol — Live", size=13,
                                     weight=FontWeight.W_700, color="#1a1a1a"),
                            ]),
                        IconButton(
                            icon=Icons.REFRESH_ROUNDED,
                            icon_size=18,
                            icon_color="#2d5a3d",
                            on_click=refresh_sensor,
                            tooltip="Actualizează",
                        ),
                    ],
                ),
                sensor_value_text,
                sensor_bar,
                sensor_status_text,
            ],
        ),
    )

    # ── AVG FOOTER — umiditate live din senzor ─────────────────────────────────
    avg_hum   = live_hum()
    avg_color = hum_color(avg_hum)

    avg_bar_fill = Container(
        width=70 * avg_hum / 100, height=5,
        border_radius=3, bgcolor=avg_color,
    )
    avg_val_text = Text(
        f"{avg_hum}%", size=12,
        weight=FontWeight.W_600, color="#555555",
    )

    avg_footer = Container(
        margin=margin.only(left=16, right=16, top=4, bottom=8),
        padding=padding.symmetric(horizontal=16, vertical=12),
        bgcolor="#f7faf7",
        border_radius=16,
        content=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(spacing=8, vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Icon(Icons.WATER_DROP_OUTLINED, size=14, color="#88aaaaaa"),
                        Text("Umiditate sol acum", size=12, color="#aaaaaa",
                             weight=FontWeight.W_500),
                    ]),
                Row(spacing=8, vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            width=70, height=5,
                            border_radius=3, bgcolor="#eeeeee",
                            content=avg_bar_fill,
                        ),
                        avg_val_text,
                    ]),
            ],
        ),
    )

    # ── AI ADVICE — folosește date live ───────────────────────────────────────
    a_hum = user_plants[0]["humidity"] if user_plants else live_hum()
    b_hum = user_plants[1]["humidity"] if len(user_plants) > 1 else live_hum()
    advice_text = advice_engine(live_temp() or 20, live_hum() or 50, a_hum, b_hum)

    ai_advice = Container(
        margin=margin.only(left=16, right=16, top=0, bottom=8),
        padding=padding.symmetric(horizontal=16, vertical=14),
        bgcolor="#eef5f0",
        border_radius=16,
        border=border.all(1, "#c8dfd0"),
        content=Row(
            spacing=12,
            vertical_alignment=CrossAxisAlignment.START,
            controls=[
                Container(
                    width=32, height=32, border_radius=10,
                    bgcolor="#2d5a3d",
                    alignment=Alignment.CENTER,
                    content=Icon(Icons.AUTO_AWESOME_ROUNDED, size=14, color="white"),
                ),
                Column(spacing=3, expand=True, controls=[
                    Text("Sfat AI", size=11, weight=FontWeight.W_700, color="#2d5a3d"),
                    Text(advice_text, size=11, color="#555555"),
                ]),
            ],
        ),
    )

    # ── CARD ───────────────────────────────────────────────────────────────────
    plant_rows = [plant_row(p) for p in user_plants]
    if not plant_rows:
        plant_rows = [Container(
            padding=padding.all(24),
            content=Text("Nu ai plante adaugate inca.",
                         color="#aaaaaa", size=14,
                         text_align=TextAlign.CENTER),
        )]

    handle_icon = Icon(Icons.KEYBOARD_ARROW_UP_ROUNDED, size=18, color="#bbbbbb")

    card = Container(
        height=COLLAPSED_HEIGHT,
        animate=Animation(350, AnimationCurve.EASE_IN_OUT),
        bgcolor="#f3f5f2",
        border_radius=BorderRadius(top_left=32, top_right=32,
                                   bottom_left=0, bottom_right=0),
        shadow=BoxShadow(blur_radius=30, color="#18000000", offset=Offset(0, -4)),
        content=Column(
            spacing=0,
            expand=True,
            controls=[
                # Handle
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
                                    bgcolor="#dedede", border_radius=4,
                                ),
                                handle_icon,
                            ],
                        ),
                    ),
                ),
                # Header
                Container(
                    padding=padding.only(left=20, right=20, top=4, bottom=12),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Row(
                                spacing=10,
                                vertical_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Container(
                                        width=38, height=38, border_radius=13,
                                        bgcolor="#2d5a3d",
                                        alignment=Alignment.CENTER,
                                        content=Icon(Icons.LOCAL_FLORIST_ROUNDED,
                                                     size=18, color="white"),
                                    ),
                                    Column(spacing=1, controls=[
                                        Text("Plantele mele", size=17,
                                             weight=FontWeight.W_800, color="#1a1a1a"),
                                        Text(f"{len(user_plants)} plante active",
                                             size=11, color="#999999"),
                                    ]),
                                ],
                            ),
                            GestureDetector(
                                on_tap=go_plants,
                                content=Container(
                                    padding=padding.symmetric(horizontal=14, vertical=8),
                                    bgcolor="#2d5a3d",
                                    border_radius=20,
                                    content=Text("Vezi toate", size=11,
                                                 color="white",
                                                 weight=FontWeight.W_600),
                                ),
                            ),
                        ],
                    ),
                ),
                # Plant list
                Container(
                    expand=True,
                    content=ListView(
                        expand=True,
                        controls=plant_rows,
                        padding=padding.only(top=4),
                    ),
                ),
                pico_card,
                avg_footer,
                ai_advice,
                Container(height=8),
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

    # ── MAIN LAYOUT ────────────────────────────────────────────────────────────
    main_content = Column(
        spacing=0, expand=True,
        controls=[top_hero, card],
    )

    main_stack = Stack(
        expand=True,
        controls=[main_content, menu_overlay, menu_panel],
    )

    # Auto-refresh la fiecare 5 secunde
    async def auto_refresh():
        while True:
            await asyncio.sleep(5)
            try:
                refresh_sensor(None)
                print("Refreshed OK!")
            except Exception as e:
                print("EROARE auto-refresh:", e)

    page.run_task(auto_refresh)


    body = Column(
        spacing=0, expand=True,
        controls=[
            Container(expand=True, content=main_stack),
            bottom_nav,
        ],
    )

    return body