import sys
import time
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

try:
    ChannelFactoryInitialize(0, 'Ethernet 2')
    print("Init Ethernet 2 SUCCESS")
except Exception as e:
    print(f"Init Ethernet 2 FAILED: {e}")
    try:
        ChannelFactoryInitialize(0)
        print("Init Auto SUCCESS")
    except Exception as e2:
        print(f"Init Auto FAILED: {e2}")

sys.exit(0)
