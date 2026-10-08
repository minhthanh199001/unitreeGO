import sys
import time
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

print('Init start', flush=True)
ChannelFactoryInitialize(0, 'Ethernet 2')
print('Channel Init done', flush=True)

sc = SportClient()
sc.SetTimeout(5.0)
sc.Init()
print('SportClient Init done', flush=True)
