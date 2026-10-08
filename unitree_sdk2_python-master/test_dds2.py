import sys
import time
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_

def handler(msg: SportModeState_):
    print(f"Received msg: mode {msg.mode}")
    sys.exit(0)

if __name__ == '__main__':
    ChannelFactoryInitialize(0, '192.168.12.41')
    sub = ChannelSubscriber('rt/sportmodestate', SportModeState_)
    sub.Init(handler, 10)
    print('Waiting for SportModeState on IP...')
    time.sleep(5)
    print('Timeout')
    sys.exit(1)
