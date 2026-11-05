# Ghi chú giấy phép của dự án Tre

> Ghi chú này không phải tư vấn pháp lý. Khi phát hành rộng cho nhiều trường, nên nhờ người có chuyên môn xem lại.

## 1. Khi nào phải công khai mã nguồn?

Giấy phép GPL ràng buộc khi **phân phối** phần mềm cho người khác.

| Tình huống | Nghĩa vụ |
|---|---|
| Chỉ cài trong phòng máy của trường mình | Chưa phải công khai (vẫn nên lưu cấu hình lên GitHub để sao lưu) |
| Chia sẻ file ISO cho trường khác, đăng lên mạng | **Phải** cung cấp mã nguồn kèm theo |

## 2. Những gì phải công khai khi phát hành

| Thành phần | Giấy phép | Việc cần làm |
|---|---|---|
| Nhân Linux, công cụ hệ thống, phần lớn gói Debian | GPL | Đăng **ISO mã nguồn** (`sudo ./build.sh --nguon`) cùng chỗ với ISO cài đặt |
| Firefox ESR | MPL 2.0 | Dùng nguyên bản của Debian nên giữ được tên. **Nếu sửa** Firefox thì phải đổi tên, logo và công khai phần sửa |
| LibreOffice | MPL 2.0 | Dùng nguyên bản, không phải làm thêm |
| Kịch bản dựng, gói `tre-he-thong`, lệnh `tre-quan-ly` (do dự án Tre viết) | **GPL-3.0** (file `LICENSE`) | Đăng toàn bộ thư mục này lên GitHub |
| Kho cập nhật (GitHub Pages) | — | Chỉ chứa gói `tre-he-thong` của Tre; phần mềm Debian vẫn tải từ kho Debian chính thức |
| Logo Tre | **CC BY-SA 4.0** | Ghi rõ trong README; người khác dùng lại phải ghi nguồn |
| Ảnh hình nền, màn hình bật/tắt máy (`tai-nguyen/anh-goc/`) | Thầy Nam tạo bằng công cụ AI | Kiểm tra điều khoản của công cụ AI đã dùng trước khi phát hành rộng |
| Phần mềm riêng của trường (Quản Lý Phòng Máy...) | Tác giả tự chọn | **Không bắt buộc** công khai, miễn là không chép mã GPL vào |
| TurboWarp (Scratch 3) nếu thêm vào | GPL-3.0 | Ghi đường dẫn tới mã nguồn của TurboWarp trong README |

## 3. Công khai ở đâu

- **GitHub** (miễn phí): kho `tre` chứa toàn bộ thư mục này.
- **GitHub Releases** hoặc **SourceForge** (miễn phí, chứa file lớn): đăng **2 file song song**
  - `tre-1.0-amd64.hybrid.iso` — bản cài đặt
  - `tre-1.0-source.*` — bản mã nguồn do `--nguon` tạo ra

## 4. Bài học từ các dự án trước

Vietkey Linux (2002) từng bị cộng đồng phê phán vì chậm công bố mã nguồn các thành phần GPL.
Tre công khai ngay từ đầu để tránh điều này.
