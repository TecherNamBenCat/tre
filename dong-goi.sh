#!/bin/bash
# =============================================================
#  Tre — đóng gói phần riêng của Tre thành file .deb
#  Dùng:  ./dong-goi.sh            -> tạo dist/tre-he-thong_<phiên-bản>_all.deb
#  Phiên bản tự lấy theo ngày giờ (luôn tăng), hoặc đặt TRE_PHIEN_BAN=...
# =============================================================
set -euo pipefail
GOC="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$GOC/cau-hinh/kho-cap-nhat.conf"

PHIEN_BAN="${TRE_PHIEN_BAN:-1.$(date -u +%Y%m%d.%H%M%S)}"
TAM="$(mktemp -d)"
trap 'rm -rf "$TAM"' EXIT
GOI="$TAM/tre-he-thong"

cp -a "$GOC/goi-tre" "$GOI"
sed -e "s|@@PHIEN_BAN@@|$PHIEN_BAN|" -e "s|@@NGUOI_BAO_TRI@@|$NGUOI_BAO_TRI|" \
    "$GOI/DEBIAN/control.mau" > "$GOI/DEBIAN/control"
rm "$GOI/DEBIAN/control.mau"

# Kho cập nhật: chỉ bật khi đã có khoá ký và đã điền địa chỉ kho
KHOA="$GOC/kho-apt/tre-archive-keyring.gpg"
if [[ -f "$KHOA" && "$DIA_CHI_KHO" != *TEN-TAI-KHOAN* ]]; then
    install -Dm644 "$KHOA" "$GOI/usr/share/keyrings/tre-archive-keyring.gpg"
    mkdir -p "$GOI/etc/apt/sources.list.d"
    sed "s|@@DIA_CHI_KHO@@|$DIA_CHI_KHO|" "$GOI/usr/share/tre/tre.sources.mau" \
        > "$GOI/etc/apt/sources.list.d/tre.sources"
    echo ">> Kho cập nhật: $DIA_CHI_KHO"
else
    echo ">> CHÚ Ý: chưa cấu hình kho cập nhật (kho-apt/tre-archive-keyring.gpg hoặc cau-hinh/kho-cap-nhat.conf)."
    echo "   Gói vẫn dùng được, chỉ là máy sẽ chưa tự nhận bản cập nhật của Tre."
fi
rmdir "$GOI/usr/share/keyrings" "$GOI/etc/apt/sources.list.d" 2>/dev/null || true

# Quyền file
find "$GOI" -type d -exec chmod 755 {} +
find "$GOI" -type f -exec chmod 644 {} +
chmod 755 "$GOI"/DEBIAN/postinst "$GOI"/DEBIAN/postrm \
          "$GOI"/usr/bin/* "$GOI"/usr/sbin/* "$GOI"/usr/share/tre/ap-dung-tu-dang-nhap

# Kích thước cài đặt
echo "Installed-Size: $(du -sk --exclude=DEBIAN "$GOI" | cut -f1)" >> "$GOI/DEBIAN/control"

mkdir -p "$GOC/dist"
DEB="$GOC/dist/tre-he-thong_${PHIEN_BAN}_all.deb"
dpkg-deb --root-owner-group -Zxz --build "$GOI" "$DEB" >/dev/null
echo ">> Đã đóng gói: $DEB"
