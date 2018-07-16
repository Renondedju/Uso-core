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

from .decorators import requires_connection
from osupy       import pyosu

class Core():

    def __init__(self):
         
        self.connection = None
        self.api        = None

    @property
    def is_connected(self):
        return self.connection is not None and self.api is not None

    async def connect(self, api_key : str, dsn : str):
        """ Connects the core to the database and setups an api connection 
        
            api_key : osu api key. You may request an API key from [here](https://osu.ppy.sh/p/api).  
            dsn     : ``postgres://user:pass@host:port/database?option=value``
        """

        if self.is_connected:
            return

        self.connection = await asyncpg.connect(dsn = dsn)
        self.api        = pyosu.api.OsuApi(api_key)

        return

    @requires_connection
    async def test(self):
        
        await self.connection.execute('CREATE TABLE mytab (a int)')

    @requires_connection('Cannot close an unopened connection.')
    async def close(self):

        await self.connection.close()