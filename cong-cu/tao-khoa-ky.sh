#!/bin/bash
# =============================================================
#  Tre — tạo cặp khoá ký kho cập nhật (CHỈ LÀM 1 LẦN)
#   - kho-apt/tre-archive-keyring.gpg : khoá CÔNG KHAI, đưa vào mọi máy Tre (được commit)
#   - khoa-bi-mat-tre.asc             : khoá BÍ MẬT, dán vào GitHub Secret "TRE_KHOA_KY"
#                                       rồi cất USB/ổ riêng. KHÔNG đưa lên GitHub.
# =============================================================
set -euo pipefail
GOC="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "$GOC/kho-apt/tre-archive-keyring.gpg" ]]; then
    echo "Đã có khoá rồi (kho-apt/tre-archive-keyring.gpg). Không tạo lại để máy cũ vẫn nhận cập nhật."
    exit 1
fi
GNUPGHOME="$(mktemp -d)"; export GNUPGHOME
trap 'rm -rf "$GNUPGHOME"' EXIT
gpg --batch --quiet --passphrase '' --quick-gen-key "Kho cap nhat Tre <tre@example.invalid>" rsa4096 sign never
gpg --batch --export > "$GOC/kho-apt/tre-archive-keyring.gpg"
gpg --batch --armor --export-secret-keys > "$GOC/khoa-bi-mat-tre.asc"
chmod 600 "$GOC/khoa-bi-mat-tre.asc"
echo "Xong:"
echo "  - khoá công khai : kho-apt/tre-archive-keyring.gpg"
echo "  - khoá bí mật    : khoa-bi-mat-tre.asc  (dán vào GitHub Secret TRE_KHOA_KY rồi cất riêng)"
