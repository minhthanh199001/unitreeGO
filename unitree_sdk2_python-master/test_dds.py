import sys
import time
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_

def handler(msg: SportModeState_):
    print(f"Received battery: {msg.battery if hasattr(msg, 'battery') else '?'}, mode: {msg.mode}, pos: {msg.position}")
    sys.exit(0)

if __name__ == '__main__':
    ChannelFactoryInitialize(0, 'Wi-Fi')
    sub = ChannelSubscriber('rt/sportmodestate', SportModeState_)
    sub.Init(handler, 10)
    print('Waiting for SportModeState...')
    time.sleep(5)
    print('Timeout')
    sys.exit(1)
