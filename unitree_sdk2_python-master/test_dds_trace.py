import sys
import time
import os
os.environ["CYCLONEDDS_URI"] = "<CycloneDDS><Domain id='any'><Tracing><Verbosity>finest</Verbosity><OutputFile>dds_trace.log</OutputFile></Tracing></Domain></CycloneDDS>"
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

ChannelFactoryInitialize(0, 'Ethernet 2')
sc = SportClient()
sc.SetTimeout(5.0)
sc.Init()
sc.RecoveryStand()
