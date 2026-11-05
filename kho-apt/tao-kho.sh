#!/bin/bash
# =============================================================
#  Tre — tạo kho cập nhật APT (có chữ ký) từ các file .deb
#  Dùng:  TRE_KHOA_KY="<khoá bí mật dạng ASCII>" kho-apt/tao-kho.sh <thư-mục-ra> file1.deb [file2.deb ...]
#  Kết quả: <thư-mục-ra>/apt/{dists,pool}  -> đưa lên GitHub Pages
# =============================================================
set -euo pipefail
mkdir -p "$1"; RA="$(cd "$1" && pwd)"; shift
KHO="$RA/apt"
PHIEN_BAN="$(dpkg-deb -f "$1" Version)"
SUITE=trixie

rm -rf "$KHO"
mkdir -p "$KHO/pool/main/t/tre-he-thong" "$KHO/dists/$SUITE/main/binary-amd64"
cp "$@" "$KHO/pool/main/t/tre-he-thong/"

cd "$KHO"
apt-ftparchive packages pool > "dists/$SUITE/main/binary-amd64/Packages"
gzip -9k "dists/$SUITE/main/binary-amd64/Packages"
apt-ftparchive \
    -o APT::FTPArchive::Release::Origin=Tre \
    -o APT::FTPArchive::Release::Label=Tre \
    -o APT::FTPArchive::Release::Suite=$SUITE \
    -o APT::FTPArchive::Release::Codename=$SUITE \
    -o APT::FTPArchive::Release::Architectures="amd64 all" \
    -o APT::FTPArchive::Release::Components=main \
    -o APT::FTPArchive::Release::Description="Kho cap nhat cua Tre" \
    release "dists/$SUITE" > "$RA/Release.tam"
mv "$RA/Release.tam" "dists/$SUITE/Release"

# Ký kho bằng khoá bí mật (lấy từ GitHub Secret TRE_KHOA_KY)
GNUPGHOME="$(mktemp -d)"; export GNUPGHOME
trap 'rm -rf "$GNUPGHOME"' EXIT
if [[ -z "${TRE_KHOA_KY:-}" ]]; then
    echo "Thiếu khoá ký (biến TRE_KHOA_KY)." >&2; exit 1
fi
printf '%s\n' "$TRE_KHOA_KY" | gpg --batch --quiet --import
gpg --batch --yes --clearsign -o "dists/$SUITE/InRelease" "dists/$SUITE/Release"
gpg --batch --yes -abs -o "dists/$SUITE/Release.gpg" "dists/$SUITE/Release"

# Trang giới thiệu nhỏ
cat > "$RA/index.html" <<HTML
<!doctype html><meta charset="utf-8"><title>Tre - kho cập nhật</title>
<h1>Tre — Hệ điều hành học tập</h1>
<p>Đây là kho cập nhật tự động của Tre. Các máy cài Tre tự lấy bản mới từ đây.</p>
<p>Phiên bản hiện tại: $PHIEN_BAN</p>
HTML
echo ">> Đã tạo kho cập nhật trong $KHO"
