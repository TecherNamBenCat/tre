# Tre 1.0 "Măng" — Hệ điều hành học tập

**Tre** là hệ điều hành miễn phí dành cho phòng máy Tin học THCS, xây dựng trên nền Debian 13 (Linux).
Giai đoạn 1 chỉ phục vụ giảng dạy, không thương mại; ưu tiên **ổn định** và **chạy tốt trên máy cấu hình thấp** (RAM 2GB, chip Pentium/Celeron G).

Người khởi xướng: Thầy Trần Huỳnh Nhựt Nam — Trường THCS Lê Quý Đôn, Phường Bến Cát, TP. Hồ Chí Minh.

---

## 1. Tre có gì

| Nhóm | Phần mềm |
|---|---|
| Giao diện | XFCE nhẹ, một thanh tác vụ ở dưới, nút "Tre" giống nút Start |
| Tiếng Việt | Giao diện tiếng Việt, bộ gõ **Bamboo** (Telex), bấm `Ctrl + Space` để bật/tắt |
| Internet | Firefox (tiếng Việt) |
| Văn phòng | LibreOffice: soạn thảo, bảng tính, trình chiếu; font tương thích Word (Carlito, Caladea, Liberation) |
| Lập trình | Python + Thonny |
| Học tập | Freeplane (sơ đồ tư duy), Klavaro (luyện gõ phím), GCompris (trò chơi học tập) |
| Phòng máy | Tài khoản **hocsinh** không mật khẩu, không có quyền quản trị, **tự khôi phục mỗi lần khởi động** |
| Bản sắc | Màn hình động: bật máy *học sinh đến trường*, tắt máy *tan trường về*; hình nền đồng quê |
| Cập nhật | **Tự động mỗi ngày** như Windows Update — không cần cài lại |

**Scratch** chưa có sẵn trong kho Debian 13. Xem mục 5 để thêm Scratch 3 (TurboWarp).

---

## 2. Chuẩn bị máy để dựng ISO

Cần **một máy chạy Debian 13 "trixie"**. Thầy đang dùng Windows thì cách dễ nhất:

1. Cài **VirtualBox** (miễn phí) trên máy Windows.
2. Tải bản cài Debian 13 tại debian.org, tạo máy ảo: RAM ≥ 4GB, ổ cứng ≥ **40GB**.
3. Cài Debian vào máy ảo (chọn giao diện bất kỳ hoặc không cần giao diện).
4. Chép thư mục `tre` này vào máy ảo.

Máy dựng cần **Internet** (tải khoảng 2–3GB gói phần mềm).

## 3. Dựng file ISO

Mở Terminal trong thư mục `tre`:

```bash
chmod +x build.sh
sudo ./build.sh
```

Đợi 30–90 phút. Kết quả nằm trong thư mục `ket-qua/`:
- `tre-1.0-amd64.hybrid.iso` — file cài đặt
- `nhat-ky-dung.log` — nhật ký (gửi file này nếu cần nhờ sửa lỗi)

Khi phát hành cho trường khác, dựng kèm ISO mã nguồn (bắt buộc theo giấy phép GPL):

```bash
sudo ./build.sh --nguon
```

## 4. Thử và cài đặt

1. **Thử trên máy ảo trước**: tạo máy ảo mới RAM 2GB, gắn file ISO, khởi động → chọn "Live".
2. **Ghi ra USB**: trên Windows dùng **Rufus** hoặc **balenaEtcher**, chọn file ISO, chế độ DD/Image.
3. **Cài lên máy thật**: khởi động từ USB → biểu tượng "Install" trên màn hình → làm theo hướng dẫn.
   Tài khoản tạo lúc cài đặt là **tài khoản giáo viên/quản trị** (có quyền sudo).

> Nên thử trên 2–3 máy trước khi cài cả phòng.

### Tài khoản

| Tài khoản | Mật khẩu | Quyền |
|---|---|---|
| `hocsinh` | **không có** — bật máy là tự vào | Học sinh, **không** cài/xoá được phần mềm |
| Giáo viên (tạo lúc cài đặt) | giáo viên tự đặt | Quản trị |

Giáo viên vào tài khoản của mình: **Đăng xuất** khỏi tài khoản học sinh → chọn tài khoản giáo viên.
Muốn tắt/bật tự đăng nhập: `sudo tre-quan-ly tu-dang-nhap tat` (hoặc `bat`).

### Chế độ tự khôi phục (giống Deep Freeze)

Mỗi lần khởi động, tài khoản `hocsinh` trở về **bản mẫu**. Riêng thư mục **LuuBai** được giữ lại để học sinh lưu bài.

Lệnh dành cho giáo viên (mở Terminal ở tài khoản giáo viên):

| Lệnh | Tác dụng |
|---|---|
| `sudo tre-quan-ly trang-thai` | Xem đang bật hay tắt |
| `sudo tre-quan-ly tat` | Tạm tắt khôi phục |
| `sudo tre-quan-ly bat` | Bật lại |
| `sudo tre-quan-ly luu-mau` | Lấy tài khoản học sinh hiện tại làm bản mẫu |
| `sudo tre-quan-ly xoa-bai` | Xoá thư mục LuuBai (đầu học kỳ) |

**Chỉnh giao diện cho học sinh** (hình nền, lối tắt trên màn hình...):
`tat` → khởi động lại → đăng nhập `hocsinh`, chỉnh sửa → đăng xuất → vào tài khoản giáo viên chạy `luu-mau` → `bat`.

## 5. Cập nhật tự động (giống Windows Update)

**File ISO chỉ dùng để cài máy mới.** Máy đã cài Tre tự cập nhật qua mạng, không cần cài lại.

```
 Sửa trong goi-tre/  ──>  đưa lên GitHub  ──>  GitHub tự đóng gói + ký  ──>  kho cập nhật (GitHub Pages)
                                                                                    │
                       45 máy phòng máy tự kiểm tra 2 lần/ngày, tự tải và cài  <────┘
```

- Máy tự cập nhật **bản vá bảo mật của Debian** và **bản cập nhật của Tre**: hình nền, màn hình bật/tắt máy,
  cấu hình, phần mềm học tập mới (thêm tên phần mềm vào dòng `Depends:` trong `goi-tre/DEBIAN/control.mau`).
- Không tự khởi động lại giữa giờ học. Thay đổi về màn hình bật/tắt máy có hiệu lực từ lần bật máy sau.
- Giáo viên muốn cập nhật ngay: `sudo tre-quan-ly cap-nhat`. Xem phiên bản: `tre-quan-ly phien-ban`.

### Cài đặt kho cập nhật (chỉ làm 1 lần)

1. Tạo kho **công khai** tên `tre` trên GitHub, đưa toàn bộ thư mục này lên.
2. Chạy `./cong-cu/tao-khoa-ky.sh` → tạo khoá công khai (`kho-apt/tre-archive-keyring.gpg`, đưa lên GitHub)
   và khoá bí mật `khoa-bi-mat-tre.asc` (**không** đưa lên GitHub).
3. Trên GitHub: *Settings → Secrets and variables → Actions → New secret*: tên `TRE_KHOA_KY`,
   nội dung là toàn bộ file `khoa-bi-mat-tre.asc`. Sau đó cất file này vào USB riêng.
4. *Settings → Pages → Source*: chọn **GitHub Actions**.
5. Sửa `cau-hinh/kho-cap-nhat.conf`: điền địa chỉ `https://<tài-khoản>.github.io/tre/apt`.
6. Dựng ISO **một lần cuối** (`sudo ./build.sh`) rồi cài cho các máy. Từ đây trở đi chỉ cần đưa thay đổi lên GitHub.

> Mất khoá bí mật thì máy cũ không nhận được cập nhật nữa — hãy giữ cẩn thận.

## 6. Thêm phần mềm ngoài (.deb)

Chép file `.deb` vào thư mục `goi-them/` rồi dựng lại ISO. Xem `goi-them/README.md`.

## 7. Cấu trúc thư mục

```
tre/
├── build.sh                      Dựng file ISO (chỉ cần khi cài máy mới)
├── dong-goi.sh                   Đóng gói goi-tre/ thành tre-he-thong.deb
├── goi-tre/                      TOÀN BỘ phần riêng của Tre (sửa ở đây là máy tự cập nhật)
│   ├── DEBIAN/                   Thông tin gói, danh sách phần mềm (Depends), lệnh cài đặt (postinst)
│   ├── usr/share/tre/            Hình nền, logo, thanh tác vụ, cấu hình
│   ├── usr/share/plymouth/themes/tre/   Màn hình động bật/tắt máy
│   └── usr/sbin/tre-quan-ly      Lệnh quản lý cho giáo viên
├── cau-hinh/
│   ├── package-lists/            Phần mềm nền của ISO (live, bộ cài đặt, XFCE...)
│   └── kho-cap-nhat.conf         Địa chỉ kho cập nhật
├── kho-apt/                      Tạo kho cập nhật có chữ ký + khoá công khai
├── .github/workflows/            GitHub tự đóng gói và phát hành bản cập nhật
├── cong-cu/                      Tạo logo, hình nền, màn hình động; tạo khoá ký
├── tai-nguyen/anh-goc/           Ảnh gốc (do thầy Nam tạo bằng AI)
├── goi-them/                     Gói .deb bổ sung (Scratch/TurboWarp...)
├── GIAY-PHEP.md, LICENSE         Giấy phép
```

## 8. Lộ trình

- [x] Giai đoạn 1a: bộ khung dựng ISO, tiếng Việt, tài khoản học sinh, khôi phục
- [x] Màn hình động bật/tắt máy, hình nền đồng quê, tự vào tài khoản học sinh
- [x] Cập nhật tự động qua mạng (không cần dựng lại ISO)
- [ ] Đưa lên GitHub, dựng ISO bản chính thức, thử trên 2–3 máy phòng máy
- [ ] Ứng dụng học sinh của **Quản Lý Phòng Máy** chạy trên Tre (.NET 8 + Avalonia), phát hành qua kho cập nhật
- [ ] Bộ cài đặt mang thương hiệu Tre, kho ứng dụng theo khối lớp
