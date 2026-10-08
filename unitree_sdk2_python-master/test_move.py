import sys
import time
import os
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

os.environ["CYCLONEDDS_URI"] = "file://" + os.path.abspath("cyclonedds.xml")
ChannelFactoryInitialize(0)
sc = SportClient()
sc.SetTimeout(5.0)
sc.Init()

print("Standing up...")
sc.StandUp()
time.sleep(2)
print("Moving...")
for _ in range(20):
    sc.Move(0.1, 0, 0)
    time.sleep(0.05)
print("Done")
