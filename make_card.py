#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carte de visite Le Bon VTC (theme charbon/or) + QR code vers le site live."""
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"C:\Users\PC\le-bon-vtc"
SITE = "https://laya-vtc.github.io/le-bon-vtc/"

# Polices
FD = r"C:\Windows\Fonts"
def f_serif(sz): return ImageFont.truetype(os.path.join(FD, "georgia.ttf"), sz)
def f_sans(sz):  return ImageFont.truetype(os.path.join(FD, "segoeui.ttf"), sz)
def f_sans_b(sz):return ImageFont.truetype(os.path.join(FD, "segoeuib.ttf"), sz)

GOLD = (212, 175, 106)
GOLD_L = (231, 200, 135)
BG = (12, 15, 20)
BG2 = (17, 21, 28)
CARD = (22, 27, 36)
LINE = (42, 50, 63)
TEXT = (238, 241, 246)
MUTED = (154, 164, 178)

def load_hero(path=OUT + r"\hero.jpg"):
    im = Image.open(path).convert("RGB")
    return im

def cover(im, W, H):
    """Recadre l'image pour remplir WxH (cover)."""
    iw, ih = im.size
    scale = max(W/iw, H/ih)
    nw, nh = int(iw*scale), int(ih*scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw - W)//2; top = (nh - H)//2
    return im.crop((left, top, left+W, top+H))

def darken_overlay(W, H, strength=0.55):
    ov = Image.new("RGB", (W, H), (8, 10, 14))
    mask = Image.new("L", (W, H), int(255*strength))
    return ov, mask

# ---------- QR code ----------
def make_qr(path, url, size=320):
    qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), Image.LANCZOS)
    # cadre or
    pad = 18
    framed = Image.new("RGB", (size+pad*2, size+pad*2), GOLD)
    framed.paste(img, (pad, pad))
    framed.save(path)
    return framed

# ---------- Logo (reprend le SVG, dessine en PIL) ----------
def draw_logo(d, x, y, scale=1.0):
    # badge or
    bw, bh = int(44*scale), int(44*scale)
    d.rounded_rectangle([x, y, x+bw, y+bh], radius=int(12*scale), fill=GOLD)
    # voiture simplifiee (noir)
    cx, cy = x+bw//2, y+bh//2
    car_c = (26, 20, 8)
    d.rounded_rectangle([cx-15*scale, cy-2*scale, cx+15*scale, cy+8*scale], radius=int(3*scale), fill=car_c)
    d.rounded_rectangle([cx-9*scale, cy-10*scale, cx+9*scale, cy-2*scale], radius=int(2*scale), fill=car_c)
    d.ellipse([cx-12*scale, cy+6*scale, cx-5*scale, cy+13*scale], fill=car_c)
    d.ellipse([cx+5*scale, cy+6*scale, cx+12*scale, cy+13*scale], fill=car_c)
    # eclair
    d.polygon([(cx+2*scale, cy-16*scale),(cx-3*scale, cy-4*scale),(cx+1*scale, cy-4*scale),
               (cx-2*scale, cy+6*scale),(cx+6*scale, cy-6*scale),(cx+1*scale, cy-6*scale)], fill=car_c)

# ---------- Carte horizontale (85x55mm @300dpi = 1003x649) ----------
def make_card_landscape():
    W, H = 1003, 649
    m = 16
    # Fond = photo voiture noire (cover) + overlay sombre + liseré or
    hero = load_hero()
    base = cover(hero, W, H)
    ov, mask = darken_overlay(W, H, 0.55)
    base = Image.composite(ov, base, mask)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([m, m, W-m, H-m], radius=26, outline=GOLD, width=3)

    # Logo + nom (gauche haut)
    draw_logo(d, 60, 70, 1.0)
    d.text((122, 72), "Le Bon", font=f_serif(40), fill=TEXT)
    d.text((122, 118), "VTC", font=f_serif(40), fill=GOLD_L)
    # slogan
    d.text((62, 188), "Chauffeur privé · Paris & Île-de-France", font=f_sans(22), fill=MUTED)

    # separator verticale
    d.line([(W//2-40, 70), (W//2-40, H-70)], fill=LINE, width=2)

    # Bloc infos (centre/droite)
    ix = W//2 + 10
    iy = 80
    rows = [
        ("Tél.", "+33 7 61 08 18 95"),
        ("Email", "lazeregg98@gmail.com"),
        ("Zone", "Paris & Île-de-France"),
        ("Dispo", "24h/24 · 7j/7"),
    ]
    for label, val in rows:
        d.text((ix, iy), label, font=f_sans_b(20), fill=GOLD)
        d.text((ix+90, iy), val, font=f_sans(21), fill=TEXT)
        iy += 62

    # QR code (bas droite)
    qr = make_qr(OUT + r"\qr_tmp.png", SITE, size=200)
    qx = W - m - 30 - 200
    qy = H - m - 30 - 200
    base.paste(qr, (qx, qy))
    d.text((qx+100, qy-34), "Scannez", font=f_sans_b(20), fill=GOLD, anchor="mm")
    d.text((qx+100, qy+234), "le-bon-vtc", font=f_sans(18), fill=MUTED, anchor="mm")

    base.save(OUT + r"\carte_visite_landscape.png")
    print("landscape saved")

# ---------- Carte portrait (pour mobile / partage) ----------
def make_card_portrait():
    W, H = 720, 1100
    m = 18
    # Fond = photo voiture noire (cover) + overlay sombre + liseré or
    hero = load_hero()
    base = cover(hero, W, H)
    ov, mask = darken_overlay(W, H, 0.55)
    base = Image.composite(ov, base, mask)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([m, m, W-m, H-m], radius=28, outline=GOLD, width=3)

    # Logo centre haut
    draw_logo(d, W//2-22, 70, 1.0)
    d.text((W//2, 135), "Le Bon", font=f_serif(46), fill=TEXT, anchor="mm")
    d.text((W//2, 188), "VTC", font=f_serif(46), fill=GOLD_L, anchor="mm")
    d.text((W//2, 250), "Chauffeur privé · Paris & Île-de-France", font=f_sans(22), fill=MUTED, anchor="mm")

    # ligne
    d.line([(60, 300), (W-60, 300)], fill=LINE, width=2)

    # infos
    iy = 360
    rows = [
        ("Téléphone", "+33 7 61 08 18 95"),
        ("Email", "lazeregg98@gmail.com"),
        ("Zone", "Paris & Île-de-France"),
        ("Disponibilité", "24h/24 · 7j/7"),
        ("Véhicules", "Éco · Van · Berline"),
        ("Tarif", "Sur devis"),
    ]
    for label, val in rows:
        d.text((60, iy), label, font=f_sans_b(22), fill=GOLD)
        d.text((60, iy+30), val, font=f_sans(24), fill=TEXT)
        iy += 86

    # QR
    qr = make_qr(OUT + r"\qr_tmp.png", SITE, size=240)
    qx = W//2 - 120
    qy = iy + 10
    base.paste(qr, (qx, qy))
    d.text((W//2, qy+270), "Scannez pour réserver", font=f_sans_b(22), fill=GOLD_L, anchor="mm")
    d.text((W//2, qy+302), "le-bon-vtc.github.io/le-bon-vtc", font=f_sans(18), fill=MUTED, anchor="mm")

    base.save(OUT + r"\carte_visite_portrait.png")
    print("portrait saved")

# ---------- Carte verticale etroite (55x85mm @300dpi = 650x1003) ----------
def make_card_vertical():
    W, H = 650, 1003
    m = 16
    # Fond = photo voiture noire (cover) + overlay sombre + liseré or
    hero = load_hero()
    base = cover(hero, W, H)
    ov, mask = darken_overlay(W, H, 0.58)
    base = Image.composite(ov, base, mask)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([m, m, W-m, H-m], radius=26, outline=GOLD, width=3)

    # Logo centre haut
    draw_logo(d, W//2-22, 54, 1.0)
    d.text((W//2, 122), "Le Bon", font=f_serif(40), fill=TEXT, anchor="mm")
    d.text((W//2, 170), "VTC", font=f_serif(40), fill=GOLD_L, anchor="mm")
    d.text((W//2, 226), "Chauffeur privé", font=f_sans(20), fill=MUTED, anchor="mm")
    d.text((W//2, 252), "Paris & Île-de-France", font=f_sans(20), fill=MUTED, anchor="mm")

    # ligne
    d.line([(54, 296), (W-54, 296)], fill=LINE, width=2)

    # infos
    iy = 340
    rows = [
        ("Téléphone", "+33 7 61 08 18 95"),
        ("Email", "lazeregg98@gmail.com"),
        ("Zone", "Paris & Île-de-France"),
        ("Dispo", "24h/24 · 7j/7"),
        ("Véhicules", "Éco · Van · Berline"),
        ("Tarif", "Sur devis"),
    ]
    for label, val in rows:
        d.text((54, iy), label, font=f_sans_b(20), fill=GOLD)
        d.text((54, iy+28), val, font=f_sans(21), fill=TEXT)
        iy += 78

    # QR
    qr = make_qr(OUT + r"\qr_tmp.png", SITE, size=210)
    qx = W//2 - 105
    qy = iy + 6
    base.paste(qr, (qx, qy))
    d.text((W//2, qy+242), "Scannez pour réserver", font=f_sans_b(20), fill=GOLD_L, anchor="mm")
    d.text((W//2, qy+272), "le-bon-vtc.github.io", font=f_sans(17), fill=MUTED, anchor="mm")

    base.save(OUT + r"\carte_visite_verticale.png")
    print("vertical saved")

if __name__ == "__main__":
    make_card_landscape()
    make_card_portrait()
    make_card_vertical()
    print("DONE")
