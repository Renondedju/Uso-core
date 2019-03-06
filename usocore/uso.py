# MIT License

# Copyright (c) 2018 Renondedju

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import asyncpg
import pyosu

from .db         import db
from .models     import Beatmap, User
from .decorators import requires_connection

class UsoCore():

    def __init__(self):
        self.gino_api  = None
        self.osu_api   = None

    @property
    def is_connected(self):
        """ Checks if the uso core is connected
        """
        return self.gino_api is not None and self.osu_api is not None

    async def connect(self, api_key : str, dsn : str):
        """ Connects the core to the database and setups an API connection 
        
            api_key : osu api key. You may request an API key from [here](https://osu.ppy.sh/p/api).  
            dsn     : ``postgresql://user:pass@host:port/database?option=value``
        """

        if self.is_connected:
            return

        # Connecting to the database
        self.gino_api = await db.set_bind(dsn)
        await db.gino.create_all()

        # Creating an osu api interface
        self.osu_api = pyosu.api.OsuApi(api_key)

        return

    @requires_connection('Cannot close an unopened connection.')
    async def close(self):
        """ Closes the connections withe the database and the osu API interface
        """

        await db.pop_bind().close()
        self.gino_api = None
        self.osu_api  = None
