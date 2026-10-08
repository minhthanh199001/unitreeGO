# 📦 HƯỚNG DẪN ĐÓNG GÓI, CÀI ĐẶT MÁY TÍNH MỚI & QUẢN LÝ TÀI KHOẢN KHÁCH HÀNG
### LEHOANG ROBOTICS - UNITREE GO2 SWARM CONTROLLER

Tài liệu này hướng dẫn bạn cách chuyển giao toàn bộ mã nguồn sang bất kỳ máy tính nào khác hoặc khi khách hàng sử dụng tài khoản Unitree App / Robot Go2 khác.

---

## PHẦN 1: CÀI ĐẶT LÊN MÁY TÍNH MỚI (CHỈ VỚI 1 CLICK)

### Yêu cầu trước khi cài:
- Máy tính chạy **Windows 10 hoặc Windows 11**.
- Đã cài đặt **Python 3.10 trở lên** (Khuyên dùng Python 3.11 hoặc 3.12).
- *Lưu ý quan trọng khi cài Python:* Hãy tích chọn vào ô **"Add python.exe to PATH"**.

### Các bước cài đặt:
1. Copy toàn bộ thư mục `unitree_sdk2_python-master` sang máy tính mới (qua USB, nén ZIP hoặc tải từ GitHub: `https://github.com/minhthanh199001/unitreeGO`).
2. Nhấp đúp chuột vào file:
   ```cmd
   1_CAI_DAT_MAY_MOI.bat
   ```
3. Hệ thống sẽ tự động thực hiện 100%:
   - Tạo môi trường ảo độc lập `venv`.
   - Cài đặt đầy đủ các thư viện phụ thuộc (`requirements.txt`).
   - Cài đặt gói SDK điều khiển Unitree (`unitree_sdk2py`).
   - Tự động sinh chứng chỉ bảo mật HTTPS (`cert.pem`, `key.pem`) theo IP mạng của máy tính mới.
4. Khi màn hình báo `✅ CÀI ĐẶT HOÀN TẤT 100%!`, bạn đã sẵn sàng sử dụng.

---

## PHẦN 2: KHỞI CHẠY ĐIỀU KHIỂN

Hàng ngày, để sử dụng bạn chỉ cần nhấp đúp chuột vào file:
```cmd
2_CHAY_ROBOT.bat
```
- Máy chủ HTTPS sẽ tự động chạy tại cổng `8080`.
- Trình duyệt web sẽ tự động mở trang điều khiển: `https://localhost:8080`.
- Trên điện thoại (cùng mạng Wi-Fi), bạn mở trình duyệt và truy cập: `https://[IP_MAY_TINH]:8080` (hoặc cài đặt PWA ra màn hình chính).

---

## PHẦN 3: KHI KHÁCH HÀNG DÙNG TÀI KHOẢN UNITREE KHÁC HOẶC ĐỔI ROBOT

Robot Unitree Go2 Pro yêu cầu một **mã khóa bảo mật (AES-128 Key)** để xác thực kết nối WebRTC. Khi khách hàng dùng tài khoản mới hoặc robot mới, họ không cần phải biết kỹ thuật hay tự mò mẫm mã khóa này, hệ thống đã hỗ trợ **2 cách tự động 100%**:

### CÁCH 1: Lấy trực tiếp trên Giao diện Web (Khuyên dùng - Rất tiện lợi)
1. Trên giao diện Web, bấm vào nút **⚙️ QUẢN LÝ ĐỘI ROBOT** ở góc trên bên phải.
2. Chọn tab: **☁️ TÀI KHOẢN UNITREE APP (TỰ LẤY KEY CHO KHÁCH)**.
3. Nhập:
   - **Email** tài khoản Unitree App của khách.
   - **Mật khẩu** tài khoản Unitree App của khách.
   - Chọn máy chủ: *Quốc tế / Việt Nam (Global)*.
4. Bấm **🔍 ĐĂNG NHẬP & TÌM ROBOT**.
5. Hệ thống sẽ kết nối trực tiếp đến máy chủ Unitree Cloud, hiển thị toàn bộ robot của khách, số Serial Number và **TỰ ĐỘNG LẤY MÃ KHÓA AES KEY CHÍNH XÁC 100%**.
6. Khách hàng chỉ cần nhập địa chỉ IP Wi-Fi của robot (VD: `192.168.0.41`) rồi bấm **+ THÊM ROBOT NÀY**. Robot sẽ ngay lập tức được kết nối và đèn chuyển xanh lá!

### CÁCH 2: Dùng công cụ độc lập chạy trên máy tính
1. Nhấp đúp chuột vào file:
   ```cmd
   3_LAY_KEY_TAI_KHOAN_MOI.bat
   ```
2. Cửa sổ màu vàng sẽ hiện lên, yêu cầu nhập Email và Mật khẩu App Unitree của khách.
3. Công cụ sẽ in ra chi tiết danh sách robot và hỏi: *"Bạn có muốn lưu vào cấu hình robots_config.json không?"*.
4. Gõ `Y`, nhập IP Wi-Fi của robot là hệ thống tự động ghi nhớ và lưu trữ vĩnh viễn.

---

## PHẦN 4: DANH MỤC CÁC TẬP TIN TRONG GÓI SẢN PHẨM

| Tên tập tin / Thư mục | Chức năng |
| :--- | :--- |
| `1_CAI_DAT_MAY_MOI.bat` | File cài đặt 1-click cho máy tính mới |
| `2_CHAY_ROBOT.bat` | File khởi động 1-click mở giao diện điều khiển |
| `3_LAY_KEY_TAI_KHOAN_MOI.bat` | File công cụ đăng nhập lấy mã khóa robot từ tài khoản khách |
| `requirements.txt` | Danh sách toàn bộ thư viện Python cần thiết |
| `robots_config.json` | File cấu hình lưu danh sách robot, IP và mã khóa bảo mật |
| `app.py` | Backend máy chủ HTTPS, WebRTC và điều khiển Swarm |
| `lay_key_robot.py` | Script xử lý kết nối đám mây Unitree Cloud |
| `generate_cert.py` | Script tự động tạo chứng chỉ bảo mật SSL HTTPS nội bộ |
| `www/` | Giao diện điều khiển Web & App tối giản 1 màn hình |
| `backup_stable_dual_robot/` | Thư mục sao lưu toàn diện dự phòng ngoại tuyến |
