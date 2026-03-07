from flet import *
from colors import *
from helpers import hum_color
from ai_engine import advice_engine
from pico_service import get_sensor_data
import asyncio


def build_dashboard_page(page, user_plants, build_add_plant_page, build_plants_list_page):

    # ── Dimensiuni responsive ──────────────────────────────────────────────────
    H             = page.height or 740
    W             = page.width  or 500
    HERO_H        = int(H * 0.20)
    NAV_H         = int(H * 0.09)
    CARD_H        = H - HERO_H - NAV_H
    CARD_H_EXP    = CARD_H + int(H * 0.10)

    # ── State ──────────────────────────────────────────────────────────────────
    is_expanded = [False]
    menu_open   = [False]

    # ── Date live de la Pico ───────────────────────────────────────────────────
    sensor      = [get_sensor_data()]
    live_hum    = lambda: sensor[0].get("umiditate", 0)
    live_temp   = lambda: sensor[0].get("temp", 0)
    live_status = lambda: sensor[0].get("status", "offline")

    def go_add_plant(e):
        page.clean(); page.add(build_add_plant_page()); page.update()

    def go_plants(e):
        page.clean(); page.add(build_plants_list_page()); page.update()

    def nav_btn(icon, label, active=False, on_click_fn=None):
        c = "white" if active else "#bbffffff"
        col = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=3,
            controls=[
                Icon(icon, size=22, color=c),
                Text(label, size=11, color=c,
                     weight=FontWeight.W_600 if active else FontWeight.W_400),
            ],
        )
        if on_click_fn:
            return GestureDetector(on_tap=on_click_fn, content=col)
        return col

    bottom_nav = Container(
        height=NAV_H,
        bgcolor="#ee1a1a2e",
        border=border.only(top=BorderSide(1, "#33ffffff")),
        padding=padding.symmetric(horizontal=24, vertical=6),
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

    def menu_item(icon, label, on_click_fn=None):
        return Container(
            padding=padding.symmetric(horizontal=20, vertical=14),
            border=border.only(bottom=BorderSide(1, "#08000000")),
            ink=True, on_click=on_click_fn,
            content=Row(spacing=16, vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(width=36, height=36, border_radius=12,
                              bgcolor="#f5f7f5", alignment=Alignment.CENTER,
                              content=Icon(icon, size=17, color="#2d5a3d")),
                    Text(label, size=13, weight=FontWeight.W_500, color="#2c2c2c"),
                ]),
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
            padding=padding.only(top=52, bottom=16),
            content=Column(spacing=0, controls=[
                Container(
                    padding=padding.only(left=24, right=24, bottom=20),
                    content=Column(spacing=6, controls=[
                        Container(width=46, height=46, border_radius=14,
                                  bgcolor="#e8f0e8", alignment=Alignment.CENTER,
                                  content=Icon(Icons.PERSON_ROUNDED, size=22, color="#2d5a3d")),
                        Text("Gradina mea", size=17, weight=FontWeight.W_700, color="#1a1a1a"),
                        Text("Bine ai revenit", size=11, color="#999999"),
                    ]),
                ),
                Divider(height=1, color="#f0f0f0"),
                menu_item(Icons.PERSON_OUTLINE_ROUNDED,     "Profil"),
                menu_item(Icons.CALENDAR_MONTH_ROUNDED,     "Program udare"),
                menu_item(Icons.MENU_BOOK_ROUNDED,          "Jurnal gradina"),
                menu_item(Icons.NOTIFICATIONS_NONE_ROUNDED, "Notificari"),
                menu_item(Icons.SETTINGS_OUTLINED,          "Setari"),
                Container(expand=True),
                Container(padding=padding.symmetric(horizontal=24, vertical=8),
                          content=Text("ROA v1.0", size=10, color="#cccccc")),
            ]),
        ),
    )

    menu_overlay = Container(
        visible=False, bgcolor="#44000000", expand=True,
        animate_opacity=Animation(200, AnimationCurve.EASE_IN_OUT),
        opacity=0, on_click=lambda e: toggle_menu(e),
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

    temp_text = Text(
        f"{live_temp()}°C" if live_temp() else "--°C",
        size=14, weight=FontWeight.W_700, color="white",
    )

    top_hero = Container(
        height=HERO_H,
        padding=padding.only(left=22, right=22, top=int(HERO_H * 0.30), bottom=12),
        content=Column(spacing=0, controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    GestureDetector(
                        on_tap=lambda e: toggle_menu(e),
                        content=Container(width=38, height=38, border_radius=12,
                                          bgcolor="#33ffffff", alignment=Alignment.CENTER,
                                          content=Icon(Icons.MENU_ROUNDED, size=19, color="white")),
                    ),
                    Container(
                        padding=padding.symmetric(horizontal=10, vertical=7),
                        bgcolor="#33ffffff", border_radius=12,
                        border=border.all(1, "#22ffffff"),
                        content=Row(spacing=5, vertical_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Icon(Icons.WB_SUNNY_ROUNDED, color="#f5c842", size=14),
                                temp_text,
                            ]),
                    ),
                ],
            ),
            Container(height=10),
            Text("Buna ziua !", size=26, color="white", weight=FontWeight.W_800),
        ]),
    )

    def plant_row(plant: dict) -> Container:
        hum   = plant["humidity"]
        color = hum_color(hum)
        ring  = Stack(width=50, height=50, controls=[
            ProgressRing(value=hum / 100, width=50, height=50,
                         stroke_width=5, color=color, bgcolor="#e8e8e8"),
            Container(width=50, height=50, alignment=Alignment.CENTER,
                      content=Text(f"{hum}%", size=9,
                                   weight=FontWeight.W_700, color="#333333")),
        ])
        return Container(
            margin=margin.only(left=14, right=14, bottom=7),
            padding=padding.symmetric(horizontal=14, vertical=12),
            bgcolor="white", border_radius=18,
            shadow=BoxShadow(blur_radius=12, color="#0a000000", offset=Offset(0, 2)),
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(spacing=12, vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(width=42, height=42, border_radius=12,
                                      bgcolor="#f0f5f0", alignment=Alignment.CENTER,
                                      content=Text(plant["emoji"], size=22)),
                            Column(spacing=2, controls=[
                                Text(plant["name"], size=14,
                                     weight=FontWeight.W_700, color="#1a1a1a"),
                                Text(f"Umiditate: {hum}%", size=10, color="#aaaaaa"),
                            ]),
                        ]),
                    ring,
                ],
            ),
        )

    def _sc(v):
        if v < 30: return "#ff4444"
        if v < 60: return "#ffaa00"
        return "#2d5a3d"

    def _sl(s):
        if s == "offline": return "⚫ Senzor offline"
        if s == "uscat":   return "🔴 Prea uscat — pornește apa!"
        if s == "moderat": return "🟡 Umiditate moderată"
        return "🟢 Umiditate OK"

    sensor_value_text  = Text(f"{live_hum()}%", size=32,
                               weight=FontWeight.W_800, color=_sc(live_hum()))
    sensor_status_text = Text(_sl(live_status()), size=11, color=_sc(live_hum()))
    sensor_bar         = ProgressBar(value=max(live_hum(), 1) / 100,
                                     color=_sc(live_hum()), bgcolor="#e0e0e0",
                                     height=7, border_radius=4)
    sensor_dot         = Container(width=7, height=7, border_radius=4,
                                   bgcolor="#00cc66" if live_status() != "offline" else "#888888")

    avg_bar_fill = Container(width=70 * live_hum() / 100, height=5,
                             border_radius=3, bgcolor=hum_color(live_hum()))
    avg_val_text = Text(f"{live_hum()}%", size=11,
                        weight=FontWeight.W_600, color="#555555")

    def refresh_sensor(e=None):
        sensor[0] = get_sensor_data()
        v = live_hum(); s = live_status(); c = _sc(v)
        sensor_value_text.value  = f"{v}%"
        sensor_value_text.color  = c
        sensor_status_text.value = _sl(s)
        sensor_status_text.color = c
        sensor_bar.value         = max(v, 1) / 100
        sensor_bar.color         = c
        sensor_dot.bgcolor       = "#00cc66" if s != "offline" else "#888888"
        temp_text.value          = f"{live_temp()}°C" if live_temp() else "--°C"
        avg_val_text.value       = f"{v}%"
        avg_bar_fill.width       = 70 * v / 100
        avg_bar_fill.bgcolor     = hum_color(v)
        page.update()

    pico_card = Container(
        margin=margin.only(left=14, right=14, bottom=7),
        padding=padding.symmetric(horizontal=14, vertical=12),
        bgcolor="white", border_radius=18,
        shadow=BoxShadow(blur_radius=12, color="#0a000000", offset=Offset(0, 2)),
        content=Column(spacing=8, controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Row(spacing=7, vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            sensor_dot,
                            Icon(Icons.SENSORS_ROUNDED, size=14, color="#2d5a3d"),
                            Text("Senzor Sol — Live", size=12,
                                 weight=FontWeight.W_700, color="#1a1a1a"),
                        ]),
                    IconButton(icon=Icons.REFRESH_ROUNDED, icon_size=16,
                               icon_color="#2d5a3d", on_click=refresh_sensor,
                               tooltip="Actualizează"),
                ],
            ),
            sensor_value_text,
            sensor_bar,
            sensor_status_text,
        ]),
    )

    avg_footer = Container(
        margin=margin.only(left=14, right=14, bottom=7),
        padding=padding.symmetric(horizontal=14, vertical=10),
        bgcolor="#f7faf7", border_radius=14,
        content=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(spacing=7, vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Icon(Icons.WATER_DROP_OUTLINED, size=13, color="#aaaaaa"),
                        Text("Umiditate sol acum", size=11, color="#aaaaaa",
                             weight=FontWeight.W_500),
                    ]),
                Row(spacing=7, vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(width=70, height=5, border_radius=3,
                                  bgcolor="#eeeeee", content=avg_bar_fill),
                        avg_val_text,
                    ]),
            ],
        ),
    )

    a_hum       = user_plants[0]["humidity"] if user_plants else live_hum()
    b_hum       = user_plants[1]["humidity"] if len(user_plants) > 1 else live_hum()
    advice_text = advice_engine(live_temp() or 20, live_hum() or 50, a_hum, b_hum)

    ai_advice = Container(
        margin=margin.only(left=14, right=14, bottom=7),
        padding=padding.symmetric(horizontal=14, vertical=12),
        bgcolor="#eef5f0", border_radius=14,
        border=border.all(1, "#c8dfd0"),
        content=Row(
            spacing=10, vertical_alignment=CrossAxisAlignment.START,
            controls=[
                Container(width=30, height=30, border_radius=10,
                          bgcolor="#2d5a3d", alignment=Alignment.CENTER,
                          content=Icon(Icons.AUTO_AWESOME_ROUNDED, size=13, color="white")),
                Column(spacing=3, expand=True, controls=[
                    Text("Sfat AI", size=11, weight=FontWeight.W_700, color="#2d5a3d"),
                    Text(advice_text, size=10, color="#555555"),
                ]),
            ],
        ),
    )

    plant_rows = [plant_row(p) for p in user_plants] or [
        Container(padding=padding.all(20),
                  content=Text("Nu ai plante adaugate inca.",
                               color="#aaaaaa", size=13,
                               text_align=TextAlign.CENTER))
    ]

    card = Container(
        expand=True,
        bgcolor="#f3f5f2",
        border_radius=BorderRadius(top_left=30, top_right=30,
                                   bottom_left=0, bottom_right=0),
        shadow=BoxShadow(blur_radius=24, color="#18000000", offset=Offset(0, -3)),
        content=Column(
            spacing=0, expand=True,
            controls=[
                Container(height=16),
                Container(
                    padding=padding.only(left=18, right=18, top=2, bottom=10),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Row(spacing=9, vertical_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Container(width=35, height=35, border_radius=12,
                                              bgcolor="#2d5a3d", alignment=Alignment.CENTER,
                                              content=Icon(Icons.LOCAL_FLORIST_ROUNDED,
                                                           size=16, color="white")),
                                    Column(spacing=1, controls=[
                                        Text("Plantele mele", size=15,
                                             weight=FontWeight.W_800, color="#1a1a1a"),
                                        Text(f"{len(user_plants)} plante active",
                                             size=10, color="#999999"),
                                    ]),
                                ]),
                            GestureDetector(
                                on_tap=go_plants,
                                content=Container(
                                    padding=padding.symmetric(horizontal=12, vertical=7),
                                    bgcolor="#2d5a3d", border_radius=18,
                                    content=Text("Vezi toate", size=10,
                                                 color="white", weight=FontWeight.W_600),
                                ),
                            ),
                        ],
                    ),
                ),
                Container(
                    expand=True,
                    content=ListView(
                        expand=True,
                        padding=padding.only(top=2, bottom=4),
                        controls=[
                            *plant_rows,
                            pico_card,
                            avg_footer,
                            ai_advice,
                            Container(height=6),
                        ],
                    ),
                ),
            ],
        ),
    )

    main_stack = Stack(
        expand=True,
        controls=[
            Column(spacing=0, expand=True, controls=[top_hero, card]),
            menu_overlay,
            menu_panel,
        ],
    )

    async def auto_refresh():
        while True:
            await asyncio.sleep(5)
            try:
                refresh_sensor(None)
            except Exception as ex:
                print("Auto-refresh eroare:", ex)

    page.run_task(auto_refresh)

    return Column(
        spacing=0, expand=True,
        controls=[
            Container(expand=True, content=main_stack),
            bottom_nav,
        ],
    )