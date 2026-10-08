import os
import sys
import time
import socket
import json
import queue
import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Đặt thư mục làm việc về thư mục chứa script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

VENV_PYTHON = os.path.join(SCRIPT_DIR, "venv", "Scripts", "python.exe")
if not os.path.exists(VENV_PYTHON):
    VENV_PYTHON = sys.executable

CONFIG_FILE = os.path.join(SCRIPT_DIR, "robots_config.json")
PORT = 8080

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def load_robots():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

class UnitreeLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unitree Go2 Robot Controller - Swarm Center")
        self.root.geometry("820x620")
        self.root.minsize(700, 500)
        self.root.configure(bg="#0f172a")

        self.server_process = None
        self.is_running = False
        self.lan_ip = get_lan_ip()
        self.log_queue = queue.Queue()

        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Định kỳ xử lý hàng đợi log từ luồng phụ
        self.process_log_queue()

        # Tự động khởi động server và mở web khi bật app
        self.root.after(300, self.start_server_auto)

    def setup_ui(self):
        # Header Frame
        header = tk.Frame(self.root, bg="#1e293b", padx=16, pady=12)
        header.pack(fill=tk.X)

        title_box = tk.Frame(header, bg="#1e293b")
        title_box.pack(side=tk.LEFT)

        title_lbl = tk.Label(
            title_box,
            text="🐕 UNITREE GO2 SWARM CONTROLLER",
            font=("Segoe UI", 14, "bold"),
            fg="#38bdf8",
            bg="#1e293b"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            title_box,
            text=f"Địa chỉ Web: http://localhost:{PORT}  |  Mạng LAN: http://{self.lan_ip}:{PORT}",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        sub_lbl.pack(anchor="w")

        # Status Badge
        self.status_badge = tk.Label(
            header,
            text="● ĐANG KHỞI TẠO",
            font=("Segoe UI", 10, "bold"),
            fg="#eab308",
            bg="#334155",
            padx=12,
            pady=6,
            relief=tk.FLAT
        )
        self.status_badge.pack(side=tk.RIGHT)

        # Robot List Bar
        robots = load_robots()
        robot_summary = " | ".join([f"🤖 {r.get('name', 'Robot')}: {r.get('ip', 'N/A')}" for r in robots]) or "Chưa có robot trong cấu hình"
        
        info_bar = tk.Frame(self.root, bg="#0f172a", padx=16, pady=6)
        info_bar.pack(fill=tk.X)

        tk.Label(
            info_bar,
            text=f"Đội robot: {robot_summary}",
            font=("Segoe UI", 9, "italic"),
            fg="#cbd5e1",
            bg="#0f172a"
        ).pack(side=tk.LEFT)

        # Control Buttons Bar
        btn_bar = tk.Frame(self.root, bg="#1e293b", padx=14, pady=8)
        btn_bar.pack(fill=tk.X, pady=(2, 6))

        # Nút Mở Web (To nhất, nổi bật nhất)
        self.btn_web = tk.Button(
            btn_bar,
            text="🌐 MỞ TRÌNH DUYỆT ĐIỀU KHIỂN",
            font=("Segoe UI", 10, "bold"),
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.open_browser
        )
        self.btn_web.pack(side=tk.LEFT, padx=(0, 8))

        # Nút Khởi động lại
        self.btn_restart = tk.Button(
            btn_bar,
            text="🔄 Khởi động lại",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#f1f5f9",
            activebackground="#475569",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.restart_server
        )
        self.btn_restart.pack(side=tk.LEFT, padx=(0, 6))

        # Nút Dừng
        self.btn_stop = tk.Button(
            btn_bar,
            text="⏹️ Dừng Server",
            font=("Segoe UI", 9, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.stop_server
        )
        self.btn_stop.pack(side=tk.LEFT, padx=(0, 6))

        # Nút Cấu hình
        btn_cfg = tk.Button(
            btn_bar,
            text="⚙️ Cấu hình Robot",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#cbd5e1",
            activebackground="#475569",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.edit_config
        )
        btn_cfg.pack(side=tk.LEFT, padx=(0, 6))

        # Nút Xóa Log
        btn_clear = tk.Button(
            btn_bar,
            text="🧹 Xóa Log",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#94a3b8",
            activebackground="#475569",
            relief=tk.FLAT,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self.clear_logs
        )
        btn_clear.pack(side=tk.RIGHT)

        # Log View Header
        log_head = tk.Frame(self.root, bg="#0f172a", padx=16, pady=2)
        log_head.pack(fill=tk.X)
        tk.Label(
            log_head,
            text="NHẬT KÝ HOẠT ĐỘNG (REALTIME LOG):",
            font=("Segoe UI", 8, "bold"),
            fg="#64748b",
            bg="#0f172a"
        ).pack(side=tk.LEFT)

        # Scrolled Text for Log
        log_frame = tk.Frame(self.root, bg="#0f172a", padx=16, pady=8)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            bg="#020617",
            fg="#e2e8f0",
            insertbackground="#38bdf8",
            font=("Consolas", 9),
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.tag_config("info", foreground="#38bdf8")
        self.log_area.tag_config("success", foreground="#4ade80")
        self.log_area.tag_config("warn", foreground="#facc15")
        self.log_area.tag_config("error", foreground="#f87171")

    def append_log(self, text, tag=None):
        self.log_area.insert(tk.END, text, tag)
        self.log_area.see(tk.END)

    def process_log_queue(self):
        try:
            while True:
                item = self.log_queue.get_nowait()
                if item == "__SERVER_STOPPED__":
                    self.on_server_stopped()
                else:
                    line, tag = item
                    self.append_log(line, tag)
        except queue.Empty:
            pass
        self.root.after(50, self.process_log_queue)

    def set_status(self, text, fg_color, bg_color):
        self.status_badge.config(text=text, fg=fg_color, bg=bg_color)

    def start_server_auto(self):
        self.start_server(open_browser_after=True)

    def start_server(self, open_browser_after=False):
        if self.is_running:
            return

        # Kiểm tra xem cổng 8080 đã có tiến trình nào chạy chưa
        if is_port_open(PORT):
            self.is_running = True
            self.set_status("● SERVER ĐANG CHẠY", "#4ade80", "#052e16")
            self.append_log(f"[{time.strftime('%H:%M:%S')}] Cổng {PORT} đã có Server đang hoạt động sẵn sàng.\n", "success")
            self.btn_stop.config(state=tk.NORMAL)
            if open_browser_after:
                self.root.after(500, self.open_browser)
            return

        self.append_log(f"[{time.strftime('%H:%M:%S')}] Đang khởi động Unitree Go Web Server...\n", "info")
        self.set_status("● ĐANG KHỞI ĐỘNG...", "#facc15", "#422006")

        try:
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            cmd = [VENV_PYTHON, "-u", "app.py"]
            self.server_process = subprocess.Popen(
                cmd,
                cwd=SCRIPT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                creationflags=creationflags
            )

            self.is_running = True
            self.set_status("● SERVER ĐANG CHẠY", "#4ade80", "#052e16")
            self.btn_stop.config(state=tk.NORMAL)

            # Khởi tạo luồng đọc stdout an toàn qua queue
            t = threading.Thread(target=self.read_server_output, daemon=True)
            t.start()

            if open_browser_after:
                # Đợi server lên cổng rồi mở trình duyệt
                self.root.after(1500, self.wait_and_open_browser)

        except Exception as e:
            self.is_running = False
            self.set_status("● LỖI KHỞI ĐỘNG", "#f87171", "#450a0a")
            self.append_log(f"Lỗi khởi động: {e}\n", "error")
            messagebox.showerror("Lỗi", f"Không thể khởi động server: {e}")

    def wait_and_open_browser(self):
        self.open_browser()

    def read_server_output(self):
        proc = self.server_process
        if not proc or not proc.stdout:
            return

        for line in iter(proc.stdout.readline, ''):
            if not line:
                break
            tag = None
            lower_line = line.lower()
            if "error" in lower_line or "exception" in lower_line or "fail" in lower_line:
                tag = "error"
            elif "warning" in lower_line:
                tag = "warn"
            elif "ket noi" in lower_line or "started" in lower_line or "http" in lower_line or "complete" in lower_line:
                tag = "success"
            self.log_queue.put((line, tag))

        proc.stdout.close()
        proc.wait()
        self.log_queue.put("__SERVER_STOPPED__")

    def on_server_stopped(self):
        self.is_running = False
        self.set_status("● SERVER ĐÃ DỪNG", "#f87171", "#450a0a")
        self.append_log(f"[{time.strftime('%H:%M:%S')}] Server đã dừng.\n", "warn")
        self.btn_stop.config(state=tk.DISABLED)

    def stop_server(self):
        if self.server_process and self.is_running:
            self.append_log(f"[{time.strftime('%H:%M:%S')}] Đang dừng server...\n", "warn")
            try:
                self.server_process.terminate()
                self.root.after(1000, self.force_kill_if_needed)
            except Exception as e:
                self.append_log(f"Lỗi khi dừng server: {e}\n", "error")
        else:
            self.on_server_stopped()

    def force_kill_if_needed(self):
        if self.server_process:
            try:
                self.server_process.kill()
            except Exception:
                pass
        self.is_running = False
        self.on_server_stopped()

    def restart_server(self):
        self.stop_server()
        self.root.after(1200, lambda: self.start_server(open_browser_after=False))

    def open_browser(self):
        url = f"http://localhost:{PORT}"
        self.append_log(f"[{time.strftime('%H:%M:%S')}] Đang mở trình duyệt: {url}\n", "info")
        webbrowser.open(url)

    def edit_config(self):
        if os.path.exists(CONFIG_FILE):
            if sys.platform == "win32":
                os.startfile(CONFIG_FILE)
            else:
                subprocess.Popen(["xdg-open", CONFIG_FILE])
        else:
            messagebox.showinfo("Thông báo", f"Không tìm thấy file {CONFIG_FILE}")

    def clear_logs(self):
        self.log_area.delete("1.0", tk.END)

    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno("Thoát", "Bạn có muốn dừng Server và thoát ứng dụng không?"):
                self.stop_server()
                self.root.after(300, self.root.destroy)
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitreeLauncherApp(root)
    root.mainloop()
