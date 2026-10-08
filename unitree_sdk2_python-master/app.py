import sys
import os
import time
import math
import random
import socket
import json
import asyncio
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn

# Đảm bảo mã hóa UTF-8 an toàn trên Windows terminal
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from unitree_webrtc_connect import (
    UnitreeWebRTCConnection,
    WebRTCConnectionMethod,
    RTC_TOPIC,
    SPORT_CMD,
    DATA_CHANNEL_TYPE,
)

CONFIG_FILE = "robots_config.json"

DEFAULT_ROBOTS = [
    {
        "id": "robot1",
        "name": "Robot 1 (Go2_46945)",
        "ip": "192.168.0.41",
        "fallback_ip": "192.168.12.1",
        "key": "d15cda4ffb907236f7e363e77dfab121",
        "enabled": True,
    },
    {
        "id": "robot2",
        "name": "Robot 2 (Go2_48462)",
        "ip": "192.168.0.75",
        "fallback_ip": None,
        "key": None,
        "enabled": True,
    },
]

# Quản lý cấu hình danh sách Robot
ROBOTS: Dict[str, Dict[str, Any]] = {}
robot_monitor_tasks: Dict[str, asyncio.Task] = {}

def load_robots_config():
    """Tải danh sách Robot từ file cấu hình JSON"""
    global ROBOTS
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_ROBOTS, f, indent=2, ensure_ascii=False)
        data = DEFAULT_ROBOTS
    else:
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Lỗi đọc {CONFIG_FILE}: {e}. Dùng mặc định.", flush=True)
            data = DEFAULT_ROBOTS

    for item in data:
        r_id = item["id"]
        ROBOTS[r_id] = {
            "id": r_id,
            "name": item.get("name", f"Robot {r_id}"),
            "ip": item["ip"],
            "fallback_ip": item.get("fallback_ip"),
            "key": item.get("key"),
            "enabled": item.get("enabled", True),
            "conn": None,
            "connected": False,
        }

def save_robots_config():
    """Lưu danh sách Robot vào file cấu hình JSON"""
    data = []
    for r in ROBOTS.values():
        data.append({
            "id": r["id"],
            "name": r["name"],
            "ip": r["ip"],
            "fallback_ip": r.get("fallback_ip"),
            "key": r.get("key"),
            "enabled": r.get("enabled", True),
        })
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Khởi tạo danh sách robot ban đầu
load_robots_config()

# Lưu trữ trạng thái điều khiển
state = {
    "mode": "IDLE",  # IDLE, MOVE, POSTURE, ACTION
    "target_robot": "all",  # 'all', 'both' hoặc id cụ thể ('robot1', 'robot2', ...)
    "vx": 0.0,
    "vy": 0.0,
    "vyaw": 0.0,
    "roll": 0.0,
    "pitch": 0.0,
    "yaw": 0.0,
    "last_recv_time": time.time(),
}

active_websockets = set()

def send_to_robot(r_info, api_id, parameter=None):
    """Gửi gói tin tức thì không blocking xuống 1 Robot cụ thể"""
    if not r_info.get("enabled", True):
        return False
    conn = r_info.get("conn")
    if not conn or not getattr(conn, "isConnected", False):
        return False
    try:
        channel = getattr(conn, "datachannel", None)
        if not channel or getattr(channel.channel, "readyState", None) != "open":
            return False

        generated_id = int(time.time() * 1000) % 2147483648 + random.randint(0, 1000)
        request_payload = {
            "header": {
                "identity": {
                    "id": generated_id,
                    "api_id": api_id
                }
            },
            "parameter": ""
        }
        if parameter is not None:
            request_payload["parameter"] = parameter if isinstance(parameter, str) else json.dumps(parameter)

        channel.pub_sub.publish_without_callback(
            RTC_TOPIC["SPORT_MOD"],
            request_payload,
            DATA_CHANNEL_TYPE["REQUEST"]
        )
        return True
    except Exception as e:
        print(f"[{r_info['name']}] Lỗi gửi lệnh api_id {api_id}: {e}", flush=True)
        return False

def broadcast_sport_req(api_id, parameter=None):
    """Gửi lệnh tới các robot theo chế độ được chọn (Tất cả hoặc riêng từng robot)"""
    target = state.get("target_robot", "all")
    sent = False
    for r_id, r_info in ROBOTS.items():
        if not r_info.get("enabled", True):
            continue
        if target in ("all", "both") or target == r_id:
            if send_to_robot(r_info, api_id, parameter):
                sent = True
    return sent

async def control_loop():
    """Vòng lặp gửi lệnh di chuyển liên tục xuống các Robot (chu kỳ 50ms)"""
    while True:
        try:
            if state["mode"] == "MOVE":
                # Watchdog: Nếu không nhận lệnh từ web quá 800ms -> Dừng an toàn
                if time.time() - state.get("last_recv_time", 0) > 0.8:
                    state["vx"] = 0.0
                    state["vy"] = 0.0
                    state["vyaw"] = 0.0
                    state["mode"] = "IDLE"
                    broadcast_sport_req(SPORT_CMD["StopMove"])
                    print("Watchdog: Đã dừng các robot an toàn.", flush=True)
                    continue

                vx = round(float(state["vx"]), 3)
                vy = round(float(state["vyaw"]), 3)
                vyaw = round(float(state["vyaw"]), 3)

                if abs(vx) > 0.005 or abs(state["vy"]) > 0.005 or abs(vyaw) > 0.005:
                    broadcast_sport_req(
                        SPORT_CMD["Move"],
                        parameter={"x": vx, "y": round(float(state["vy"]), 3), "z": vyaw}
                    )
        except Exception as e:
            print(f"Exception trong control_loop: {e}", flush=True)
        await asyncio.sleep(0.05)

async def robot_monitor(robot_id):
    """Tự động kết nối và duy trì kết nối cho từng Robot riêng biệt"""
    idx = 0
    while True:
        try:
            r_info = ROBOTS.get(robot_id)
            if not r_info:
                break
            if not r_info.get("enabled", True):
                if r_info.get("conn"):
                    try:
                        await r_info["conn"].disconnect()
                    except Exception:
                        pass
                    r_info["conn"] = None
                    r_info["connected"] = False
                await asyncio.sleep(2)
                continue

            candidate_ips = [r_info["ip"]]
            if r_info.get("fallback_ip"):
                candidate_ips.append(r_info["fallback_ip"])

            conn = r_info["conn"]
            if conn is None or not getattr(conn, "isConnected", False):
                if conn:
                    try:
                        await conn.disconnect()
                    except Exception:
                        pass
                ip = candidate_ips[idx % len(candidate_ips)]
                method = WebRTCConnectionMethod.LocalAP if ip == "192.168.12.1" else WebRTCConnectionMethod.LocalSTA
                
                new_conn = UnitreeWebRTCConnection(
                    connectionMethod=method,
                    ip=ip,
                    aes_128_key=r_info["key"],
                )
                await new_conn.connect()
                r_info["conn"] = new_conn
                r_info["connected"] = True
                print(f"✅ [{r_info['name']}] ĐÃ KẾT NỐI WEBRTC THÀNH CÔNG ({ip})!", flush=True)
                idx = 0
            else:
                r_info["connected"] = True
        except asyncio.CancelledError:
            print(f"Monitor cho [{robot_id}] đã kết thúc.", flush=True)
            break
        except Exception as e:
            if robot_id in ROBOTS:
                ROBOTS[robot_id]["connected"] = False
            idx += 1
        await asyncio.sleep(2)

def start_robot_task(r_id):
    """Khởi chạy task giám sát kết nối cho một robot"""
    if r_id in robot_monitor_tasks and not robot_monitor_tasks[r_id].done():
        return
    robot_monitor_tasks[r_id] = asyncio.create_task(robot_monitor(r_id))

async def stop_robot_task(r_id):
    """Dừng task giám sát và ngắt kết nối robot"""
    task = robot_monitor_tasks.pop(r_id, None)
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    r_info = ROBOTS.get(r_id)
    if r_info and r_info.get("conn"):
        try:
            await r_info["conn"].disconnect()
        except Exception:
            pass
        r_info["conn"] = None
        r_info["connected"] = False

async def status_broadcast_loop():
    """Gửi trạng thái kết nối của toàn bộ đội robot định kỳ lên trình duyệt web"""
    while True:
        try:
            robot_list = []
            for r_id, r_info in ROBOTS.items():
                is_conn = bool(r_info.get("conn") and getattr(r_info["conn"], "isConnected", False))
                r_info["connected"] = is_conn
                robot_list.append({
                    "id": r_info["id"],
                    "name": r_info["name"],
                    "ip": r_info["ip"],
                    "fallback_ip": r_info.get("fallback_ip"),
                    "connected": is_conn,
                    "enabled": bool(r_info.get("enabled", True)),
                })

            payload = {
                "type": "multi_robot_status",
                "robots": robot_list,
                "target": state.get("target_robot", "all"),
                # Backward compatibility
                "robot1": next((r for r in robot_list if r["id"] == "robot1"), {"name": "Robot 1", "ip": "192.168.0.41", "connected": False}),
                "robot2": next((r for r in robot_list if r["id"] == "robot2"), {"name": "Robot 2", "ip": "192.168.0.75", "connected": False}),
            }
            for ws in list(active_websockets):
                try:
                    await ws.send_json(payload)
                except Exception:
                    active_websockets.discard(ws)
        except Exception:
            pass
        await asyncio.sleep(1)

app = FastAPI(title="Unitree Go2 Swarm Controller")

# Pydantic models cho API quản lý Robot
class RobotCreate(BaseModel):
    name: str
    ip: str
    fallback_ip: Optional[str] = None
    key: Optional[str] = None
    enabled: bool = True

@app.get("/api/robots")
async def get_robots():
    """Lấy danh sách cấu hình và trạng thái của toàn bộ robot"""
    result = []
    for r in ROBOTS.values():
        is_conn = bool(r.get("conn") and getattr(r["conn"], "isConnected", False))
        result.append({
            "id": r["id"],
            "name": r["name"],
            "ip": r["ip"],
            "fallback_ip": r.get("fallback_ip"),
            "key": r.get("key"),
            "enabled": r.get("enabled", True),
            "connected": is_conn,
        })
    return {"robots": result, "target": state.get("target_robot", "all")}

@app.post("/api/robots")
async def add_robot(robot_in: RobotCreate):
    """Thêm một robot mới vào hệ thống động và tự động kết nối ngay"""
    # Tạo ID duy nhất
    clean_ip = robot_in.ip.split(".")[-1]
    new_id = f"robot_{clean_ip}_{int(time.time()) % 1000}"
    key = robot_in.key.strip() if robot_in.key and robot_in.key.strip() else None

    ROBOTS[new_id] = {
        "id": new_id,
        "name": robot_in.name.strip(),
        "ip": robot_in.ip.strip(),
        "fallback_ip": robot_in.fallback_ip.strip() if robot_in.fallback_ip and robot_in.fallback_ip.strip() else None,
        "key": key,
        "enabled": robot_in.enabled,
        "conn": None,
        "connected": False,
    }
    save_robots_config()
    if robot_in.enabled:
        start_robot_task(new_id)

    print(f"➕ ĐÃ THÊM ROBOT MỚI: {robot_in.name} ({robot_in.ip}) [ID: {new_id}]", flush=True)
    return {"status": "ok", "id": new_id, "robot": ROBOTS[new_id]}

@app.delete("/api/robots/{robot_id}")
async def delete_robot(robot_id: str):
    """Xóa một robot khỏi hệ thống và ngắt kết nối an toàn"""
    if robot_id not in ROBOTS:
        raise HTTPException(status_code=404, detail="Không tìm thấy robot")
    
    await stop_robot_task(robot_id)
    removed = ROBOTS.pop(robot_id)
    save_robots_config()

    if state.get("target_robot") == robot_id:
        state["target_robot"] = "all"

    print(f"➖ ĐÃ XÓA ROBOT: {removed['name']} (ID: {robot_id})", flush=True)
    return {"status": "ok", "deleted_id": robot_id}

@app.post("/api/robots/{robot_id}/toggle")
async def toggle_robot(robot_id: str):
    """Bật hoặc tắt kết nối với một robot cụ thể"""
    if robot_id not in ROBOTS:
        raise HTTPException(status_code=404, detail="Không tìm thấy robot")
    
    r = ROBOTS[robot_id]
    r["enabled"] = not r.get("enabled", True)
    save_robots_config()

    if r["enabled"]:
        start_robot_task(robot_id)
    else:
        await stop_robot_task(robot_id)

    return {"status": "ok", "enabled": r["enabled"]}

def get_server_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@app.get("/api/lan_ip")
async def get_lan_ip():
    ip = get_server_lan_ip()
    return {"ip": ip, "port": 8080, "url": f"http://{ip}:8080"}

@app.on_event("startup")
async def startup_event():
    print("==================================================", flush=True)
    print("KHỞI ĐỘNG HỆ THỐNG ĐIỀU KHIỂN ROBOT SWARM ĐA NĂNG...", flush=True)
    for r_id, r_info in ROBOTS.items():
        print(f"-> {r_info['name']} (ID: {r_id}, IP: {r_info['ip']}) - Bật: {r_info['enabled']}", flush=True)
        if r_info.get("enabled", True):
            start_robot_task(r_id)
    print("==================================================", flush=True)

    asyncio.create_task(control_loop())
    asyncio.create_task(status_broadcast_loop())

@app.on_event("shutdown")
async def shutdown_event():
    for r_id in list(ROBOTS.keys()):
        await stop_robot_task(r_id)
    print("Đã ngắt kết nối an toàn với toàn bộ đội Robot.", flush=True)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    try:
        # Gửi danh sách trạng thái ban đầu
        robot_list = []
        for r_id, r_info in ROBOTS.items():
            robot_list.append({
                "id": r_info["id"],
                "name": r_info["name"],
                "ip": r_info["ip"],
                "fallback_ip": r_info.get("fallback_ip"),
                "connected": bool(r_info.get("connected", False)),
                "enabled": bool(r_info.get("enabled", True)),
            })
        await websocket.send_json({
            "type": "multi_robot_status",
            "robots": robot_list,
            "target": state.get("target_robot", "all"),
        })

        while True:
            data = await websocket.receive_json()
            cmd_type = data.get("type")

            if cmd_type == "set_target":
                target = data.get("target", "all")
                state["target_robot"] = target
                print(f"-> Chế độ điều khiển chuyển sang mục tiêu: {target}", flush=True)

            elif cmd_type == "move":
                state["vx"] = float(data.get("vx", 0.0))
                state["vy"] = float(data.get("vy", 0.0))
                state["vyaw"] = float(data.get("vyaw", 0.0))
                state["mode"] = "MOVE"
                state["last_recv_time"] = time.time()

                vx = round(state["vx"], 3)
                vy = round(state["vy"], 3)
                vyaw = round(state["vyaw"], 3)
                if abs(vx) > 0.005 or abs(vy) > 0.005 or abs(vyaw) > 0.005:
                    broadcast_sport_req(
                        SPORT_CMD["Move"],
                        parameter={"x": vx, "y": vy, "z": vyaw}
                    )
                else:
                    state["mode"] = "IDLE"
                    broadcast_sport_req(SPORT_CMD["StopMove"])

            elif cmd_type == "posture":
                roll = float(data.get("roll", 0.0))
                pitch = float(data.get("pitch", 0.0))
                yaw = float(data.get("yaw", 0.0))
                state["roll"] = roll
                state["pitch"] = pitch
                state["yaw"] = yaw
                state["mode"] = "POSTURE"
                state["last_recv_time"] = time.time()

                if abs(roll) < 0.01 and abs(pitch) < 0.01 and abs(yaw) < 0.01:
                    broadcast_sport_req(
                        SPORT_CMD["Euler"],
                        parameter={"x": 0.0, "y": 0.0, "z": 0.0}
                    )
                    broadcast_sport_req(SPORT_CMD["BalanceStand"])
                else:
                    broadcast_sport_req(
                        SPORT_CMD["Euler"],
                        parameter={"x": roll, "y": pitch, "z": yaw}
                    )

            elif cmd_type == "action":
                cmd = data.get("cmd")
                print(f"Web Action: {cmd} (Mục tiêu: {state['target_robot']})", flush=True)

                ACTION_MAP = {
                    "stand_up": SPORT_CMD.get("StandUp", 1004),
                    "stand_down": SPORT_CMD.get("StandDown", 1005),
                    "recovery": SPORT_CMD.get("RecoveryStand", 1006),
                    "balance": SPORT_CMD.get("BalanceStand", 1002),
                    "dance1": SPORT_CMD.get("Dance1", 1022),
                    "dance2": SPORT_CMD.get("Dance2", 1023),
                    "stretch": SPORT_CMD.get("Stretch", 1017),
                    "shake_hands": SPORT_CMD.get("Hello", 1016),
                    "greet": SPORT_CMD.get("Hello", 1016),
                    "pounce": SPORT_CMD.get("FrontPounce", 1032),
                    "jump_forward": SPORT_CMD.get("FrontJump", 1031),
                    "heart": SPORT_CMD.get("FingerHeart", 1036),
                    "wiggle_hips": SPORT_CMD.get("WiggleHips", 1033),
                    "scrape": SPORT_CMD.get("Scrape", 1029),
                    "front_flip": SPORT_CMD.get("FrontFlip", 1030),
                    "moonwalk": SPORT_CMD.get("MoonWalk", 1305),
                }

                if cmd in ACTION_MAP:
                    state["mode"] = "ACTION"
                    broadcast_sport_req(ACTION_MAP[cmd])
                elif cmd == "take_control":
                    state["mode"] = "ACTION"
                    broadcast_sport_req(
                        SPORT_CMD["SwitchJoystick"], parameter={"enable": False}
                    )
                elif cmd == "release_control":
                    state["mode"] = "ACTION"
                    broadcast_sport_req(
                        SPORT_CMD["SwitchJoystick"], parameter={"enable": True}
                    )
                elif cmd == "stop":
                    state["mode"] = "IDLE"
                    state["vx"] = 0.0
                    state["vy"] = 0.0
                    state["vyaw"] = 0.0
                    broadcast_sport_req(SPORT_CMD["StopMove"])

    except WebSocketDisconnect:
        print("Trình duyệt web ngắt kết nối.", flush=True)
        state["vx"] = 0.0
        state["vy"] = 0.0
        state["vyaw"] = 0.0
    finally:
        active_websockets.discard(websocket)

# Phục vụ giao diện web tại thư mục www
app.mount("/", StaticFiles(directory="www", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
