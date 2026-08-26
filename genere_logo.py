from PIL import Image, ImageDraw, ImageFont
import os

OUT = "C:/Users/PC/le-bon-vtc"
os.makedirs(OUT, exist_ok=True)

C_ACCENT = (127, 227, 176)  # #7fe3b0
C_WHITE = (255, 255, 255)
C_DARK = (11, 61, 46)

FONT_DIR = "C:/Windows/Fonts"
F_BOLD = os.path.join(FONT_DIR, "arialbd.ttf")

SIZE = 64  # logo height in px
pad_x = 24
d_tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
f = ImageFont.truetype(F_BOLD, SIZE)
w1 = d_tmp.textlength("Le Bon ", font=f)
w2 = d_tmp.textlength("VTC", font=f)
total_w = int(w1 + w2) + pad_x * 2
total_h = SIZE + 36  # vertical padding

img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
x0 = pad_x
y0 = (total_h - SIZE) // 2
d.text((x0, y0), "Le Bon ", font=f, fill=C_WHITE)
d.text((x0 + w1, y0), "VTC", font=f, fill=C_ACCENT)

# small leaf dot before text
leaf_r = 10
d.ellipse([x0 - leaf_r*2 - 6, y0 + SIZE//2 - leaf_r, x0 - 6, y0 + SIZE//2 + leaf_r], fill=C_ACCENT)

out_path = os.path.join(OUT, "logo-le-bon-vtc.png")
img.save(out_path, "PNG")
print("SAVED:", out_path, img.size)

# Also a version with a subtle dark rounded backing for light headers
img2 = Image.new("RGBA", (total_w + 24, total_h + 12), (0, 0, 0, 0))
d2 = ImageDraw.Draw(img2)
d2.rounded_rectangle([0, 0, total_w + 24, total_h + 12], radius=14, fill=C_DARK + (255,))
d2.text((x0 + 12, (total_h + 12 - SIZE)//2), "Le Bon ", font=f, fill=C_WHITE)
d2.text((x0 + 12 + w1, (total_h + 12 - SIZE)//2), "VTC", font=f, fill=C_ACCENT)
out2 = os.path.join(OUT, "logo-le-bon-vtc-badge.png")
img2.save(out2, "PNG")
print("SAVED:", out2, img2.size)
