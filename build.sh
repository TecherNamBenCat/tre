#!/bin/bash
# =============================================================
#  Tre 1.0 "Măng" — kịch bản dựng file cài đặt ISO
#  Chạy trên máy (hoặc máy ảo) Debian 13 "trixie":
#      sudo ./build.sh            -> tạo ISO cài đặt
#      sudo ./build.sh --nguon    -> tạo thêm ISO mã nguồn (khi phát hành cho trường khác)
# =============================================================
set -euo pipefail

THU_MUC="$(cd "$(dirname "$0")" && pwd)"
CAU_HINH="$THU_MUC/cau-hinh"
GOI_THEM="$THU_MUC/goi-them"
BUILD="$THU_MUC/build"
KET_QUA="$THU_MUC/ket-qua"

TAO_NGUON=false
if [[ "${1:-}" == "--nguon" ]]; then
    TAO_NGUON=true
fi

if [[ $EUID -ne 0 ]]; then
    echo "Hãy chạy bằng quyền quản trị:  sudo ./build.sh"
    exit 1
fi

# shellcheck disable=SC1091
. /etc/os-release
if [[ "${VERSION_CODENAME:-}" != "trixie" ]]; then
    echo "CẢNH BÁO: máy này không phải Debian 13 (trixie). Nên dựng trên Debian 13 để tránh lỗi."
    read -r -p "Vẫn tiếp tục? (c/k) " tl
    [[ "$tl" == "c" ]] || exit 1
fi

if ! command -v lb >/dev/null 2>&1; then
    echo ">> Cài công cụ live-build..."
    apt-get update
    apt-get install -y live-build
fi

echo ">> Chuẩn bị thư mục dựng..."
if [[ -d "$BUILD" ]]; then
    (cd "$BUILD" && lb clean --purge) || true
    rm -rf "$BUILD"
fi
mkdir -p "$BUILD" "$KET_QUA"
cd "$BUILD"

TUY_CHON_NGUON=()
if $TAO_NGUON; then
    TUY_CHON_NGUON=(--source true --source-images iso)
fi

lb config \
    --mode debian \
    --distribution trixie \
    --architectures amd64 \
    --archive-areas "main contrib non-free non-free-firmware" \
    --firmware-chroot true \
    --firmware-binary true \
    --security true \
    --updates true \
    --debian-installer none \
    --image-name "tre-1.0" \
    --iso-application "Tre" \
    --iso-publisher "Tre - He dieu hanh hoc tap" \
    --iso-volume "Tre 1.0" \
    --bootappend-live "boot=live components locales=vi_VN.UTF-8 keyboard-layouts=us timezone=Asia/Ho_Chi_Minh quiet splash" \
    "${TUY_CHON_NGUON[@]}"

echo ">> Chép cấu hình Tre..."
cp -a "$CAU_HINH/package-lists/."   config/package-lists/

# Tự bỏ phần mềm không có trong kho Debian (tránh dừng giữa chừng)
echo ">> Kiểm tra danh sách phần mềm..."
apt-get update -qq || true
for DS in config/package-lists/*.list.chroot; do
    mapfile -t GOI < <(grep -Ev '^[[:space:]]*(#|$)' "$DS")
    for p in "${GOI[@]}"; do
        if ! apt-cache policy "$p" 2>/dev/null | grep -Eq 'Candidate: [0-9]'; then
            echo "   BỎ QUA (không có trong kho): $p"
            sed -i "s/^$p\$/# $p/" "$DS"
        fi
    done
done
# Toàn bộ phần riêng của Tre nằm trong gói tre-he-thong (cũng là gói được cập nhật tự động)
echo ">> Đóng gói tre-he-thong..."
rm -rf "$THU_MUC/dist"
# Phụ thuộc nào của tre-he-thong không có trong kho Debian thì bỏ, tránh dừng giữa chừng
TRE_BO_GOI=""
for p in $(sed -n -E 's/^Depends: //p' "$THU_MUC/goi-tre/DEBIAN/control.mau" | tr -d ' ' | tr ',' ' '); do
    if ! apt-cache policy "$p" 2>/dev/null | grep -Eq 'Candidate: [0-9]'; then
        echo "   BỎ QUA phụ thuộc (không có trong kho): $p"
        TRE_BO_GOI="$TRE_BO_GOI $p"
    fi
done
export TRE_BO_GOI
"$THU_MUC/dong-goi.sh"
mkdir -p config/packages.chroot
cp -a "$THU_MUC"/dist/tre-he-thong_*.deb config/packages.chroot/
echo "tre-he-thong" > config/package-lists/tre-he-thong.list.chroot

# Gói .deb bổ sung (Scratch/TurboWarp, phần mềm riêng của trường...)
shopt -s nullglob
DEB=("$GOI_THEM"/*.deb)
if (( ${#DEB[@]} > 0 )); then
    mkdir -p config/packages.chroot
    cp -a "${DEB[@]}" config/packages.chroot/
    echo ">> Thêm ${#DEB[@]} gói từ thư mục goi-them/"
fi

echo ">> Bắt đầu dựng (mất khoảng 30–90 phút tuỳ tốc độ mạng)..."
lb build 2>&1 | tee "$KET_QUA/nhat-ky-dung.log"

mv -f ./*.iso "$KET_QUA/" 2>/dev/null || true
mv -f ./*.tar "$KET_QUA/" 2>/dev/null || true
echo
echo "== XONG. File nằm trong thư mục: $KET_QUA =="
ls -lh "$KET_QUA"
