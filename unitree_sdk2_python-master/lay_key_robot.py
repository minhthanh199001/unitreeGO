# -*- coding: utf-8 -*-
"""
Công cụ tự động đăng nhập Unitree Cloud và lấy mã bảo mật AES-128 Key
Dành cho khách hàng dùng tài khoản Unitree khác hoặc robot mới.
"""
import sys
import os
import json
import getpass

# Cấu hình UTF-8 cho Windows cmd
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

CONFIG_FILE = "robots_config.json"

def main():
    print("=" * 65)
    print(" 🐕 UNITREE GO2 - CÔNG CỤ TỰ ĐỘNG LẤY MÃ KHÓA BẢO MẬT ROBOT")
    print(" (Dành cho khách hàng sử dụng tài khoản Unitree App khác)")
    print("=" * 65)
    print()

    try:
        from unitree_webrtc_connect import UnitreeCloud
    except ImportError:
        print("❌ Lỗi: Chưa tìm thấy thư viện unitree_webrtc_connect!")
        print("Vui lòng kích hoạt venv hoặc chạy file 1_CAI_DAT_MAY_MOI.bat trước.")
        input("\nNhấn Enter để thoát...")
        return

    email = input("👉 Nhập Email đăng ký tài khoản Unitree App: ").strip()
    if not email:
        print("❌ Email không được để trống!")
        return

    password = getpass.getpass("👉 Nhập Mật khẩu Unitree App (khi gõ sẽ ẩn ký tự): ").strip()
    if not password:
        print("❌ Mật khẩu không được để trống!")
        return

    print("\nChọn khu vực máy chủ Unitree:")
    print("  1. Quốc tế / Việt Nam (Global - Mặc định)")
    print("  2. Nội địa Trung Quốc (China - cn)")
    region_choice = input("Lựa chọn (1 hoặc 2, mặc định 1): ").strip()
    region = "cn" if region_choice == "2" else "global"

    print(f"\n🔄 Đang kết nối tới Unitree Cloud ({region})... Vui lòng đợi trong giây lát...")
    try:
        cloud = UnitreeCloud(region=region, device_type="Go2")
        token = cloud.login_email(email, password)
        print("✅ Đăng nhập tài khoản thành công!")
        
        devices = cloud.list_devices()
        if not devices:
            print("⚠️ Tài khoản đăng nhập thành công nhưng không tìm thấy robot Go2 nào được liên kết!")
            print("Vui lòng kiểm tra xem bạn đã kết nối và liên kết robot trong App Unitree chưa.")
            input("\nNhấn Enter để kết thúc...")
            return

        print(f"\n🎉 Tìm thấy {len(devices)} robot trong tài khoản của bạn:\n")
        print("-" * 65)
        for idx, dev in enumerate(devices, 1):
            alias = dev.alias or f"Go2_{dev.sn[-5:] if len(dev.sn) >= 5 else dev.sn}"
            print(f"[{idx}] Tên Robot : {alias}")
            print(f"    Số Serial : {dev.sn}")
            print(f"    Model     : {dev.model or dev.series or 'Go2'}")
            print(f"    Trạng thái: {'Trực tuyến' if dev.online else 'Ngoại tuyến'}")
            print(f"    🔑 AES Key: {dev.key if dev.key else '(Không yêu cầu mã hoặc bản Legacy)'}")
            print("-" * 65)

        # Hỏi lưu vào cấu hình
        save_choice = input("\n👉 Bạn có muốn thêm robot vào file cấu hình robots_config.json? (Y/n): ").strip().lower()
        if save_choice in ("", "y", "yes"):
            # Đọc config hiện tại
            current_config = []
            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        current_config = json.load(f)
                except Exception:
                    current_config = []

            for dev in devices:
                alias = dev.alias or f"Go2_{dev.sn[-5:] if len(dev.sn) >= 5 else dev.sn}"
                print(f"\n--- Thiết lập địa chỉ IP cho robot: {alias} ---")
                robot_ip = input(f"👉 Nhập địa chỉ IP Wi-Fi của robot {alias} (Ví dụ: 192.168.0.41): ").strip()
                if not robot_ip:
                    robot_ip = "192.168.0.41"
                    print(f"   -> Sử dụng IP mặc định: {robot_ip}")

                fallback_ip = input("👉 Nhập IP điểm phát sóng AP dự phòng (Mặc định: 192.168.12.1): ").strip()
                if not fallback_ip:
                    fallback_ip = "192.168.12.1"

                # Sinh ID duy nhất
                r_id = f"robot_{dev.sn[-5:] if len(dev.sn) >= 5 else idx}"
                
                # Cập nhật hoặc thêm mới
                updated = False
                for existing in current_config:
                    if existing.get("id") == r_id or existing.get("ip") == robot_ip:
                        existing["name"] = alias
                        existing["ip"] = robot_ip
                        existing["key"] = dev.key or None
                        existing["fallback_ip"] = fallback_ip
                        existing["enabled"] = True
                        updated = True
                        break

                if not updated:
                    current_config.append({
                        "id": r_id,
                        "name": alias,
                        "ip": robot_ip,
                        "fallback_ip": fallback_ip,
                        "key": dev.key or None,
                        "enabled": True
                    })

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(current_config, f, indent=2, ensure_ascii=False)

            print(f"\n✅ ĐÃ LƯU THÀNH CÔNG VÀO {CONFIG_FILE}!")
            print("🚀 Bây giờ bạn có thể chạy file 2_CHAY_ROBOT.bat để điều khiển ngay!")

    except Exception as e:
        print(f"\n❌ Lỗi khi đăng nhập hoặc lấy thông tin: {e}")
        print("Vui lòng kiểm tra lại Email, Mật khẩu hoặc kết nối mạng Internet.")

    input("\nNhấn phím Enter để hoàn tất...")

if __name__ == "__main__":
    main()
