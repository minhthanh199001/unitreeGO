# HỆ THỐNG ĐIỀU KHIỂN ROBOT SWARM & FLEET MANAGER (LAN ROUTER)

Tài liệu hướng dẫn quản trị và sử dụng hệ thống điều khiển đội robot Unitree Go2 đa năng. Hệ thống hỗ trợ điều khiển **đồng bộ nhiều robot cùng lúc (N-Robots Swarm)** hoặc **tách riêng từng robot**, dễ dàng thêm bớt robot trực tiếp trên giao diện Web.

---

## 1. Tính Năng Quản Lý Đội Robot (Fleet Management)

Hệ thống cho phép bạn **thêm robot mới vào ứng dụng bất kỳ lúc nào mà không cần sửa code**:

### Cách 1: Thêm trực tiếp trên giao diện Web (Khuyên dùng)
1. Mở trình duyệt vào [http://localhost:8080](http://localhost:8080).
2. Nhấp vào nút **`⚙️ QUẢN LÝ ĐỘI ROBOT`** ở góc trên bên phải.
3. Trong bảng hiện ra:
   - Nhập **Tên gợi nhớ** (VD: `Robot 3`, `Go2 Beta`).
   - Nhập **Địa chỉ IP** trong mạng Wi-Fi (VD: `192.168.0.88`).
   - Nhập **Mã AES Key** (Nếu là Go2 Pro/Air có firmware >= 1.1.15; nếu là Go2 Edu thì bỏ trống).
   - Nhấp nút **`+ LƯU VÀ KẾT NỐI NGAY`**.
4. Robot mới sẽ xuất hiện ngay lập tức trên thanh trạng thái và tự động kết nối nền!

### Cách 2: Cấu hình qua file `robots_config.json`
Bạn cũng có thể mở file [`robots_config.json`](file:///d:/THANH/unitreego/unitree_sdk2_python-master/robots_config.json) và thêm/chỉnh sửa danh sách robot:
```json
[
  {
    "id": "robot1",
    "name": "Robot 1 (Go2_46945)",
    "ip": "192.168.0.41",
    "fallback_ip": "192.168.12.1",
    "key": "d15cda4ffb907236f7e363e77dfab121",
    "enabled": true
  },
  {
    "id": "robot2",
    "name": "Robot 2 (Go2_48462)",
    "ip": "192.168.0.75",
    "fallback_ip": null,
    "key": null,
    "enabled": true
  }
]
```

---

## 2. Cách Khởi Động Nhanh (1 Click)

1. **LƯU Ý:** Tắt ứng dụng Unitree trên điện thoại trước khi chạy để tránh xung đột WebRTC.
2. Nhấp đúp chuột vào file:
   ```text
   CHAY_ROBOT_DONG_BO.bat
   ```
3. Mở trình duyệt web truy cập:
   - Trên máy tính này: [http://localhost:8080](http://localhost:8080)
   - Thiết bị cùng mạng Wi-Fi: [http://192.168.0.153:8080](http://192.168.0.153:8080)

---

## 3. Các Chế Độ Điều Khiển Swarm

- **`🔄 ĐỒNG BỘ TẤT CẢ ROBOT (N Robot)`**: Tất cả các robot đang online trong hệ thống sẽ cùng lúc nhận lệnh di chuyển, thực hiện động tác biểu diễn cùng nhau.
- **`1️⃣, 2️⃣, 3️⃣... CHỈ ROBOT X`**: Chọn riêng từng con robot để ra lệnh độc lập mà không ảnh hưởng đến các robot còn lại.

---

## 4. Các Phím Tắt & Tính Năng Điều Khiển

### 🎮 Di Chuyển (Keyboard / Joystick)
- **`W` / `S`**: Tiến / Lùi
- **`A` / `D`**: Đi ngang Trái / Phải
- **`Q` / `E`**: Xoay Trái / Phải (Yaw)
- **Giữ `Shift`**: Tăng tốc tức thì (**TURBO x1.4**)
- **`Space`**: Dừng phanh khẩn cấp

### 🎭 Động Tác Biểu Diễn & Giọng Nói Tiếng Việt
Bấm nút trên giao diện hoặc bấm vào Mic 🎤 và nói:
- 💃 *"Nhảy múa"*, *"Dance 1"*
- 🕺 *"Nhảy điệu 2"*, *"Dance 2"*
- 🧘 *"Vươn vai"*, *"Giãn cơ"*
- 🤝 *"Bắt tay"*, *"Shake hands"*
- 👋 *"Chào"*, *"Xin chào"*
- 🐅 *"Vồ mồi"*, *"Chồm tới"*
- 🦘 *"Nhảy tới"*, *"Nhảy lên"*
- ❤️ *"Bắn tim"*, *"Thả tim"*
- 🐕 *"Lắc mông"*, *"Lắc hông"*
- 🐾 *"Cào đất"*, *"Bới đất"*
- 🤸 *"Lộn nhào"*
- 🕺 *"Moonwalk"*
