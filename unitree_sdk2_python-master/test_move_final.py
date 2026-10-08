import sys
import time
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

try:
    ChannelFactoryInitialize(0, 'Ethernet 2')
    sc = SportClient()
    sc.SetTimeout(5.0)
    sc.Init()
    
    print("Recovery Stand...", flush=True)
    sc.RecoveryStand()
    time.sleep(3)
    
    print("Balance Stand...", flush=True)
    sc.BalanceStand()
    time.sleep(2)
    
    print("Moving forward...", flush=True)
    for _ in range(40):
        sc.Move(0.2, 0, 0)
        time.sleep(0.05)
        
    print("Stopping...", flush=True)
    sc.Move(0, 0, 0)
    sc.StopMove()
    print("Done", flush=True)
except Exception as e:
    print(f"Error: {e}")
