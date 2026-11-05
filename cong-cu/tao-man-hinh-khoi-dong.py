#!/usr/bin/env python3
"""Tre — tạo tài nguyên cho màn hình động khởi động / tắt máy (Plymouth)
và dựng video xem trước.

Chạy (không tham số = dùng ảnh trong tai-nguyen/anh-goc, ghi vào gói tre-he-thong):
  python3 cong-cu/tao-man-hinh-khoi-dong.py
  python3 cong-cu/tao-man-hinh-khoi-dong.py <ảnh-đến-trường> <ảnh-tan-trường> <thư-mục-theme> [thư-mục-video]
"""
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_DAM = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SO_DOT = 10            # số đốt tre trên thanh tiến trình
DOT_W, DOT_H, KHE = 34, 12, 4
# vị trí khối chữ "Tre" + thanh tiến trình trên ảnh bật máy (toạ độ ở cỡ 1920x1080)
TH_X, TH_Y_TRE, TH_Y_THANH = 70, 690, 948


# ---------------------------------------------------------------- tài nguyên
def nen(duong_dan, ra):
    """Phóng ảnh nền lên 1920x1080 (cắt giữa nếu lệch tỉ lệ), làm nét nhẹ."""
    im = Image.open(duong_dan).convert("RGB")
    tl = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * tl), round(im.height * tl)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=70, threshold=2))
    im.save(ra, optimize=True)
    return im


def con_co(canh_len, mau, co=64):
    """Cò bay: thân + 2 cánh; canh_len=True/False để tạo 2 khung vỗ cánh."""
    S = 4
    im = Image.new("RGBA", (co * S, co // 2 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = co * S / 2, co * S / 4 + (0 if canh_len else 4 * S)
    w = max(2, int(co * S * 0.06))
    if canh_len:
        d.line([(cx - co * S * 0.46, cy - co * S * 0.18), (cx - co * S * 0.2, cy - co * S * 0.02), (cx, cy)], fill=mau, width=w, joint="curve")
        d.line([(cx + co * S * 0.46, cy - co * S * 0.18), (cx + co * S * 0.2, cy - co * S * 0.02), (cx, cy)], fill=mau, width=w, joint="curve")
    else:
        d.line([(cx - co * S * 0.46, cy + co * S * 0.08), (cx - co * S * 0.22, cy - co * S * 0.06), (cx, cy)], fill=mau, width=w, joint="curve")
        d.line([(cx + co * S * 0.46, cy + co * S * 0.08), (cx + co * S * 0.22, cy - co * S * 0.06), (cx, cy)], fill=mau, width=w, joint="curve")
    d.ellipse([cx - co * S * 0.07, cy - co * S * 0.03, cx + co * S * 0.12, cy + co * S * 0.04], fill=mau)
    return im.resize((co, co // 2), Image.LANCZOS)


def dot_tre(day):
    """Một đốt tre nằm ngang: rỗng (mờ) hoặc đầy (xanh)."""
    S = 4
    im = Image.new("RGBA", (DOT_W * S, (DOT_H + 6) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y0 = 3 * S
    if day:
        for i in range(DOT_H * S):
            t = i / (DOT_H * S)
            c = (int(120 + 60 * (1 - abs(t - 0.35) * 2)), int(185 + 45 * (1 - abs(t - 0.35) * 2)), 70, 255)
            d.line([(2 * S, y0 + i), (DOT_W * S - 2 * S, y0 + i)], fill=c)
        mat = (80, 130, 50, 255)
    else:
        d.rounded_rectangle([2 * S, y0, DOT_W * S - 2 * S, y0 + DOT_H * S], radius=3 * S,
                            fill=(255, 255, 255, 70), outline=(255, 255, 255, 140), width=S)
        mat = (255, 255, 255, 150)
    # mắt tre ở đầu đốt
    d.rounded_rectangle([DOT_W * S - 5 * S, y0 - 2 * S, DOT_W * S, y0 + DOT_H * S + 2 * S], radius=S * 1.5, fill=mat)
    return im.resize((DOT_W, DOT_H + 6), Image.LANCZOS)


def chu(noi_dung, co=34, dam=False):
    f = ImageFont.truetype(FONT_DAM if dam else FONT, co)
    x0, y0, x1, y1 = f.getbbox(noi_dung)
    pad = 16
    im = Image.new("RGBA", (x1 - x0 + pad * 2, y1 - y0 + pad * 2), (0, 0, 0, 0))
    bong = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(bong).text((pad - x0 + 2, pad - y0 + 2), noi_dung, font=f, fill=(0, 0, 0, 200))
    im.alpha_composite(bong.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(im).text((pad - x0, pad - y0), noi_dung, font=f, fill=(255, 255, 255, 255))
    return im


def tao_tai_nguyen(anh_sang, anh_chieu, thu_muc):
    os.makedirs(thu_muc, exist_ok=True)
    p = lambda n: os.path.join(thu_muc, n)
    them_thuong_hieu(nen(anh_sang, p("nen-khoi-dong.png"))).save(p("nen-khoi-dong.png"), optimize=True)
    nen(anh_chieu, p("nen-tat-may.png"))
    con_co(True, (255, 255, 255, 255)).save(p("co-trang-1.png"))
    con_co(False, (255, 255, 255, 255)).save(p("co-trang-2.png"))
    con_co(True, (40, 30, 30, 255)).save(p("co-toi-1.png"))
    con_co(False, (40, 30, 30, 255)).save(p("co-toi-2.png"))
    dot_tre(False).save(p("dot-rong.png"))
    dot_tre(True).save(p("dot-day.png"))
    chu("Chào buổi sáng! Đang khởi động…", 26).save(p("chu-khoi-dong.png"))
    chu("Tan học rồi! Hẹn gặp lại nhé.", 40, True).save(p("chu-tat-may.png"))
    chu("Đang khởi động lại…", 40, True).save(p("chu-khoi-dong-lai.png"))
    Image.new("RGBA", (16, 16), (0, 0, 0, 255)).save(p("den.png"))
    # nền mờ phía sau thanh tiến trình và chữ, để luôn dễ đọc trên mọi ảnh
    nen_mo(Image.open(p("chu-tat-may.png")).width + 50, 84).save(p("nen-chu-tat.png"))
    nen_mo(Image.open(p("chu-khoi-dong-lai.png")).width + 50, 84).save(p("nen-chu-lai.png"))


def them_thuong_hieu(im):
    """Thêm chữ "Tre" + gạch xanh + "Hệ điều hành học tập" ở góc dưới bên trái,
    kèm vùng tối mờ phía sau cho dễ đọc (giống mẫu ban đầu)."""
    im = im.convert("RGBA")
    toi = Image.new("L", (W, H), 0)
    dt = ImageDraw.Draw(toi)
    dt.ellipse([-420, 560, 820, 1400], fill=150)
    toi = toi.filter(ImageFilter.GaussianBlur(120))
    lop = Image.new("RGBA", (W, H), (5, 20, 10, 0))
    lop.putalpha(toi)
    im.alpha_composite(lop)
    f_tre = ImageFont.truetype(FONT_DAM, 150)
    f_phu = ImageFont.truetype(FONT, 34)
    bong = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(bong)
    db.text((TH_X + 4, TH_Y_TRE + 4), "Tre", font=f_tre, fill=(0, 0, 0, 150))
    db.text((TH_X + 6, TH_Y_TRE + 192), "Hệ điều hành học tập", font=f_phu, fill=(0, 0, 0, 200))
    im.alpha_composite(bong.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(im)
    d.text((TH_X, TH_Y_TRE), "Tre", font=f_tre, fill=(255, 255, 255, 255))
    d.line([(TH_X + 6, TH_Y_TRE + 178), (TH_X + 116, TH_Y_TRE + 178)], fill=(120, 200, 80, 255), width=5)
    d.text((TH_X + 4, TH_Y_TRE + 190), "Hệ điều hành học tập", font=f_phu, fill=(255, 255, 255, 255))
    return im.convert("RGB")


def nen_mo(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2 if h < 90 else 26, fill=(10, 25, 15, 125))
    return im


# ------------------------------------------------- video xem trước (mô phỏng)
def mo_phong(thu_muc, che_do, ra, giay=7, fps=25):
    """Mô phỏng đúng cách theme Plymouth vẽ (cùng công thức với tre.script)."""
    p = lambda n: Image.open(os.path.join(thu_muc, n)).convert("RGBA")
    sang = che_do == "boot"
    bg0 = p("nen-khoi-dong.png" if sang else "nen-tat-may.png")
    tl = 1.0 if sang else 1.08
    bg = bg0.resize((int(W * tl), int(H * tl)), Image.LANCZOS)
    co = [p("co-trang-1.png"), p("co-trang-2.png")] if sang else [p("co-toi-1.png"), p("co-toi-2.png")]
    rong, day = p("dot-rong.png"), p("dot-day.png")
    txt = p("chu-khoi-dong.png" if sang else "chu-tat-may.png")
    den = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    dan_co = [(0.0, 0.18, 1.0), (0.12, 0.22, 0.8), (0.25, 0.15, 0.9), (0.33, 0.25, 0.7)]
    tmp = tempfile.mkdtemp()
    n = giay * fps
    for k in range(n):
        t = k / fps
        f = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        # nền trượt chậm (sáng: sang trái; chiều: sang phải)
        u = min(1.0, t / giay)
        dx = (bg.width - W) * (1 - u)
        dy = (bg.height - H) / 2
        layer = bg.copy()
        layer.putalpha(int(255 * min(1.0, t / 0.8)))
        f.alpha_composite(layer, (int(-dx), int(-dy)))
        # đàn cò bay ngang trời
        for (tre, yy, toc) in dan_co:
            x = (-80 + (t - tre * 4) * 170 * toc) if sang else (W + 80 - (t - tre * 4) * 170 * toc)
            if -100 < x < W + 100:
                y = H * yy + math.sin(t * 2 + tre * 10) * 8
                hinh = co[int(t * 5 + tre * 7) % 2]
                if not sang:
                    hinh = hinh.transpose(Image.FLIP_LEFT_RIGHT)
                f.alpha_composite(hinh, (int(x), int(y)))
        # chữ
        a = min(1.0, max(0.0, (t - 0.6) / 0.8))
        tt = txt.copy(); tt.putalpha(tt.getchannel("A").point(lambda v: int(v * a)))
        if sang:
            # thanh tiến trình đốt tre
            tien = min(1.0, t / (giay - 1))
            x0, y0 = TH_X + 6, TH_Y_THANH
            for i in range(SO_DOT):
                f.alpha_composite(day if (i + 1) / SO_DOT <= tien + 1e-6 else rong, (x0 + i * (DOT_W + KHE), y0))
            f.alpha_composite(tt, (x0 - 16, y0 + 18))
        else:
            pill = p("nen-chu-tat.png")
            f.alpha_composite(pill, ((W - pill.width) // 2, int(H * 0.82) - 4))
            f.alpha_composite(tt, ((W - tt.width) // 2, int(H * 0.82)))
            # tối dần ở cuối
            toi = max(0.0, (t - (giay - 2.5)) / 2.5)
            if toi > 0:
                d2 = den.copy(); d2.putalpha(int(255 * min(1, toi)))
                f.alpha_composite(d2)
        f.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(tmp, f"{k:04d}.jpg"), quality=90)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "%04d.jpg"),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", ra], check=True)


if __name__ == "__main__":
    GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) >= 4:
        anh_sang, anh_chieu, theme = sys.argv[1:4]
    else:
        anh_sang = os.path.join(GOC, "tai-nguyen", "anh-goc", "hoc-sinh-den-truong.png")
        anh_chieu = os.path.join(GOC, "tai-nguyen", "anh-goc", "tan-hoc-hoang-hon.png")
        theme = os.path.join(GOC, "goi-tre", "usr", "share", "plymouth", "themes", "tre")
    tao_tai_nguyen(anh_sang, anh_chieu, theme)
    if len(sys.argv) > 4:
        os.makedirs(sys.argv[4], exist_ok=True)
        mo_phong(theme, "boot", os.path.join(sys.argv[4], "xem-truoc-bat-may.mp4"))
        mo_phong(theme, "shutdown", os.path.join(sys.argv[4], "xem-truoc-tat-may.mp4"))
    print("Xong:", theme)
