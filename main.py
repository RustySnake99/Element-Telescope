import json
from os.path import dirname
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk

p = dirname(__file__)
with open(f"{p}/elements.json") as elements:
    ELEMENTS = json.load(elements)

BY_POS = {(e["position"][0], e["position"][1]): e for e in ELEMENTS}
CATEGORY_COLORS = {
    "alkali_metal": "#FF6B6B",
    "alkaline_earth_metal": "#FFA94D",
    "transition_metal": "#74C0FC",
    "post_transition_metal": "#A9E34B",
    "metalloid": "#63E6BE",
    "nonmetal": "#FFD43B",
    "halogen": "#DA77F2",
    "noble_gas": "#FF8787",
    "lanthanide": "#66D9E8",
    "actinide": "#F773AC"
}
DEFAULT_COLOR = "#CED4DA"
LABELS = {
    "alkali_metal": "Alkali Metal",
    "alkaline_earth_metal": "Alkaline Earth Metal",
    "transition_metal": "Transition Metal",
    "post_transition_metal": "Post Transition Metal",
    "metalloid": "Metalloid",
    "halogen": "Halogen",
    "noble_gas": "Noble Gas",
    "lanthanide": "Lanthanide",
    "actinide": "Actinide"
}
BG = "#1A1A2E"
PANEL_BG = "#16213E"
TEXT = "#E0E0E0"
MUTED = "#888"
CELL_WIDTH, CELL_HEIGHT = 62, 52
IMG_SIZE = 160

def get_colour(element: dict) -> str:
    return CATEGORY_COLORS.get(element.get("category", ""), DEFAULT_COLOR)
def fmt(value, unit=""):
    return "-" if value is None else f"{value} {unit}".strip()

def load_element_image(path):
    """Load and thumbnail the element image. Returns a PhotoImage or None."""
    img = Image.open(path).convert("RGB")
    img.thumbnail((IMG_SIZE, IMG_SIZE))
    return ImageTk.PhotoImage(img)


root = tk.Tk()
root.title("Element Telescope")
root.configure(bg=BG)
root.resizable(True, True)

bold_font = font.Font(family="Helvetica", size=8, weight="bold")
sym_font = font.Font(family="Helvetica", size=13, weight="bold")
num_font = font.Font(family="Helvetica", size=7)
small_font = font.Font(family="Helvetica", size=7)
title_font = font.Font(family="Helvetica", size=18, weight="bold")
h2_font = font.Font(family="Helvetica", size=13, weight="bold")
detail_font = font.Font(family="Helvetica", size=11)

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=20, pady=(14, 4))

tk.Label(header, text="Periodic Table of Elements", font=title_font, bg=BG, fg=TEXT).pack(side="left")
tk.Label(header, text="Click any element for more information", font=h2_font, bg=BG, fg=MUTED).pack(side="left", padx=14)

grid_frame = tk.Frame(root, bg=BG)
grid_frame.pack(fill="both", expand=True, padx=10, pady=4)
canvas = tk.Canvas(grid_frame, bg=BG, highlightthickness=0)
canvas.pack(fill="both", expand=True)

COLS, ROWS = 10, 10

def visual_row(r):
    return r

element_frame = {}

_popup = None
_img_ref = None
def show_detail(el):
    global _popup, _img_ref
    if _popup and _popup.winfo_exists():
        _popup.destroy()

    color = get_colour(el)
    popup = tk.Toplevel(root)
    popup.title(f"{el["name"]} ({el['symbol']})")
    popup.configure(bg=PANEL_BG)
    popup.resizable(True, True)
    _popup = popup

    banner = tk.Frame(popup, bg=color, pady=18, padx=24)
    banner.pack(fill="x")
 
    left = tk.Frame(banner, bg=color)
    left.pack(side="left")
 
    tk.Label(left, text=str(el["atomic_number"]), font=bold_font,
             bg=color, fg="#333").pack(anchor="w")
    tk.Label(left, text=el["symbol"],
             font=font.Font(family="Helvetica", size=48, weight="bold"),
             bg=color, fg="#111").pack()
    tk.Label(left, text=el["name"],
             font=font.Font(family="Helvetica", size=16),
             bg=color, fg="#222").pack()
 
    right = tk.Frame(banner, bg=color)
    right.pack(side="left", padx=30, anchor="n", pady=8)
 
    cat_text = LABELS.get(el.get("category", ""), el.get("category", "—"))
    tk.Label(right, text=f"Category:  {cat_text}",
             font=detail_font, bg=color, fg="#222").pack(anchor="w", pady=2)
    tk.Label(right, text=f"Atomic Mass:  {fmt(el.get('atomic_mass'))} u",
             font=detail_font, bg=color, fg="#222").pack(anchor="w", pady=2)
    e_cfg = el.get("e_config", "—")
    tk.Label(right, text=f"Electron Config:  {e_cfg}",
             font=detail_font, bg=color, fg="#222").pack(anchor="w", pady=2)

    body = tk.Frame(popup, bg=PANEL_BG, padx=24, pady=16)
    body.pack(fill="both", expand=True)

    img_frame = tk.Frame(body, bg=PANEL_BG)
    img_frame.grid(row=5, column=0, rowspan=6, padx=(0, 20), sticky="n", pady=20)
 
    photo = load_element_image(f"{p}/{el["image"]}")
    _img_ref = photo  # prevent garbage collection
    img_lbl = tk.Label(img_frame, image=photo, bg=PANEL_BG, relief="flat", bd=0)
    img_lbl.pack()
    tk.Label(img_frame, text=el["name"], font=small_font, bg=PANEL_BG, fg=MUTED).pack(pady=(4, 0))    
 
    fields = [
        ("Melting Point", fmt(el.get("melting_point"), "K")),
        ("Boiling Point", fmt(el.get("boiling_point"), "K")),
        ("Oxidation States",
         ", ".join(str(s) for s in el.get("oxidation_states", [])) or "—"),
        ("Period (Row)", str(el["position"][0] + 1)),
        ("Group (Col)",  str(el["position"][1] + 1)),
    ]
 
    for i, (key, val) in enumerate(fields):
        tk.Label(body, text=key + ":", font=bold_font,
                 bg=PANEL_BG, fg=MUTED, anchor="e", width=18)\
            .grid(row=i, column=0, sticky="e", pady=4, padx=(0, 10))
        tk.Label(body, text=val, font=detail_font,
                 bg=PANEL_BG, fg=TEXT, anchor="w")\
            .grid(row=i, column=1, sticky="w", pady=4)

    tk.Button(popup, text="✕  Close", command=popup.destroy,
              bg=color, fg="#111",
              font=bold_font, relief="flat", padx=12, pady=6,
              cursor="hand2")\
        .pack(pady=(0, 14))

    popup.update_idletasks()
    pw, ph = popup.winfo_width(), popup.winfo_height()
    rx = root.winfo_x() + (root.winfo_width()  - pw) // 2
    ry = root.winfo_y() + (root.winfo_height() - ph) // 2
    popup.geometry(f"+{rx}+{ry}")


def make_cell(el, vrow, vcol):
    color = get_colour(el)
    f = tk.Frame(canvas, bg=color, relief="flat", bd=0, width=CELL_WIDTH, height=CELL_HEIGHT, cursor="hand2")
    f.pack_propagate(False)

    tk.Label(f, text=str(el["atomic_number"]), font=num_font, bg=color, fg="#333").pack(anchor="w", padx=3, pady=(2, 0))
    tk.Label(f, text=el["symbol"], font=sym_font, bg=color, fg="#111").pack()
    tk.Label(f, text=el["name"], font=small_font, bg=color, fg="#333").pack()

    def on_enter(e, fr=f, c=color):
        fr.configure(bg="white")
        for i in fr.winfo_children():
            i.configure(bg="white")
    def on_leave(e, fr=f, c=color):
        fr.configure(bg=c)
        for i in fr.winfo_children():
            i.configure(bg=c)
    def on_click(e, element=el):
        show_detail(element)
    
    f.bind("<Enter>", on_enter)
    f.bind("<Leave>", on_leave)
    f.bind("<Button-1>", on_click)
    for i in f.winfo_children():
        i.bind("<Enter>", on_enter)
        i.bind("<Leave>", on_leave)
        i.bind("<Button-1>", on_click)
    
    x = vcol * (CELL_WIDTH + 2) + 4
    y = vrow * (CELL_HEIGHT + 2) + 4
    if vrow >= 8:
        y += 18

    canvas.create_window(x, y, anchor="nw", window=f, width=CELL_WIDTH, height=CELL_HEIGHT)
    element_frame[(vrow, vcol)] = f


if __name__ == "__main__":
    for i in ELEMENTS:
        r, c = i["position"]
        make_cell(i, r, c)
    canvas.create_text(4, 7 * (CELL_HEIGHT + 2) + 4 + (CELL_WIDTH + 2) // 2 + 2, anchor="w", text="↓  Lanthanides / Actinides", fill=MUTED, font=small_font)

    total_w = COLS * (CELL_WIDTH + 2) + 8
    total_h = 10 * (CELL_HEIGHT + 2) + 28
    canvas.configure(width=total_w, height=total_h, scrollregion=(0, 0, total_w, total_h))

    legend = tk.Frame(root, bg=BG)
    legend.pack(fill="x", padx=14, pady=(2, 6))
    tk.Label(legend, text="Categories: ", font=small_font, bg=BG, fg=MUTED).grid(row=0, column=0, sticky="w")

    col_idx = 1
    for i, j in CATEGORY_COLORS.items():
        color = CATEGORY_COLORS[i]
        dot = tk.Label(legend, text="\t", bg=color, relief="flat")
        dot.grid(row=0, column=col_idx, padx=(6, 1))
        lbl = tk.Label(legend, text=i.replace("_", " ").capitalize(), font=small_font, bg=BG, fg=TEXT)
        lbl.grid(row=0, column=col_idx + 1, sticky="w", padx=(0, 4))
        col_idx += 2

    root.mainloop()