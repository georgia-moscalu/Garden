from flet import *
from log_in_back import init_db
from colors import *
from user_session import user_plants
from login_page import build_login_page
from register_page import build_register_page
from dashboard_page import build_dashboard_page
from plants_list_page import build_plants_list_page
from add_plants_page import build_add_plant_page

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

    OVERLAY = "#66000000"

    def page_shell(body) -> Container:
        return Container(
            width=500, height=740,
            content=Stack(controls=[
                Image(src="pozaFundal.jpg", width=500, height=740, fit="cover"),
                Container(width=500, height=740, bgcolor=OVERLAY),
                Container(width=500, height=740, content=body),
            ]),
        )

    def get_dashboard():
        return page_shell(build_dashboard_page(
            page, user_plants,
            lambda: page_shell(build_add_plant_page(page, user_plants, get_dashboard)),
            lambda: page_shell(build_plants_list_page(page, user_plants, get_dashboard,
                lambda: page_shell(build_add_plant_page(page, user_plants, get_dashboard)))),
        ))

    def get_login():
        return page_shell(build_login_page(page, get_dashboard, get_register))

    def get_register():
        return page_shell(build_register_page(page, get_login))

    page.add(get_login())

app(target=main, assets_dir="assets")