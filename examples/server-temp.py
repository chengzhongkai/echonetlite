import argparse
import struct

from echonetlite.interfaces import monitor
from echonetlite import middleware
from echonetlite.protocol import *

class MyTemperature(middleware.NodeSuperObject):
    def __init__(self, eoj):
        super(MyTemperature, self).__init__(eoj=eoj)
        # self.property[EPC_MANUFACTURE_CODE] = ...
        self._add_property(EPC_TEMPERATURE, [0,0])
        self.get_property_map += [
            EPC_TEMPERATURE]

        monitor.schedule_loopingcall(
            1,
            self._update_temperature)

    def _update_temperature(self):
        # update temperature value here
        val = 270
        self._properties[EPC_TEMPERATURE] = struct.pack('!h', val)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--self-node', dest='self_node', required=True,
                        help='IP address of this node')
    args = parser.parse_args()

    # Create local devices
    profile = middleware.NodeProfile()
    # profile.property[EPC_MANUFACTURE_CODE] = ...
    # profile.property[EPC_IDENTIFICATION_NUMBER] = ...
    temperature = MyTemperature(eoj=EOJ(clsgrp=CLSGRP_CODE['SENSOR'],
                                        cls=CLS_SE_CODE['TEMPERATURE'],
                                        instance_id=1))

    # Start the Echonet Lite message loop
    monitor.start(node_id=args.self_node,
                  devices={str(profile.eoj): profile,
                           str(temperature.eoj): temperature})
