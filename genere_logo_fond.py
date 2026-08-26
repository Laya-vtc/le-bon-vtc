from PIL import Image, ImageDraw, ImageFont
import os

OUT = "C:/Users/PC/le-bon-vtc"
os.makedirs(OUT, exist_ok=True)

C_DARK = (11, 61, 46)      # green-900 #0b3d2e
C_MID = (21, 122, 79)      # green-700 #157a4f
C_ACCENT = (127, 227, 176) # green-300 #7fe3b0
C_LIGHT = (234, 250, 241)  # green-50 #eafaf1
C_INK = (20, 36, 29)       # --ink #14241d (voiture noire)
C_WHITE = (255, 255, 255)

FONT_DIR = "C:/Windows/Fonts"
F_BOLD = os.path.join(FONT_DIR, "arialbd.ttf")

# ============ VERSION 1 : logo horizontal (texte + pastille voiture) ============
LOGO_D = 120
SIZE = 66
pad_x = 28
d_tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
f = ImageFont.truetype(F_BOLD, SIZE)
w1 = d_tmp.textlength("Le Bon ", font=f)
w2 = d_tmp.textlength("VTC", font=f)

# canvas: logo circle + text
W1 = LOGO_D + 24 + int(w1 + w2) + pad_x * 2
H1 = LOGO_D + 40

img1 = Image.new("RGBA", (W1, H1), (0, 0, 0, 0))
d = ImageDraw.Draw(img1)

# gradient circle background (hero colors)
cx, cy, r = LOGO_D // 2 + 8, H1 // 2, LOGO_D // 2
for yy in range(int(cy - r), int(cy + r) + 1):
    if (yy - cy) ** 2 > r ** 2:
        continue
    t = (yy - (cy - r)) / (2 * r)
    rr = int(C_DARK[0] + (C_MID[0] - C_DARK[0]) * t)
    gg = int(C_DARK[1] + (C_MID[1] - C_DARK[1]) * t)
    bb = int(C_DARK[2] + (C_MID[2] - C_DARK[2]) * t)
    d.line([(cx - r, yy), (cx + r, yy)], fill=(rr, gg, bb))
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=C_ACCENT, width=3)

# car (black) centered in circle, scaled to logo.svg proportions
s = LOGO_D / 64.0
def S(x, y): return (cx - r + (x - 32) * s + r, cy - r + (y - 32) * s + r)
body = [S(12,40),S(14,38),S(18,38),S(22,38),S(25,31),S(28,31),S(33,31),S(40,31),S(43,34),S(46,38),S(50,38),S(52,38),S(54,40),S(54,44),S(52,46),S(50,46),S(48,46),S(43,49),S(38,49),S(33,49),S(28,49),S(23,49),S(18,46),S(16,46),S(14,44),S(12,44)]
d.polygon(body, fill=C_INK)
# windows
wpts = [S(24,31),S(36,31),S(39,32),S(41,35),S(22,35)]
d.polygon(wpts, fill=C_LIGHT)
# wheels
for wx in (22, 42):
    d.ellipse([S(wx,46)[0]-7, S(wx,46)[1]-7, S(wx,46)[0]+7, S(wx,46)[1]+7], fill=C_DARK)
    d.ellipse([S(wx,46)[0]-2.6, S(wx,46)[1]-2.6, S(wx,46)[0]+2.6, S(wx,46)[1]+2.6], fill=C_ACCENT)
# leaf (eco)
d.polygon([S(46,16),S(53,17),S(50,25),S(45,24)], fill=C_ACCENT)

# text
tx = cx + r + 24
ty = (H1 - SIZE) // 2
d.text((tx, ty), "Le Bon ", font=f, fill=C_WHITE)
d.text((tx + w1, ty), "VTC", font=f, fill=C_ACCENT)

out1 = os.path.join(OUT, "logo-le-bon-vtc-fond.png")
img1.save(out1, "PNG")
print("SAVED", out1, img1.size)

# ============ VERSION 2 : icône carrée (favicon/badge) ============
S2 = 256
img2 = Image.new("RGBA", (S2, S2), (0, 0, 0, 0))
d2 = ImageDraw.Draw(img2)
# rounded gradient bg
rad = 48
d2.rounded_rectangle([0, 0, S2, S2], radius=rad, fill=C_DARK)
for yy in range(S2):
    t = yy / S2
    rr = int(C_DARK[0] + (C_MID[0] - C_DARK[0]) * t)
    gg = int(C_DARK[1] + (C_MID[1] - C_DARK[1]) * t)
    bb = int(C_DARK[2] + (C_MID[2] - C_DARK[2]) * t)
    d2.line([(rad, yy), (S2 - rad, yy)], fill=(rr, gg, bb)) if False else None
# recompute gradient properly with rounding mask
img2 = Image.new("RGBA", (S2, S2), (0, 0, 0, 0))
mask = Image.new("L", (S2, S2), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S2, S2], radius=rad, fill=255)
grad = Image.new("RGBA", (S2, S2), (0, 0, 0, 0))
gd = ImageDraw.Draw(grad)
for yy in range(S2):
    t = yy / S2
    rr = int(C_DARK[0] + (C_MID[0] - C_DARK[0]) * t)
    gg = int(C_DARK[1] + (C_MID[1] - C_DARK[1]) * t)
    bb = int(C_DARK[2] + (C_MID[2] - C_DARK[2]) * t)
    gd.line([(0, yy), (S2, yy)], fill=(rr, gg, bb, 255))
img2 = Image.alpha_composite(grad, Image.new("RGBA", (S2, S2), (0, 0, 0, 0)))
img2.putalpha(mask)
d2 = ImageDraw.Draw(img2)
d2.rounded_rectangle([0, 0, S2, S2], radius=rad, outline=C_ACCENT, width=5)
# car black centered
s2 = S2 / 64.0
def S2c(x, y): return (32 * s2 + (x - 32) * s2, 32 * s2 + (y - 32) * s2)
body2 = [S2c(12,40),S2c(14,38),S2c(18,38),S2c(22,38),S2c(25,31),S2c(28,31),S2c(33,31),S2c(40,31),S2c(43,34),S2c(46,38),S2c(50,38),S2c(52,38),S2c(54,40),S2c(54,44),S2c(52,46),S2c(50,46),S2c(48,46),S2c(43,49),S2c(38,49),S2c(33,49),S2c(28,49),S2c(23,49),S2c(18,46),S2c(16,46),S2c(14,44),S2c(12,44)]
d2.polygon(body2, fill=C_INK)
d2.polygon([S2c(24,31),S2c(36,31),S2c(39,32),S2c(41,35),S2c(22,35)], fill=C_LIGHT)
for wx in (22, 42):
    d2.ellipse([S2c(wx,46)[0]-14, S2c(wx,46)[1]-14, S2c(wx,46)[0]+14, S2c(wx,46)[1]+14], fill=C_DARK)
    d2.ellipse([S2c(wx,46)[0]-5, S2c(wx,46)[1]-5, S2c(wx,46)[0]+5, S2c(wx,46)[1]+5], fill=C_ACCENT)
d2.polygon([S2c(46,16),S2c(53,17),S2c(50,25),S2c(45,24)], fill=C_ACCENT)
out2 = os.path.join(OUT, "logo-le-bon-vtc-carre.png")
img2.save(out2, "PNG")
print("SAVED", out2, img2.size)
