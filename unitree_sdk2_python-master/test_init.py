import sys
import time
from unitree_sdk2py.core.channel import ChannelFactoryInitialize

print('Init start', flush=True)
ChannelFactoryInitialize(0, 'Ethernet 2')
print('Init done', flush=True)
