#!/usr/bin/env python

# This software is part of the EEGsynth project, see <https://github.com/eegsynth/eegsynth>.
#
# Copyright (C) 2018-2024 EEGsynth project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import asyncio
from bleak import BleakClient, discover

if hasattr(sys, 'frozen'):
    path = os.path.split(sys.executable)[0]
    file = os.path.split(__file__)[-1]
    name = os.path.splitext(file)[0]
elif __name__ == '__main__' and sys.argv[0] != '':
    path = os.path.split(sys.argv[0])[0]
    file = os.path.split(sys.argv[0])[-1]
    name = os.path.splitext(file)[0]
elif __name__ == '__main__':
    path = os.path.abspath('')
    file = os.path.split(path)[-1] + '.py'
    name = os.path.splitext(file)[0]
else:
    path = os.path.split(__file__)[0]
    file = os.path.split(__file__)[-1]
    name = os.path.splitext(file)[0]

# the lib directory contains shared code
sys.path.append(os.path.join(path, '../../lib'))
import EEGsynth


class PolarClient:
    def __init__(self, path, name):

        # configure and start the patch, this will parse the command-line arguments and the ini file
        patch = EEGsynth.patch(name=name, path=path)

        # this shows the splash screen and can be used to track parameters that have changed
        self.monitor = EEGsynth.monitor(name=name, debug=self.patch.getint("general", "debug", default=1))

        # BLE client.
        self.loop = asyncio.get_event_loop()
        self.ble_client = BleakClient(self.patch.getstring("input", "uuid"), loop=self.loop)
        self.loop.run_until_complete(self.discover())


    async def discover(self):
        devices = await discover()
        for d in devices:
            self.monitor.info(d)


    async def connect(self):
        self.monitor.info("Trying to connect to Polar belt {0}".format(self.patch.getstring("input", "uuid")))
        await self.ble_client.connect()
        await self.ble_client.start_notify(self.patch.getstring("input", "uuid"),
                                           self.data_handler)
        self.monitor.success("Connected to Polar belt {0}".format(self.patch.getstring("input", "uuid")))


    def start(self):
        asyncio.ensure_future(self.connect())
        self.loop.run_forever()


    def stop(self):
        asyncio.ensure_future(self.ble_client.stop_notify(self.patch.getstring("input", "uuid")))
        asyncio.ensure_future(self.ble_client.disconnect())
        self.monitor.success("Disconnected from Polar belt {0}".format(self.patch.getstring("input", "uuid")))


    def data_handler(self, sender, data):    # sender (UUID) unused but required by Bleak API
        """
        data has up to 6 bytes:
        byte 1: flags
            00 = only HR
            16 = HR and IBI(s)
        byte 2: HR
        byte 3 and 4: IBI1
        byte 5 and 6: IBI2 (if present)
        byte 7 and 8: IBI3 (if present)
        etc.

        Polar H10 Heart Rate Characteristics
        (UUID: 00002a37-0000-1000-8000-00805f9b34fb):
            + Energy expenditure is not transmitted
            + HR only transmitted as uint8, no need to check if HR is
              transmitted as uint8 or uint16 (necessary for bpm > 255)
        Acceleration and raw ECG only available via Polar SDK
        """
        bytes = list(data)
        hr = None
        ibis = []
        if bytes[0] == 00:
            hr = data[1]
        if bytes[0] == 16:
            hr = data[1]
            for i in range(2, len(bytes), 2):
                ibis.append(data[i] + 256 * data[i + 1])
        if ibis:
            for ibi in ibis:
                self.patch.setvalue(self.patch.getstring("output", "key_ibi"), ibi)
        if hr:
            self.patch.setvalue(self.patch.getstring("output", "key_hr"), hr)
        print("Received HR={0}, IBI(s)={1}".format(hr, ibis))


if __name__ == "__main__":
    polar = PolarClient(path, name)
    try:
        polar.start()
    except (SystemExit, KeyboardInterrupt, RuntimeError):
        polar.stop()
    sys.exit()
