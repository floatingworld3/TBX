import sys

if "linux" in sys.platform:
    FONT_BASE = ("gothic", 9)
    FONT_LABEL = ("gothic", 8)
else:
    FONT_BASE = ("Helvetica", 9)
    FONT_LABEL = ("Helvetica", 8)


COLOR_TEXT = "#AAAAAA"
COLOR_TEXT_ACCENT = "#FFFFFF"
COLOR_TEXT_PASSIVE = "#595959"
COLOR_ACCENT = "#5680C2"
COLOR_BASE = "#383838"
COLOR_ELEVATED = "#484848"
COLOR_DEPRESSED = "#2d2d2d"


button = dict(
    font=FONT_BASE,
    width=64,
    height=15,
    fg=COLOR_TEXT,
    bg=COLOR_ELEVATED,
    activeforeground=COLOR_TEXT_ACCENT,
    activebackground=COLOR_ACCENT,
    relief="flat",
    compound="left",
    borderwidth=0,
    highlightthickness=0,
)

button_disabled = dict(
    font=FONT_BASE,
    width=64,
    height=15,
    fg=COLOR_TEXT_PASSIVE,
    bg=COLOR_ELEVATED,
    activeforeground=COLOR_TEXT_ACCENT,
    activebackground=COLOR_ACCENT,
    relief="flat",
    compound="left",
    highlightthickness=0,
)

placeholder_entry = dict(
    font=FONT_BASE,
    width=64,
    text="",
    fg=COLOR_TEXT_PASSIVE,
    bg=COLOR_DEPRESSED,
    selectforeground=COLOR_TEXT_PASSIVE,
    selectbackground=COLOR_DEPRESSED,
    relief="flat",
    highlightthickness=0,
)

entry = dict(
    font=FONT_BASE,
    width=9,
    justify="center",
    fg=COLOR_TEXT,
    bg=COLOR_DEPRESSED,
    selectforeground=COLOR_TEXT,
    selectbackground=COLOR_BASE,
    relief="flat",
    highlightthickness=0,
)



label_frame = dict(
    font=FONT_BASE,
    fg=COLOR_TEXT,
    bg=COLOR_BASE,
    relief="flat",
    highlightthickness=0,
)

label = dict(
    font=FONT_BASE,
    fg=COLOR_TEXT,
    bg=COLOR_BASE,
    relief="flat",
    highlightthickness=0,
)

combo = dict(
    font=FONT_BASE,
    fg=COLOR_TEXT,
    activeforeground=COLOR_TEXT,
    bg=COLOR_DEPRESSED,
    activebackground=COLOR_DEPRESSED,
    highlightthickness=0,
    relief="flat",
    borderwidth=0,
    indicatoron=0,
    width=55,
    height=8,
    compound='right',
)

frame = dict(
    bg=COLOR_BASE,
    relief="flat",
    highlightthickness=0,
)

checkbox = dict(
    bd=0,
    background=COLOR_DEPRESSED,
    activebackground=COLOR_DEPRESSED,
    activeforeground=COLOR_DEPRESSED,
    selectcolor=COLOR_DEPRESSED,
    indicatoron=False,
    onvalue=1,
    offvalue=0,
    width=8,
    height=8,
    highlightthickness=0,
)

progress_bar = dict(
    orient="horizontal",
    mode="determinate",
    length=384,
)

canvas = dict(
    bg=COLOR_BASE,
    width=60,
    height=70,
    highlightthickness=0,
)



