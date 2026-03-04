from flet import *
from colors import *
from helpers import gbox, hum_color
from ai_engine import advice_engine
from plants_db import SOLAR_TEMP, AVG_HUMIDITY

def build_dashboard_page(page, user_plants, build_add_plant_page, build_plants_list_page):

    scroll_ref = [None]

    def go_home(e):
        if scroll_ref[0]:
            scroll_ref[0].scroll_to(offset=0, duration=300)
            page.update()

    def go_add_plant(e):
        page.clean(); page.add(build_add_plant_page()); page.update()

    def go_plants(e):
        page.clean(); page.add(build_plants_list_page()); page.update()

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
                nav_btn(Icons.HOME_ROUNDED, "Acasa", active=True, on_click_fn=go_home),
                nav_btn(Icons.ADD_CIRCLE_OUTLINE_ROUNDED, "Adauga", on_click_fn=go_add_plant),
                nav_btn(Icons.LOCAL_FLORIST_ROUNDED, "Plantele", on_click_fn=go_plants),
            ],
        ),
    )

    header = gbox(
        w=None, rad=18, bg=GLASS_BG,
        pad=padding.symmetric(horizontal=18, vertical=12),
        content=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(spacing=6, tight=True, controls=[
                    Icon(Icons.WB_SUNNY_ROUNDED, color=AMBER_W, size=20),
                    Text(f"{SOLAR_TEMP}°C", size=17, weight=FontWeight.W_800, color=TEXT_DARK),
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

    greeting = gbox(
        w=None, rad=18, bg=GLASS_BG,
        pad=padding.symmetric(horizontal=18, vertical=14),
        content=Column(spacing=2, controls=[
            Text("Buna ziua!", size=22, weight=FontWeight.W_800, color=TEXT_DARK),
            Text("Gradina ta este monitorizata in timp real.", size=13, color=TEXT_SUB),
        ]),
    )

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
                            Text(f"{AVG_HUMIDITY}%", size=26, weight=FontWeight.W_800, color=TEXT_DARK),
                            Text("umid.", size=11, color=TEXT_SUB),
                        ],
                    ),
                ]),
                Column(spacing=10, controls=[
                    Row(spacing=7, controls=[
                        Container(width=8, height=8, border_radius=4, bgcolor=HUM_GREEN),
                        Text("Umiditate medie globala", size=13, color=TEXT_DARK, weight=FontWeight.W_600),
                    ]),
                    Row(spacing=7, controls=[
                        Icon(Icons.SENSORS_ROUNDED, size=14, color=ACCENT_MID),
                        Text(f"{len(user_plants)} senzori activi", size=12, color=TEXT_SUB),
                    ]),
                    Row(spacing=7, controls=[
                        Icon(Icons.WATER_DROP_OUTLINED, size=14, color="#2980b9"),
                        Text("2.4 L consumate astazi", size=12, color=TEXT_SUB),
                    ]),
                    Container(
                        padding=padding.symmetric(horizontal=10, vertical=4),
                        bgcolor="#2227ae60", border_radius=20,
                        border=border.all(1, "#4427ae60"),
                        content=Text("Live", size=11, color=ACCENT_GREEN, weight=FontWeight.W_700),
                    ),
                ]),
            ],
        ),
    )

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
                        Text(f"{hum}%", size=13, weight=FontWeight.W_800, color=TEXT_DARK),
                    ]),
                ],
            ),
        )

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
                        content=Icon(Icons.AUTO_AWESOME_ROUNDED, size=15, color=ACCENT_GREEN),
                        alignment=Alignment.CENTER,
                    ),
                    Column(spacing=1, controls=[
                        Text("Sfat zilnic AI", size=14, weight=FontWeight.W_700, color=TEXT_DARK),
                        Text("Analiza temperatura x umiditate", size=11, color=TEXT_SUB),
                    ]),
                ]),
            Divider(height=1, color="#33000000"),
            Text(advice_text, size=12, color=TEXT_SUB),
        ]),
    )

    scroll_col = Column(
        spacing=12, scroll=ScrollMode.AUTO,
        controls=[header, greeting, humidity_section, build_grid(), advice_box, Container(height=4)],
    )
    scroll_ref[0] = scroll_col

    scroll_body = Container(
        expand=True,
        padding=padding.symmetric(horizontal=18, vertical=14),
        content=scroll_col,
    )

    body = Column(spacing=0, expand=True, controls=[scroll_body, bottom_bar])
    return body