import sys
import time
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

ChannelFactoryInitialize(0)
sc = SportClient()
sc.SetTimeout(5.0)
sc.Init()

print("Sending RecoveryStand...")
sc.RecoveryStand()
time.sleep(2)
print("Sending StandUp...")
sc.StandUp()
time.sleep(2)
print("Done")
