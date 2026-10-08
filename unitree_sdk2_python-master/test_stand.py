import sys
import asyncio

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from unitree_webrtc_connect import (
    UnitreeWebRTCConnection,
    WebRTCConnectionMethod,
    RTC_TOPIC,
    SPORT_CMD,
)

async def main():
    print("Connecting to Go2 via WebRTC (192.168.12.1)...", flush=True)
    conn = UnitreeWebRTCConnection(
        connectionMethod=WebRTCConnectionMethod.LocalAP,
        ip="192.168.12.1"
    )
    
    try:
        await conn.connect()
        print(">>> WebRTC CONNECTED SUCCESSFULLY! <<<", flush=True)
        await asyncio.sleep(1)
        
        print("Sending StandUp command...", flush=True)
        try:
            response = await asyncio.wait_for(
                conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["SPORT_MOD"],
                    {"api_id": SPORT_CMD["StandUp"]}
                ),
                timeout=2.0
            )
            print("StandUp response from robot:", response, flush=True)
        except asyncio.TimeoutError:
            print("StandUp command dispatched to robot!", flush=True)
        
        await asyncio.sleep(5)
    except Exception as e:
        print(f"Error during test: {type(e).__name__} - {e}", flush=True)
    finally:
        try:
            await conn.disconnect()
            print("Disconnected safely.", flush=True)
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(main())
