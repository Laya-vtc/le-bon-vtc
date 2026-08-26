import qrcode
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFilter import GaussianBlur
import os

OUT = "C:/Users/PC/le-bon-vtc"
os.makedirs(OUT, exist_ok=True)

# --- Constants ---
NAME = "Le Bon VTC"
TAG = "Réservation VTC · Île-de-France"
PHONE = "+33 7 61 08 18 95"
PHONE_HREF = "tel:+33761081895"
EMAIL = "lazeregg98@gmail.com"
LINE1 = "24h/24 · 7j/7"
LINE2 = "Ponctualité · Confort · Prix clairs"

# --- Colors (éco vert, same family as Laya) ---
C_DARK = (11, 61, 46)      # #0b3d2e
C_MID = (21, 122, 79)      # #157a4f
C_ACCENT = (127, 227, 176) # #7fe3b0
C_LIGHT = (234, 250, 241)  # #eafaf1
C_WHITE = (255, 255, 255)

FONT_DIR = "C:/Windows/Fonts"
F_REG = os.path.join(FONT_DIR, "arial.ttf")
F_BOLD = os.path.join(FONT_DIR, "arialbd.ttf")
F_ITAL = os.path.join(FONT_DIR, "ariali.ttf")

# --- Card size: 85x55mm @ 300dpi ---
W, H = 1003, 649
card = Image.new("RGB", (W, H), C_DARK)
d = ImageDraw.Draw(card)

# Diagonal gradient backdrop
for y in range(H):
    t = y / H
    r = int(C_DARK[0] + (C_MID[0] - C_DARK[0]) * t)
    g = int(C_DARK[1] + (C_MID[1] - C_DARK[1]) * t)
    b = int(C_DARK[2] + (C_MID[2] - C_DARK[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# Soft glow top-right
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W - 360, -200, W + 160, 360], fill=(127, 227, 176, 70))
glow = glow.filter(GaussianBlur(60))
card = Image.alpha_composite(card.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(card)

# Subtle bottom band
d.rectangle([0, H - 70, W, H], fill=(6, 42, 31, 255) if False else (8, 46, 34))

def fnt(size, bold=True):
    return ImageFont.truetype(F_BOLD if bold else F_REG, size)

# --- Logo mark (rounded leaf circle + car glyph) ---
LOGO = 92
lx, ly = 46, 44
# circle
d.ellipse([lx, ly, lx + LOGO, ly + LOGO], fill=C_LIGHT)
# leaf arc
d.pieslice([lx + 18, ly + 16, lx + LOGO - 18, ly + LOGO - 14], 200, 340, fill=C_MID)
# simple car body
cxc = lx + LOGO // 2
cyc = ly + LOGO // 2 + 6
d.rounded_rectangle([cxc - 26, cyc - 8, cxc + 26, cyc + 10], radius=8, fill=C_DARK)
d.ellipse([cxc - 18, cyc + 6, cxc - 6, cyc + 18], fill=C_DARK)
d.ellipse([cxc + 6, cyc + 6, cxc + 18, cyc + 18], fill=C_DARK)

# --- Name ---
name_y = 50
d.text((lx + LOGO + 24, name_y), "Le Bon ", font=fnt(52), fill=C_WHITE)
# measure "Le Bon " width to color "VTC"
bw = d.textlength("Le Bon ", font=fnt(52))
d.text((lx + LOGO + 24 + bw, name_y), "VTC", font=fnt(52), fill=C_ACCENT)
d.text((lx + LOGO + 24, name_y + 60), TAG, font=fnt(26, bold=False), fill=C_LIGHT)

# --- Contact rows ---
rows = [
    ("☎", PHONE),
    ("✉", EMAIL),
]
ry = 250
for icon, val in rows:
    d.text((lx, ry), icon, font=fnt(34), fill=C_ACCENT)
    d.text((lx + 56, ry + 4), val, font=fnt(30, bold=False), fill=C_LIGHT)
    ry += 58

# --- Bottom tagline band ---
d.text((lx, H - 56), LINE1 + "   —   " + LINE2, font=fnt(24, bold=False), fill=C_ACCENT)

# --- QR (vCard) bottom-right ---
vcard = (
    "BEGIN:VCARD\n"
    "VERSION:3.0\n"
    f"N:;{NAME}\n"
    f"FN:{NAME}\n"
    f"ORG:{NAME}\n"
    f"TITLE:{TAG}\n"
    f"TEL;TYPE=CELL:{PHONE}\n"
    f"EMAIL:{EMAIL}\n"
    f"NOTE:{LINE1} - {LINE2}\n"
    "END:VCARD"
)
qr = qrcode.QRCode(box_size=8, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(vcard)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qsize = 200
qr_img = qr_img.resize((qsize, qsize))
# white rounded frame
qx, qy = W - qsize - 40, H - qsize - 95
frame = Image.new("RGB", (qsize + 24, qsize + 24), C_WHITE)
frame.paste(qr_img, (12, 12))
card.paste(frame, (qx - 12, qy - 12))
d.text((qx - 30, qy + qsize + 4), "Scannez pour\nsauvegarder le contact", font=fnt(20, bold=False), fill=C_ACCENT)

# --- Save ---
out_path = os.path.join(OUT, "carte-visite-le-bon-vtc.png")
card.save(out_path, "PNG", dpi=(300, 300))
print("SAVED:", out_path, card.size)
