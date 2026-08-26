from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, base64, qrcode

OUT = "C:/Users/PC/le-bon-vtc"
os.makedirs(OUT, exist_ok=True)

# Black & gold palette
BLACK = (13, 13, 13)        # #0d0d0d
BLACK2 = (22, 22, 22)       # #161616
GOLD = (212, 175, 55)       # #d4af37
GOLD_L = (241, 217, 122)    # #f1d97a
GOLD_D = (168, 131, 31)     # #a8831f
CREAM = (245, 239, 224)     # #f5efe0
WHITE = (255, 255, 255)

FONT_DIR = "C:/Windows/Fonts"
F_BOLD = os.path.join(FONT_DIR, "arialbd.ttf")
F_REG = os.path.join(FONT_DIR, "arial.ttf")

# Car polygon (from logo.svg, scaled)
CAR_BODY = [(12,40),(14,38),(18,38),(22,38),(25,31),(28,31),(33,31),(40,31),(43,34),(46,38),(50,38),(52,38),(54,40),(54,44),(52,46),(50,46),(48,46),(43,49),(38,49),(33,49),(28,49),(23,49),(18,46),(16,46),(14,44),(12,44)]
CAR_WIN = [(24,31),(36,31),(39,32),(41,35),(22,35)]
LEAF = [(46,16),(53,17),(50,25),(45,24)]

def gradient_circle(d, cx, cy, r, c1, c2):
    for yy in range(int(cy-r), int(cy+r)+1):
        if (yy-cy)**2 > r**2: continue
        t = (yy-(cy-r))/(2*r)
        rr = int(c1[0]+(c2[0]-c1[0])*t); gg = int(c1[1]+(c2[1]-c1[1])*t); bb = int(c1[2]+(c2[2]-c1[2])*t)
        d.line([(cx-r, yy),(cx+r, yy)], fill=(rr,gg,bb))

def draw_car(d, cx, cy, r, s, car_col, win_col, wheel_col, hub_col, leaf_col):
    def S(x,y): return (cx-r+(x-32)*s+r, cy-r+(y-32)*s+r)
    d.polygon([S(*p) for p in CAR_BODY], fill=car_col)
    d.polygon([S(*p) for p in CAR_WIN], fill=win_col)
    for wx in (22,42):
        c = S(wx,46)
        d.ellipse([c[0]-7*s, c[1]-7*s, c[0]+7*s, c[1]+7*s], fill=wheel_col)
        d.ellipse([c[0]-2.6*s, c[1]-2.6*s, c[0]+2.6*s, c[1]+2.6*s], fill=hub_col)
    d.polygon([S(*p) for p in LEAF], fill=leaf_col)

# ===== LOGO horizontal =====
LOGO_D = 120; SIZE = 66; pad_x = 24
d_tmp = ImageDraw.Draw(Image.new("RGBA",(10,10)))
f = ImageFont.truetype(F_BOLD, SIZE)
w1 = d_tmp.textlength("Le Bon ", font=f); w2 = d_tmp.textlength("VTC", font=f)
W1 = LOGO_D + 24 + int(w1+w2) + pad_x*2; H1 = LOGO_D + 40
img1 = Image.new("RGBA",(W1,H1),(0,0,0,0)); d = ImageDraw.Draw(img1)
cx,cy,r = LOGO_D//2+8, H1//2, LOGO_D//2
gradient_circle(d, cx, cy, r, BLACK, BLACK2)
d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=GOLD, width=3)
draw_car(d, cx, cy, r, LOGO_D/64.0, GOLD, BLACK, BLACK2, GOLD_L, GOLD_L)
tx = cx+r+24; ty=(H1-SIZE)//2
d.text((tx,ty),"Le Bon ", font=f, fill=CREAM)
d.text((tx+w1,ty),"VTC", font=f, fill=GOLD)
img1.save(os.path.join(OUT,"logo-le-bon-vtc-fond.png"),"PNG")
print("logo horizontal saved", img1.size)

# ===== LOGO carre =====
S2=256; rad=48
mask = Image.new("L",(S2,S2),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,S2,S2],radius=rad,fill=255)
grad = Image.new("RGBA",(S2,S2),(0,0,0,0)); gd=ImageDraw.Draw(grad)
for yy in range(S2):
    t=yy/S2; rr=int(BLACK[0]+(BLACK2[0]-BLACK[0])*t); gg=int(BLACK[1]+(BLACK2[1]-BLACK[1])*t); bb=int(BLACK[2]+(BLACK2[2]-BLACK[2])*t)
    gd.line([(0,yy),(S2,yy)], fill=(rr,gg,bb,255))
img2 = Image.alpha_composite(grad, Image.new("RGBA",(S2,S2),(0,0,0,0))); img2.putalpha(mask)
d2 = ImageDraw.Draw(img2); d2.rounded_rectangle([0,0,S2,S2],radius=rad,outline=GOLD,width=5)
draw_car(d2, S2/2, S2/2, S2/2-14, S2/64.0, GOLD, BLACK, BLACK2, GOLD_L, GOLD_L)
img2.save(os.path.join(OUT,"logo-le-bon-vtc-carre.png"),"PNG")
print("logo carre saved", img2.size)

# ===== CARTE DE VISITE (85x55mm @300dpi) =====
W,H=1003,649
card = Image.new("RGB",(W,H),BLACK)
dc = ImageDraw.Draw(card)
for y in range(H):
    t=y/H; rr=int(BLACK[0]+(BLACK2[0]-BLACK[0])*t); gg=int(BLACK[1]+(BLACK2[1]-BLACK[1])*t); bb=int(BLACK[2]+(BLACK2[2]-BLACK[2])*t)
    dc.line([(0,y),(W,y)], fill=(rr,gg,bb))
# gold border
dc.rectangle([16,16,W-16,H-16], outline=GOLD, width=4)
# glow
glow = Image.new("RGBA",(W,H),(0,0,0,0)); gdc=ImageDraw.Draw(glow)
gdc.ellipse([W-360,-200,W+160,360], fill=(212,175,55,60)); glow=glow.filter(ImageFilter.GaussianBlur(60))
card = Image.alpha_composite(card.convert("RGBA"),glow).convert("RGB"); dc=ImageDraw.Draw(card)

# logo
LOGO=92; lx,ly=46,44
gradient_circle(dc, lx+LOGO//2, ly+LOGO//2, LOGO//2, BLACK, BLACK2)
dc.ellipse([lx,ly,lx+LOGO,lx+LOGO], outline=GOLD, width=3)
draw_car(dc, lx+LOGO//2, ly+LOGO//2, LOGO//2, LOGO/64.0, GOLD, BLACK, BLACK2, GOLD_L, GOLD_L)

# name
fname = ImageFont.truetype(F_BOLD,52)
dc.text((lx+LOGO+24,50),"Le Bon ", font=fname, fill=CREAM)
bw = dc.textlength("Le Bon ", font=fname)
dc.text((lx+LOGO+24+bw,50),"VTC", font=fname, fill=GOLD)
dc.text((lx+LOGO+24,110),"Réservation VTC · Île-de-France", font=ImageFont.truetype(F_REG,26), fill=GOLD_L)

# contact
rows=[("☎","+33 7 61 08 18 95"),("✉","lazeregg98@gmail.com")]
ry=250
for ic,val in rows:
    dc.text((lx,ry),ic, font=ImageFont.truetype(F_BOLD,34), fill=GOLD)
    dc.text((lx+56,ry+4),val, font=ImageFont.truetype(F_REG,30), fill=CREAM)
    ry+=58
dc.text((lx,H-56),"24h/24 · 7j/7   —   Ponctualité · Confort · Prix clairs", font=ImageFont.truetype(F_REG,24), fill=GOLD)

# QR vCard
vcard=("BEGIN:VCARD\nVERSION:3.0\nN:;Le Bon VTC\nFN:Le Bon VTC\nORG:Le Bon VTC\nTITLE:Réservation VTC - Île-de-France\nTEL;TYPE=CELL:+33761081895\nEMAIL:lazeregg98@gmail.com\nNOTE:24h/24 - 7j/7 - Ponctualité, Confort, Prix clairs\nEND:VCARD")
qr=qrcode.QRCode(box_size=8,border=2,error_correction=qrcode.constants.ERROR_CORRECT_M); qr.add_data(vcard); qr.make(fit=True)
qr_img=qr.make_image(fill_color="black",back_color="white").convert("RGB").resize((200,200))
qsize=200; qx,qy=W-qsize-40,H-qsize-95
frame=Image.new("RGB",(qsize+24,qsize+24),GOLD); frame.paste(qr_img,(12,12))
card.paste(frame,(qx-12,qy-12))
dc.text((qx-30,qy+qsize+4),"Scannez pour\nsauvegarder le contact", font=ImageFont.truetype(F_REG,20), fill=GOLD)
card.save(os.path.join(OUT,"carte-visite-le-bon-vtc.png"),"PNG",dpi=(300,300))
print("carte saved", card.size)
print("DONE")
