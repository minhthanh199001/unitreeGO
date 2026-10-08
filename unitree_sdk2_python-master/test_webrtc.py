import sys
import asyncio

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from unitree_webrtc_connect import UnitreeWebRTCConnection, WebRTCConnectionMethod

async def main():
    print("Testing WebRTC connection to Go2 at 192.168.12.1...", flush=True)
    conn = UnitreeWebRTCConnection(
        connectionMethod=WebRTCConnectionMethod.LocalAP,
        ip="192.168.12.1"
    )
    try:
        await conn.connect()
        print("Connected successfully via WebRTC!", flush=True)
        # Test standing up or getting state
        print("Testing StandUp...", flush=True)
        # await conn.datachannel.pub_sub.publish(...)
    except Exception as e:
        print(f"Connection failed: {type(e).__name__} - {e}", flush=True)
    finally:
        try:
            await conn.disconnect()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(main())
