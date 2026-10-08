import sys
import time
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_

def handler(msg: SportModeState_):
    print(f"Robot Mode: {msg.mode}", flush=True)
    sys.exit(0)

if __name__ == '__main__':
    ChannelFactoryInitialize(0, '192.168.123.162')
    sub = ChannelSubscriber('rt/sportmodestate', SportModeState_)
    sub.Init(handler, 10)
    print('Waiting for Robot telemetry...', flush=True)
    time.sleep(5)
    print('Failed to receive telemetry (Timeout)', flush=True)
    sys.exit(1)
