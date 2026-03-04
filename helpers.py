from flet import *
from colors import *

def hum_color(h: int) -> str:
    if h >= 55: return HUM_GREEN
    if h >= 40: return HUM_AMBER
    return HUM_RED

def gbox(content, w=360, h=None, rad=24, bg=GLASS_BG,
         pad=padding.symmetric(horizontal=24, vertical=20)) -> Container:
    return Container(
        width=w, height=h, bgcolor=bg, border_radius=rad,
        blur=20, border=border.all(1.5, GLASS_BORDER),
        padding=pad, content=content,
    )