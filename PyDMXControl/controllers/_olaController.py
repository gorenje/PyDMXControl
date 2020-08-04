"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from ._transmittingController import transmittingController

from array import array
from ola.ClientWrapper import ClientWrapper

class olaController(transmittingController):
    def __init__(self, *args, **kwargs):

        self.__universe_id = kwargs.pop("universe", 1)

        self.__wrapper = ClientWrapper()
        self.__client = self.__wrapper.Client()
        self.__previous_data = None

        super().__init__(*args, **kwargs)

    def DmxSent(self,state):
        self.__wrapper.Stop()

    def _send_data(self):
        data = self.get_frame()
        # Since OLA remembers its state, there is no need to re-send the
        # same data continously. Only send DMX data if the data changed
        # since the last time we sent something.
        if self.__previous_data != data:
            self.__client.SendDmx(self.__universe_id, array('B', data),
                                  self.DmxSent)
            self.__previous_data = data
