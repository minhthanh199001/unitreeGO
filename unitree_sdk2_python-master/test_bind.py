import sys
import time
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

try:
    ChannelFactoryInitialize(0)
    sc = SportClient()
    sc.SetTimeout(5.0)
    sc.Init()
    print("Init SUCCESS", flush=True)
    sc.RecoveryStand()
    print("Recovery Stand Sent", flush=True)
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
