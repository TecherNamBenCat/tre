#!/usr/bin/env python3
"""Tre — tạo bộ hình nền 1920x1080 từ ảnh trong tai-nguyen/hinh-nen-goc/.

- Ảnh ngang: phóng vừa khung rồi cắt giữa.
- Ảnh dọc (chụp điện thoại): giữ NGUYÊN ảnh ở giữa, hai bên là chính ảnh đó phóng to, làm mờ
  và tối đi -> không mất nội dung như khi cắt.
Kết quả: goi-tre/usr/share/backgrounds/tre/<tên>.jpg

Thêm hình nền mới: chép ảnh vào tai-nguyen/hinh-nen-goc/ (đặt tên không dấu, có gạch ngang),
chạy lại script này rồi đưa lên GitHub -> các máy tự nhận.
Chạy:  python3 cong-cu/tao-bo-hinh-nen.py
"""
import os

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

W, H = 1920, 1080
GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAO = os.path.join(GOC, "tai-nguyen", "hinh-nen-goc")
RA = os.path.join(GOC, "goi-tre", "usr", "share", "backgrounds", "tre")


def phu_kin(im, w, h):
    tl = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * tl), round(im.height * tl)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def lam(duong_dan):
    im = ImageOps.exif_transpose(Image.open(duong_dan)).convert("RGB")
    if im.width / im.height >= 1.3:          # ảnh ngang
        ra = phu_kin(im, W, H)
    else:                                     # ảnh dọc / vuông
        nen = phu_kin(im, W, H).filter(ImageFilter.GaussianBlur(40))
        nen = ImageEnhance.Brightness(nen).enhance(0.55)
        tl = H / im.height
        giua = im.resize((round(im.width * tl), H), Image.LANCZOS)
        nen.paste(giua, ((W - giua.width) // 2, 0))
        ra = nen
    return ra.filter(ImageFilter.UnsharpMask(radius=1.2, percent=50, threshold=2))


def main():
    os.makedirs(RA, exist_ok=True)
    for ten in sorted(os.listdir(VAO)):
        if not ten.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        ra = os.path.join(RA, os.path.splitext(ten)[0] + ".jpg")
        lam(os.path.join(VAO, ten)).save(ra, quality=88, optimize=True, progressive=True)
        print("  ", os.path.basename(ra))


if __name__ == "__main__":
    main()
