import aiohttp
import json
import socket
import datetime

from hwamsmartctrl.stovedata import StoveData, stoveDataOf

class Airbox:
    """ A HWAM stove that is smart control enabled, is equipped with a so called "airbox" which automatically distributes the air through 3 valves. """

    ENDPOINT_GET_STOVE_DATA = "/get_stove_data"
    ENDPOINT_START = "/start"
    ENDPOINT_SET_BURN_LEVEL = "/set_burn_level"

    def __init__(self, host: str, session: aiohttp.ClientSession = None):
        """
        Parameters
        ----------
        host
            The host IP address or domain name.
        session
            Optional pre-configured client session.
        """
        self.host = host
        if session is None:
            self.session = aiohttp.ClientSession(base_url="http://"+self.host)
        else:
            self.session = session

    async def determineHostname(self) -> str:
        with socket.gethostbyaddr(self.host) as hostname:
            return hostname

    async def getStoveData(self) -> StoveData:
        async with self.session.get(self.ENDPOINT_GET_STOVE_DATA) as response:
            txt = await response.text()
            return stoveDataOf(json.loads(txt))

    async def startCombustion(self) -> bool:
        async with self.session.get(self.ENDPOINT_START) as response:
            data = await response.json()
            if data["response"] == "OK":
                return True
            else:
                return False

    async def setBurnLevel(self, level: int) -> bool:
        """
        Sets the burn level in the range 0-5.

        Level 0: HWAM Smart Control runs at lowest 
        possible comustion temperature to maintain correct combustion
        over the longest possible time, taking into account the room 
        temperature.

        Level 1-4: At these levels, the system aims
        to achieve a constant room temperature. Therefore, once you
        have found the heat level that suits you best, do not turn the
        level up and down. At level 1-4, the system starts up gently 
        until it finds the right level of flue gas temperature compared
        to the desired room temperature. For normal operation, levels 
        2-3 are recommended.

        Level 5: Level 5 is a booster level intended only for situations
        where the stove needs to produce a lot of heat within a short 
        period of time. The stove should NOT run at level 5 for a long 
        period of time. NB! If level 5 is chosen, a lot of wood is needed
        to maintain correct combustion. Therefore, re-stoking alarams may 
        sound even if there are still flames and unburned wood in the 
        combustion chamber.

        Throws NotImplementedError as it does work with Airbox version 3.23.0
        """
        raise NotImplementedError
        async with self.session.post(self.ENDPOINT_SET_BURN_LEVEL, data={"level": level}) as response:
            data = await response.json()
            if data["response"] == "OK":
                return True
            else:
                return False

def connect(host: str) -> Airbox:
    """ Creates a new Airbox connection

    Parameters
    ----------
    host : str
        The host IP or domain name
    """
    return Airbox(str, aiohttp.ClientSession(base_url="http://"+host))
