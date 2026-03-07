from flet import *
from colors import *
from helpers import gbox, hum_color

def build_plants_list_page(page, user_plants, build_dashboard_page, build_add_plant_page):

    def go_back(e):
        page.clean(); page.add(build_dashboard_page()); page.update()

    def go_add(e):
        page.clean(); page.add(build_add_plant_page()); page.update()

    list_container = Column(spacing=0)

    def build_rows():
        list_container.controls.clear()
        for p in user_plants:
            list_container.controls.append(plant_row(p))
        if not user_plants:
            list_container.controls.append(
                Container(padding=padding.all(20),
                          content=Text("Nu ai plante adaugate inca.",
                                       color=TEXT_SUB, size=14,
                                       text_align=TextAlign.CENTER))
            )
        page.update()

    def plant_row(p):
        color = hum_color(p["humidity"])

        def do_delete(ev):
            user_plants.remove(p)
            build_rows()

        return Container(
            margin=margin.only(bottom=10),
            padding=padding.symmetric(horizontal=16, vertical=13),
            bgcolor=GLASS_CARD,
            border_radius=16,
            border=border.all(1.2, GLASS_BORDER),
            blur=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    # Stanga: emoji + nume + prag
                    Row(spacing=12, vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=46, height=46,
                                border_radius=14,
                                bgcolor="#f0f5f0",
                                alignment=Alignment.CENTER,
                                content=Text(p["emoji"], size=26),
                            ),
                            Column(spacing=3, controls=[
                                Text(p["name"], size=15,
                                     weight=FontWeight.W_700, color=TEXT_DARK),
                                Row(spacing=6, controls=[
                                    Container(
                                        width=8, height=8,
                                        border_radius=4,
                                        bgcolor=color,
                                    ),
                                    Text(f"Prag: {p['hum_threshold']}%",
                                         size=11, color=TEXT_SUB),
                                ]),
                            ]),
                        ]),

                    # Dreapta: inel + buton delete
                    Row(spacing=12, vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Stack(alignment=Alignment.CENTER, controls=[
                                ProgressRing(width=42, height=42,
                                             value=p["humidity"] / 100,
                                             color=color, bgcolor="#22000000",
                                             stroke_width=4),
                                Text(f"{p['humidity']}%", size=9,
                                     weight=FontWeight.W_700, color=TEXT_DARK),
                            ]),
                            Container(
                                width=34, height=34,
                                border_radius=10,
                                bgcolor="#fff0f0",
                                alignment=Alignment.CENTER,
                                on_click=do_delete,
                                ink=True,
                                content=Icon(
                                    Icons.DELETE_OUTLINE_ROUNDED,
                                    size=17,
                                    color="#ff3b30",
                                ),
                            ),
                        ]),
                ],
            ),
        )

    build_rows()

    card_col = Column(
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ScrollMode.AUTO,
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
            list_container,
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

    body = Column(
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        expand=True,
        controls=[gbox(card_col, h=600,
                       pad=padding.symmetric(horizontal=22, vertical=18))],
    )
    return body