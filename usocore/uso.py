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

import datetime
import asyncio
import asyncpg
import oppai
import pyosu

from .db         import db
from .models     import Beatmap, User
from .decorators import requires_connection

class UsoCore():

    # Supported mods are HardRock, DoubleTime, FlashLight, Hidden and Easy
    # Every combination of any of those mods are supported.
    supported_mods_combinations = [
        oppai.MODS_HR,
        oppai.MODS_DT,
        oppai.MODS_FL,
        oppai.MODS_HD,
        oppai.MODS_EZ,
        oppai.MODS_HD | oppai.MODS_EZ,
        oppai.MODS_FL | oppai.MODS_EZ,
        oppai.MODS_DT | oppai.MODS_EZ,
        oppai.MODS_FL | oppai.MODS_HD,
        oppai.MODS_DT | oppai.MODS_HD,
        oppai.MODS_HR | oppai.MODS_HD,
        oppai.MODS_HR | oppai.MODS_DT,
        oppai.MODS_DT | oppai.MODS_FL,
        oppai.MODS_HR | oppai.MODS_FL,
        oppai.MODS_FL | oppai.MODS_HD | oppai.MODS_EZ,
        oppai.MODS_DT | oppai.MODS_HD | oppai.MODS_EZ,
        oppai.MODS_DT | oppai.MODS_FL | oppai.MODS_EZ,
        oppai.MODS_DT | oppai.MODS_FL | oppai.MODS_HD,
        oppai.MODS_HR | oppai.MODS_FL | oppai.MODS_HD,
        oppai.MODS_HR | oppai.MODS_DT | oppai.MODS_HD,
        oppai.MODS_DT | oppai.MODS_FL | oppai.MODS_HD,
        oppai.MODS_DT | oppai.MODS_FL | oppai.MODS_HD | oppai.MODS_EZ,
        oppai.MODS_HR | oppai.MODS_DT | oppai.MODS_FL | oppai.MODS_HD
    ]

    def __init__(self):
        self.gino_api   = None
        self.osu_api    = None

    @property
    def is_connected(self):
        """ Checks if the uso core is connected
        """
        return self.gino_api is not None and self.osu_api is not None

    @staticmethod
    def get_mod_name(mods: int) -> str:
        mod_name = ""
        if (mods & oppai.MODS_HR == oppai.MODS_HR):
            mod_name += "HR"
        if (mods & oppai.MODS_DT == oppai.MODS_DT):
            mod_name += "DT"
        if (mods & oppai.MODS_FL == oppai.MODS_FL):
            mod_name += "FL"
        if (mods & oppai.MODS_HD == oppai.MODS_HD):
            mod_name += "HD"
        if (mods & oppai.MODS_EZ == oppai.MODS_EZ):
            mod_name += "EZ"

        return mod_name

    async def connect(self, api_key : str, dsn : str) -> bool:
        """ Connects the core to the database and setups an API connection 
        
            api_key : osu api key. You may request an API key from [here](https://osu.ppy.sh/p/api).  
            dsn     : ``postgresql://user:pass@host:port/database?option=value``

            returns true if the connection succeeded
        """

        if self.is_connected:
            return False

        # Connecting to the database
        self.gino_api = await db.set_bind(dsn)
        await db.gino.create_all()

        # Creating an osu api interface
        self.osu_api = pyosu.api.OsuApi(api_key)

        return self.is_connected

    @requires_connection('Cannot close an unopened connection.')
    async def close(self):
        """ Closes the connections withe the database and the osu API interface
        """

        await db.pop_bind().close()
        self.gino_api = None
        self.osu_api  = None

    @requires_connection('Cannot request a beatmap without connection.')
    async def request_beatmap(self, beatmap_id: int, force_update: bool = False, try_import: bool = True) -> Beatmap:
        """ Requests a beatmap from the UsoCore database, if the beatmap does not exists
            this method will try to automatically import it from the osu API.
            
            If the operation fails, this method return None.
        """

        beatmap = await Beatmap.query.where(
            Beatmap.beatmap_id == beatmap_id
        ).gino.first()

        # If the beatmap isn't in the database and if we should try to import it, importing it...
        if beatmap is None and try_import:
            return await self.import_beatmap(beatmap_id)

        # If we should try to update the beatmap
        if force_update:
            beatmap = await self.update_beatmap(beatmap_id)

        return beatmap

    @requires_connection('Cannot import a beatmap without connection.')
    async def import_beatmap(self, beatmap_id: int, check_database: bool = False) -> Beatmap:
        """ Fetches a beatmap from the osu API and imports it into the database.
            Be careful since this method won't check if the beatmap already exists in
            the database before importing it unless 'check_database' is True

            Returns the imported beatmap or None in case of failure.
        """

        # If we should check the database before importing
        if check_database:
            beatmap = await Beatmap.query.where(
                Beatmap.beatmap_id == beatmap_id
            ).gino.first()

            # Found a beatmap, stoping the operation here.
            if beatmap is not None:
                return beatmap

        # Fetching the beatmap from the osu API
        beatmap = await self.fetch_beatmap(beatmap_id)

        # If the beatmap doesn't exists
        if beatmap is None:
            return None

        # Otherwise, adding it to the database 
        return await Beatmap.create(**beatmap.__values__)

    @requires_connection('Cannot update a beatmap without connection.')
    async def update_beatmap(self, beatmap_id: int) -> Beatmap:
        """ This method checks if the beatmap requires an update.
            If this is the case, this method will fetch the new version from the osu API
            and update the UsoCore database.

            This method returns the updated version of the requested beatmap or None
            if the operation failed in any way.
        """

        # Fetching the beatmap from the osu API and from our database
        api_beatmap = await self.osu_api.get_beatmap(beatmap_id=beatmap_id)
        db_beatmap  = await Beatmap.query.where(
            Beatmap.beatmap_id == beatmap_id
        ).gino.first()

        # If the beatmap isn't int the osu API or in our database, the operation failed.
        if api_beatmap is None or db_beatmap is None:
            return None

        # Checking if we are already up to date
        if api_beatmap.last_update == db_beatmap.last_update:
            return db_beatmap

        # If this is not the case, requesting the new full version
        updated_beatmap = await self.fetch_beatmap(beatmap_id=beatmap_id, api_beatmap=api_beatmap)

        # If the requested beatmap doesn't exists
        if updated_beatmap is None:
            return None

        # Applying changes to the database
        await  db_beatmap.update(**updated_beatmap.__values__).apply()
        return db_beatmap

    @requires_connection('Cannot request a beatmap without connection.')
    async def fetch_beatmap(self, beatmap_id: int = None, api_beatmap: pyosu.models.Beatmap = None) -> Beatmap:
        """ Fetches a beatmap from the Osu! API and computes every statistics.
            This method is slow, use it carefully to avoid performance issues

            To know how to use every parameter, please refer to the osu.py
            documentation for the 'get_beatmap' method.
        """

        # Fetching the beatmap from the osu API
        if api_beatmap is None:
            api_beatmap = await self.osu_api.get_beatmap(beatmap_id=beatmap_id)

        # Downloading the beatmap from the osu API
        data = await self.osu_api.get_beatmap_file(beatmap_id)

        if api_beatmap is None or data is None:
            return None

        # Creating an ezpp object
        oppai_beatmap = oppai.ezpp_new()
        beatmap       = Beatmap()

        oppai.ezpp_data_dup    (oppai_beatmap, data.content, len(data.content.encode('utf-8')))
        oppai.ezpp_set_autocalc(oppai_beatmap, True)
        
        # looks like max combo can be none for some reason ...
        if api_beatmap.max_combo is None:
            api_beatmap.max_combo = oppai.ezpp_max_combo(oppai_beatmap)

        beatmap.approved         = int(api_beatmap.approved)
        beatmap.beatmap_id       = int(api_beatmap.beatmap_id)
        beatmap.beatmapset_id    = int(api_beatmap.beatmapset_id)
        beatmap.genre_id         = int(api_beatmap.genre_id)
        beatmap.language_id      = int(api_beatmap.language_id)
        beatmap.mode             = int(api_beatmap.mode)
        beatmap.favourite_count  = int(api_beatmap.favourite_count)
        beatmap.playcount        = int(api_beatmap.playcount)
        beatmap.passcount        = int(api_beatmap.passcount)
        beatmap.max_combo        = int(api_beatmap.max_combo)
        beatmap.artist           = api_beatmap.artist
        beatmap.creator          = api_beatmap.creator
        beatmap.source           = api_beatmap.source
        beatmap.file_md5         = api_beatmap.file_md5
        beatmap.title            = api_beatmap.title
        beatmap.version          = api_beatmap.version
        beatmap.tags             = api_beatmap.tags
        beatmap.pp               = oppai.ezpp_pp(oppai_beatmap)
        beatmap.bpm              = float(api_beatmap.bpm)
        beatmap.difficultyrating = float(api_beatmap.difficultyrating)
        beatmap.diff_size        = float(api_beatmap.diff_size)
        beatmap.diff_overall     = float(api_beatmap.diff_overall)
        beatmap.diff_approach    = float(api_beatmap.diff_approach)
        beatmap.diff_drain       = float(api_beatmap.diff_drain)
        beatmap.hit_length       = float(api_beatmap.hit_length)
        beatmap.total_length     = float(api_beatmap.total_length)
        beatmap.aim_stars        = oppai.ezpp_aim_stars  (oppai_beatmap)
        beatmap.speed_stars      = oppai.ezpp_speed_stars(oppai_beatmap)
        beatmap.playstyle        = beatmap.aim_stars / float(api_beatmap.difficultyrating)
        beatmap.last_update      = datetime.datetime.strptime(api_beatmap.last_update  , "%Y-%m-%d %H:%M:%S")
        beatmap.approved_date    = datetime.datetime.strptime(api_beatmap.approved_date, "%Y-%m-%d %H:%M:%S")

        for mods in UsoCore.supported_mods_combinations:
            oppai.ezpp_set_mods(oppai_beatmap, mods)
            setattr(beatmap, "pp_" + UsoCore.get_mod_name(mods), oppai.ezpp_pp(oppai_beatmap))

        oppai_beatmap = oppai.ezpp_free(oppai_beatmap)
        
        return beatmap
