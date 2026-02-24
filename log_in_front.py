from flet import *
from log_in_back import login, register, init_db

PRIMARY_GREEN = "#2d5016"
ACCENT_GREEN = "#00573F"
LIGHT_BG = "#f1faee"
SOIL_BROWN = "#8b6f47"
WARM_ACCENT = "#F0E68C"
TEXT_DARK = "#1b3a1b"
TEXT_LIGHT = "#666666"


def main(page: Page):
    init_db()

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

    email_input = TextField(
        width=280, height=50, hint_text='Adresă de email',
        border=InputBorder.UNDERLINE, prefix_icon=Icons.EMAIL, color='black'
    )

    password_input = TextField(
        width=280, height=50, hint_text='Parolă',
        border=InputBorder.UNDERLINE, prefix_icon=Icons.LOCK,
        password=True, can_reveal_password=True, color='black'
    )

    status_message = Text(value="", size=14, text_align=TextAlign.CENTER, width=280)

    # ================= EVENIMENTE =================
    def handle_login(e):
        result = login(email_input.value, password_input.value)

        if result["success"]:
            status_message.color = PRIMARY_GREEN
            status_message.value = "Autentificare reușită!"
        else:
            status_message.color = "red"
            status_message.value = result["message"]

        page.update()

    def handle_register(e):
        result = register(email_input.value, password_input.value)

        if result["success"]:
            status_message.color = PRIMARY_GREEN
            status_message.value = "Cont creat cu succes! Te poți autentifica."
        else:
            status_message.color = "red"
            status_message.value = result["message"]

        page.update()

    # ==============================================

    body = Container(
        alignment=Alignment(0, 0),
        width=500,
        height=740,
        content=Stack(
            alignment=Alignment(0, 0),
            controls=[
                Container(
                    width=500, height=740,
                    gradient=LinearGradient(
                        colors=[ACCENT_GREEN, WARM_ACCENT],
                        begin=Alignment(-1, -1), end=Alignment(1, 1),
                    ),
                ),

                # MAIN CARD
                Container(
                    bgcolor="#ffffff", opacity=0.85,
                    border_radius=20, width=360, height=560,
                    alignment=Alignment(0, 0),
                    padding=Padding.symmetric(horizontal=20),
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            Text("Bine ai venit", size=34, weight=FontWeight.W_800, color=PRIMARY_GREEN,
                                 font_family="Poppins"),
                            Text("Cultivă-ți grădina cu plăcere", color=TEXT_LIGHT, size=14),
                            Container(height=25),

                            Container(content=email_input, alignment=Alignment(0, 0), width=360),
                            Container(height=12),

                            Container(content=password_input, alignment=Alignment(0, 0), width=360),

                            Row(
                                controls=[TextButton("Ți-ai uitat parola?", style=ButtonStyle(color=ACCENT_GREEN))],
                                alignment=MainAxisAlignment.START,
                            ),
                            Container(height=5),

                            Container(content=status_message, alignment=Alignment(0, 0), width=360),
                            Container(height=10),

                            # Adăugăm on_click=handle_login
                            Container(
                                content=ElevatedButton(
                                    content=Text("Autentificare", color='white', weight=FontWeight.W_700, size=16),
                                    width=280, height=50, bgcolor=ACCENT_GREEN,
                                    on_click=handle_login  # <--- Legătura cu funcția de login
                                ),
                                alignment=Alignment(0, 0), width=360,
                            ),
                            Container(height=14),

                            Container(
                                content=Row(
                                    spacing=-10,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text("Nu ai cont? ", color=TEXT_LIGHT, size=13),
                                        # Adăugăm on_click=handle_register
                                        TextButton(
                                            "Creează cont",
                                            style=ButtonStyle(color=PRIMARY_GREEN),
                                            on_click=handle_register  # <--- Legătura cu funcția de register
                                        ),
                                    ],
                                ),
                                width=360, alignment=Alignment(0, 0),
                            ),
                        ],
                    ),
                ),
            ]
        )
    )

    page.add(body)
    page.update()


app(target=main, view=AppView.WEB_BROWSER)