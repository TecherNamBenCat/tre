#!/usr/bin/env python3
"""Tre — sinh logo và hình nền màn hình chính.

Hình nền lấy từ ảnh gốc tai-nguyen/anh-goc/hoc-sinh-den-truong.png (không in chữ).
Đổi hình nền: thay ảnh gốc, chạy lại script, rồi tăng số trong
goi-tre/usr/share/tre/hinh-nen/PHIEN_BAN để máy đã cài tự đổi theo.

Chạy:  python3 cong-cu/tao-hinh-nen.py
Cần:   pip install pillow   (và font DejaVu Sans, có sẵn trên Debian)
Muốn đổi màu/chữ: sửa các hằng số ở đầu file rồi chạy lại.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC, "goi-tre", "usr", "share", "tre")
ANH_NEN = os.path.join(GOC, "tai-nguyen", "anh-goc", "hoc-sinh-den-truong.png")

TEN = "Tre"
KHAU_HIEU = "Hệ điều hành học tập"

# Bảng màu: xanh tre non -> xanh lá đậm
NEN_TREN = (16, 58, 44)
NEN_DUOI = (8, 32, 26)
THAN_TRE = (139, 186, 92)
DOT_TRE = (98, 140, 62)
LA_TRE = (122, 178, 84)
CHU = (240, 246, 232)
CHU_PHU = (190, 214, 170)

FONT_DAM = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
]
FONT_THUONG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]


def font(ds, co):
    for p in ds:
        if os.path.exists(p):
            return ImageFont.truetype(p, co)
    return ImageFont.load_default()


def nen_chuyen_mau(w, h):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        for x in range(w):
            # thêm chút sáng ở góc phải trên (ánh nắng xuyên qua rặng tre)
            d = math.hypot((x - w * 0.82) / w, (y - h * 0.15) / h)
            sang = max(0.0, 0.55 - d) * 0.9
            c = [int(NEN_TREN[i] * (1 - t) + NEN_DUOI[i] * t) for i in range(3)]
            c = [min(255, int(v + sang * 70)) for v in c]
            px[x, y] = tuple(c)
    return img


def la(draw, cx, cy, dai, rong, goc, mau):
    """Vẽ một lá tre hình mũi mác."""
    pts = []
    n = 24
    for i in range(n + 1):
        t = i / n
        x = t * dai
        y = math.sin(math.pi * t) ** 0.8 * rong * (1 - 0.35 * t)
        pts.append((x, y))
    pts += [(x, -y) for x, y in reversed(pts)]
    c, s = math.cos(goc), math.sin(goc)
    pts = [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]
    draw.polygon(pts, fill=mau)


def cay_tre(lop, x0, day, ngon, rong, nghieng, so_dot, tl):
    """Một cây tre: các đốt thân + mắt tre + vài nhánh lá."""
    d = ImageDraw.Draw(lop)
    cao = day - ngon
    dot = cao / so_dot
    for i in range(so_dot):
        y1 = day - i * dot
        y2 = y1 - dot + 4 * tl
        xa = x0 + nghieng * (day - y1)
        xb = x0 + nghieng * (day - y2)
        r = rong * (1 - 0.25 * i / so_dot)
        d.polygon([(xa - r / 2, y1), (xa + r / 2, y1), (xb + r / 2, y2), (xb - r / 2, y2)],
                  fill=THAN_TRE + (255,))
        # vệt sáng trên thân
        d.line([(xa - r / 4, y1 - 6 * tl), (xb - r / 4, y2 + 6 * tl)],
               fill=(196, 226, 150, 150), width=max(1, int(r / 7)))
        # mắt tre
        d.rounded_rectangle([xb - r / 2 - 3 * tl, y2 - 5 * tl, xb + r / 2 + 3 * tl, y2 + 5 * tl],
                            radius=4 * tl, fill=DOT_TRE + (255,))
        # nhánh lá ở các đốt phía trên
        if i >= so_dot // 3 and random.random() < 0.75:
            huong = random.choice([-1, 1])
            for _ in range(random.randint(2, 4)):
                g = math.radians(random.uniform(-45, 30))  # hướng sang phải, hơi rủ xuống
                if huong < 0:
                    g = math.pi - g                       # lật sang trái
                la(d, xb, y2, random.uniform(90, 150) * tl, random.uniform(10, 15) * tl,
                   g, LA_TRE + (random.randint(200, 255),))


def hinh_nen(w=1920, h=1080, tl=2):
    random.seed(1945)
    W, H = w * tl, h * tl
    img = nen_chuyen_mau(w, h).resize((W, H)).convert("RGBA")

    # lớp tre phía xa (mờ) và phía gần (rõ)
    xa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for x in (0.62, 0.70, 0.93):
        cay_tre(xa, W * x, H + 20, -40, 26 * tl, random.uniform(-0.04, 0.03), 7, tl)
    xa = xa.filter(ImageFilter.GaussianBlur(6 * tl))
    xa.putalpha(xa.getchannel("A").point(lambda a: int(a * 0.45)))
    img.alpha_composite(xa)

    gan = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for x, r in ((0.76, 46), (0.84, 38), (0.885, 30)):
        cay_tre(gan, W * x, H + 20, -60, r * tl, random.uniform(-0.05, 0.02), 6, tl)
    bong = gan.filter(ImageFilter.GaussianBlur(10 * tl))
    bong.putalpha(bong.getchannel("A").point(lambda a: int(a * 0.35)))
    img.alpha_composite(bong, (14 * tl, 10 * tl))
    img.alpha_composite(gan)

    d = ImageDraw.Draw(img)
    x, y = 120 * tl, H - 330 * tl
    d.text((x, y), TEN, font=font(FONT_DAM, 150 * tl), fill=CHU)
    d.text((x + 8 * tl, y + 185 * tl), KHAU_HIEU, font=font(FONT_THUONG, 40 * tl), fill=CHU_PHU)
    d.line([(x + 8 * tl, y + 170 * tl), (x + 120 * tl, y + 170 * tl)], fill=LA_TRE, width=5 * tl)
    return img.resize((w, h), Image.LANCZOS).convert("RGB")


def logo(co=512):
    tl = 4
    S = co * tl
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.22, fill=NEN_TREN + (255,))
    # ba đốt tre đứng
    for cx, cao, r in ((0.36, 0.70, 0.11), (0.55, 0.78, 0.13), (0.72, 0.58, 0.09)):
        x = S * cx
        top = S * (0.88 - cao)
        bot = S * 0.88
        so = 3
        for i in range(so):
            y2 = bot - (bot - top) * i / so
            y1 = bot - (bot - top) * (i + 1) / so + S * 0.012
            d.rounded_rectangle([x - S * r / 2, y1, x + S * r / 2, y2], radius=S * 0.02,
                                fill=THAN_TRE + (255,))
            d.rounded_rectangle([x - S * r / 2 - S * 0.012, y1 - S * 0.012,
                                 x + S * r / 2 + S * 0.012, y1 + S * 0.006],
                                radius=S * 0.008, fill=DOT_TRE + (255,))
    la(d, S * 0.55, S * 0.32, S * 0.30, S * 0.05, math.radians(-30), LA_TRE + (255,))
    la(d, S * 0.55, S * 0.32, S * 0.24, S * 0.04, math.radians(-150), LA_TRE + (255,))
    return img.resize((co, co), Image.LANCZOS)


def main():
    os.makedirs(os.path.join(RA, "hinh-nen"), exist_ok=True)
    os.makedirs(os.path.join(RA, "logo"), exist_ok=True)
    im = Image.open(ANH_NEN).convert("RGB")
    tl = max(1920 / im.width, 1080 / im.height)
    im = im.resize((round(im.width * tl), round(im.height * tl)), Image.LANCZOS)
    x, y = (im.width - 1920) // 2, (im.height - 1080) // 2
    im = im.crop((x, y, x + 1920, y + 1080)).filter(ImageFilter.UnsharpMask(radius=1.5, percent=70, threshold=2))
    im.save(os.path.join(RA, "hinh-nen", "tre-1920x1080.jpg"), quality=92, optimize=True)
    lg = logo(512)
    for co in (512, 256, 64):
        lg.resize((co, co), Image.LANCZOS).save(os.path.join(RA, "logo", f"tre-logo-{co}.png"))
    print("Đã tạo hình nền và logo trong", RA)


if __name__ == "__main__":
    main()
