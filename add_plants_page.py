from flet import *
from colors import *
from helpers import gbox, hum_color
from plants_db import ROMANIAN_PLANTS_DB, SOLAR_TEMP

def build_add_plant_page(page, user_plants, build_dashboard_page):
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
            Text("",
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
    return body