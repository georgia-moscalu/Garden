from flet import *
from colors import *

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