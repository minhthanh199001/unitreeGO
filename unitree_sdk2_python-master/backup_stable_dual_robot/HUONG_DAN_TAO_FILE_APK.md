# 📱 HƯỚNG DẪN ĐÓNG GÓI APP THÀNH FILE APK CHO ĐIỆN THOẠI ANDROID
### LEHOANG ROBOTICS - UNITREE GO2

Dự án hiện đã được chuẩn bị đầy đủ mã nguồn để bạn có thể xuất ra file `.apk` cài đặt trực tiếp trên bất kỳ điện thoại Android nào. Dưới đây là các cách thực hiện đơn giản nhất:

---

## CÁCH 1: DÙNG MÃ NGUỒN ANDROID NATIVE CÓ SẴN (CHUYÊN NGHIỆP NHẤT)

Mã nguồn ứng dụng Android đã được tạo sẵn trong thư mục:
```text
d:\THANH\unitreego\android_client
```

### Ưu điểm vượt trội của bản Native này:
1. **Khóa màn hình nằm ngang tuyệt đối (Landscape)**: Không bị xoay dọc lung tung khi lắc điện thoại.
2. **Ẩn hoàn toàn thanh điều hướng & thanh trạng thái (Immersive Fullscreen)**: Trải nghiệm như một máy chơi game cầm tay thực thụ.
3. **Triệt tiêu 100% cảnh báo "Không bảo mật"**: Tự động chấp nhận chứng chỉ SSL nội bộ (`handler.proceed()`).
4. **Tự động cấp quyền Micro**: Không phải bấm đồng ý quyền ghi âm mỗi khi ra lệnh giọng nói.
5. **Bộ nhớ lưu IP thông minh**: Lần đầu mở app chỉ cần gõ IP máy tính (VD: `192.168.0.153:8080`), app sẽ tự ghi nhớ cho các lần sau.

### Cách xuất ra file APK:
1. Mở phần mềm **Android Studio** trên máy tính.
2. Chọn **Open** và duyệt tới thư mục `d:\THANH\unitreego\android_client`.
3. Đợi vài giây để dự án tải xong, trên thanh menu chọn:
   ```text
   Build -> Build Bundle(s) / APK(s) -> Build APK(s)
   ```
4. Sau khi build xong (khoảng 30-60 giây), Android Studio sẽ hiện thông báo ở góc dưới:
   ```text
   APK(s) generated successfully: Locate
   ```
5. Bấm vào chữ **Locate**, bạn sẽ nhận được file `app-debug.apk`. Chỉ cần copy file này sang điện thoại và nhấp cài đặt là xong!

---

## CÁCH 2: DÙNG CÔNG CỤ ONLINE PWABUILDER (KHÔNG CẦN CÀI ANDROID STUDIO)

Vì mã nguồn web của chúng ta đã được tích hợp đầy đủ file chuẩn Progressive Web App (`manifest.json` và `sw.js`), bạn có thể dùng công cụ trực tuyến của Microsoft & Google:

1. Đưa ứng dụng web lên mạng hoặc dùng công cụ ngrok / cloudflare tunnel để tạo 1 link https tạm thời.
2. Truy cập trang web: [https://www.pwabuilder.com/](https://www.pwabuilder.com/)
3. Nhập link web của bạn vào ô tìm kiếm -> Nhấn **Start**.
4. Bấm **Package for Android (APK)** -> Nhấn **Generate Package**.
5. Tải file ZIP về, giải nén ra sẽ có ngay file `.apk` cài đặt trực tiếp trên Android mà không cần phải cài bất kỳ phần mềm lập trình nào trên máy tính!

---

## CÁCH 3: CÀI ĐẶT TRỰC TIẾP QUA TRÌNH DUYỆT CHROME (NHANH NHẤT - 10 GIÂY)

Nếu bạn không bắt buộc phải có file cài `.apk` gửi qua Zalo/USB mà chỉ muốn cài lên máy của bạn hoặc của khách ngay lập tức:

1. Trên điện thoại Android, kết nối cùng Wi-Fi với máy tính.
2. Mở trình duyệt **Google Chrome** và truy cập: `https://[IP_MAY_TINH]:8080`.
3. Bấm vào dấu **3 chấm (⋮)** ở góc trên bên phải Chrome.
4. Chọn dòng **"Cài đặt ứng dụng"** (hoặc **"Thêm vào Màn hình chính"**).
5. Android sẽ tự động tạo một ứng dụng độc lập (WebAPK) ra màn hình chính điện thoại với icon Robot Cyber riêng biệt, khi mở lên sẽ tràn viền toàn màn hình y hệt như cài từ file APK!
