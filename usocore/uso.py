# MIT License

# Copyright (c) 2018-2019 Renondedju

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

import pyosu
import oppai
import asyncio
import asyncpg
import datetime

from typing             import List, Dict
from usocore.cache      import Cache
from usocore.db         import db
from usocore.models     import Beatmap, User
from usocore.decorators import requires_connection

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

    def __init__(self, use_cache: bool = True, cache_location: str = "./.uso_cache/"):
        self.gino_api   = None
        self.osu_api    = None
        self.cache      = None

        if use_cache:
            self.cache = Cache(cache_location)

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

    @requires_connection('Cannot request a user without connection.')
    async def request_user(self, user_id: int, force_update: bool = False, try_import: bool = True) -> User:
        """ Requests a user from the UsoCore database, if the user does not exists
            this method will try to automatically import it from the osu API.
            
            If the operation fails, this method return None.
        """

        user = await User.query.where(
            User.user_id == user_id
        ).gino.first()

        # If the user isn't in the database and if we should try to import it, importing it...
        if user is None and try_import:
            return await self.import_user(user_id)

        elif user is None and not try_import:
            return None

        # If we should force the update of the user or if 
        # more than one day passed since the last update
        if force_update or ((user.last_update + datetime.timedelta(days=1)) <= datetime.datetime.now().date()):
            user = await self.update_user(user_id)

        return user

    @requires_connection('Cannot import a user without connection.')
    async def import_user(self, user_id: int, check_database: bool = False) -> User:
        """ Fetches a user from the osu API and imports it into the database.
            Be careful since this method won't check if the user already exists in
            the database before importing it unless 'check_database' is True

            Returns the imported user or None in case of failure.
        """

        # If we should check the database before importing
        if check_database:
            user = await User.query.where(
                User.user_id == user_id
            ).gino.first()

            # Found a user, stoping the operation here.
            if user is not None:
                return user

        # Fetching the user from the osu API
        user = await self.fetch_user(user_id)

        # If the beatmap doesn't exists
        if user is None:
            return None

        # Otherwise, adding it to the database 
        return await User.create(**user.__values__)

    @requires_connection('Cannot import a user without connection.')
    async def update_user(self, user_id: int) -> User:

        database_user = await User.query.where(
            User.user_id == user_id
        ).gino.first()

        if database_user is None:
            return None

        api_user = await self.osu_api.get_user(user_id, type_str='id', mode=pyosu.types.GameMode.Osu)

        if api_user is None:
            return None

        # If the user won at least 5 pp, updating the user
        if api_user.pp_raw > database_user.pp_raw + 5:
            await database_user.update(**(await self.fetch_user(user_id, api_user = api_user)).__values__).apply()
        else:
            await database_user.update(last_update = datetime.datetime.now()).apply()

        return database_user

    @requires_connection('Cannot fetch a user without connection.')
    async def fetch_user(self, user_id: int = None, api_user: pyosu.models.User = None, sample_size: int = 30) -> User:
        """ Fetches a user from the Osu! API and computes every statistics.
            This method is slow, use it carefully to avoid performance issues
        """

        # Fetching the beatmap from the osu API
        if api_user is None:
            api_user = await self.osu_api.get_user(user_id, type_str='id', mode=pyosu.types.GameMode.Osu)

            # If there is no such user in the osu API
            if api_user is None:
                return None

        # Calmping the sample size between 1 and 100
        sample_size = min(max(1, sample_size), 100)

        # Downloading the beatmap from the osu API
        bests = await self.osu_api.get_user_bests(user_id, type_str='id', mode=pyosu.types.GameMode.Osu, limit=sample_size)

        # Fetching every user best from the database or the osu API (so we have stats to work with)
        bests_map = [await self.request_beatmap(beatmap_id=int(best.beatmap_id)) for best in bests]

        return await self.compute_user(api_user, bests, bests_map)

    async def compute_user(self, api_user: pyosu.models.User, user_bests_collection: pyosu.models.UserBestCollection, user_bests_beatmaps: List[Beatmap]) -> User:
        """ Computes user statistics
        """

        user = User()

        user.user_id          = api_user.user_id
        user.count300         = api_user.count300
        user.count100         = api_user.count100
        user.count50          = api_user.count50
        user.playcount        = api_user.playcount
        user.pp_rank          = api_user.pp_rank
        user.count_rank_ss    = api_user.count_rank_ss
        user.count_rank_ssh   = api_user.count_rank_ssh
        user.count_rank_a     = api_user.count_rank_a
        user.count_rank_s     = api_user.count_rank_s
        user.count_rank_sh    = api_user.count_rank_sh
        user.pp_country_rank  = api_user.pp_country_rank
        user.ranked_score     = api_user.ranked_score
        user.total_score      = api_user.total_score
        user.level            = api_user.level
        user.pp_raw           = api_user.pp_raw
        user.accuracy         = api_user.accuracy
        user.country          = api_user.country
        user.username         = api_user.username
        user.last_update      = datetime.datetime.now()

        user.bpm_low        = user_bests_beatmaps[0].bpm
        user.bpm_high       = user_bests_beatmaps[0].bpm
        user.pp_average     = 0.0
        user.od_average     = 0.0
        user.ar_average     = 0.0
        user.cs_average     = 0.0
        user.bpm_average    = 0.0
        user.len_average    = 0.0
        user.preferred_mods = pyosu.types.GameModifier.none

        sample_size = len(user_bests_beatmaps)

        mods_played: Dict[int, int] = {}
        for index in range(sample_size):
            user.pp_average  += user_bests_collection[index].pp            / sample_size
            user.od_average  += user_bests_beatmaps  [index].diff_overall  / sample_size
            user.ar_average  += user_bests_beatmaps  [index].diff_approach / sample_size
            user.cs_average  += user_bests_beatmaps  [index].diff_size     / sample_size
            user.bpm_average += user_bests_beatmaps  [index].bpm           / sample_size
            user.len_average += user_bests_beatmaps  [index].hit_length    / sample_size

            if user_bests_collection[index].enabled_mods in mods_played.keys():
                mods_played[user_bests_collection[index].enabled_mods] += 1
            else:
                mods_played[user_bests_collection[index].enabled_mods] = 1
            
            user.bpm_high = max(user_bests_beatmaps[index].bpm, user.bpm_high)
            user.bpm_low  = min(user_bests_beatmaps[index].bpm, user.bpm_low )

        # Selecting the user preferred mods
        max_value = 0
        for key, value in mods_played.items():
            if value > max_value:
                user.preferred_mods = key
                max_value = value

        return user

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
        updated_beatmap = await self.fetch_beatmap(beatmap_id=beatmap_id, api_beatmap=api_beatmap, use_cache=False)

        # If the requested beatmap doesn't exists
        if updated_beatmap is None:
            return None

        # Applying changes to the database
        await  db_beatmap.update(**updated_beatmap.__values__).apply()
        return db_beatmap

    @requires_connection('Cannot request a beatmap without connection.')
    async def get_beatmaps_ids(self) -> List[int]:
        """ Returns a list containing all the already present beatmap ids in the database.
            This is useful when importing huge amount of beatmaps into the database, 
            it allows to remove the already present beatmaps from your list before
            actually importing it and so optimize the process.
        """
        return await db.select([Beatmap]).gino.load((Beatmap.beatmap_id)).all()

    @requires_connection('Cannot fetch a beatmap without connection.')
    async def fetch_beatmap(self, beatmap_id: int = None, api_beatmap: pyosu.models.Beatmap = None, use_cache: bool = True) -> Beatmap:
        """ Fetches a beatmap from the Osu! API and computes every statistics.
            This method is slow, use it carefully to avoid performance issues
        """

        # Fetching the beatmap from the osu API
        if api_beatmap is None:
            try:
                api_beatmap = await self.osu_api.get_beatmap(beatmap_id=beatmap_id)
            except UnicodeDecodeError:
                return None

        if api_beatmap is None:
            return None

        # Reading from the cache if possible
        data            = None
        downloaded_data = False
        if use_cache and self.cache is not None:
            data = self.cache.read(f"{beatmap_id}.osu")

        # If cache reading failed then downloading the beatmap
        if data is None:
            try:
                data            = await self.osu_api.get_beatmap_file(beatmap_id)
                downloaded_data = True
            except UnicodeDecodeError:
                return None

        if data is None:
            return None
        if isinstance(data, pyosu.models.BeatmapFile):
            data = data.content

        # If a cache is avaliable, and that we just downloaded some data,
        # storing the new file into the cache
        if downloaded_data and self.cache is not None:
            self.cache.write(f"{beatmap_id}.osu", data)

        return await self.compute_beatmap(api_beatmap, data)

    async def compute_beatmap(self, api_beatmap: pyosu.models.Beatmap, beatmap_file_content: str) -> Beatmap:
        """ Computes a beatmap statistics and pp values
        """

        # Creating an ezpp object
        oppai_beatmap = oppai.ezpp_new()
        beatmap       = Beatmap()

        oppai.ezpp_data_dup    (oppai_beatmap, beatmap_file_content, len(beatmap_file_content.encode('utf-8')))
        oppai.ezpp_set_autocalc(oppai_beatmap, True)
        
        # Since Graveyard beatmaps does not influences the player stats, ignoring them
        if int(api_beatmap.approved) == pyosu.types.BeatmapApprovedState.Graveyard:
            return None

        # looks like max combo can be none for some reason ...
        if api_beatmap.max_combo is None:
            api_beatmap.max_combo = oppai.ezpp_max_combo(oppai_beatmap)

        beatmap.approved         = api_beatmap.approved
        beatmap.beatmap_id       = api_beatmap.beatmap_id
        beatmap.beatmapset_id    = api_beatmap.beatmapset_id
        beatmap.genre_id         = api_beatmap.genre_id
        beatmap.language_id      = api_beatmap.language_id
        beatmap.mode             = api_beatmap.mode
        beatmap.favourite_count  = api_beatmap.favourite_count
        beatmap.playcount        = api_beatmap.playcount
        beatmap.passcount        = api_beatmap.passcount
        beatmap.max_combo        = api_beatmap.max_combo
        beatmap.artist           = api_beatmap.artist
        beatmap.creator          = api_beatmap.creator
        beatmap.source           = api_beatmap.source
        beatmap.file_md5         = api_beatmap.file_md5
        beatmap.title            = api_beatmap.title
        beatmap.version          = api_beatmap.version
        beatmap.tags             = api_beatmap.tags
        beatmap.pp               = oppai.ezpp_pp(oppai_beatmap)
        beatmap.bpm              = api_beatmap.bpm
        beatmap.difficultyrating = api_beatmap.difficultyrating
        beatmap.diff_size        = api_beatmap.diff_size
        beatmap.diff_overall     = api_beatmap.diff_overall
        beatmap.diff_approach    = api_beatmap.diff_approach
        beatmap.diff_drain       = api_beatmap.diff_drain
        beatmap.hit_length       = api_beatmap.hit_length
        beatmap.total_length     = api_beatmap.total_length
        beatmap.aim_stars        = oppai.ezpp_aim_stars  (oppai_beatmap)
        beatmap.speed_stars      = oppai.ezpp_speed_stars(oppai_beatmap)
        beatmap.last_update      = api_beatmap.last_update
        beatmap.approved_date    = api_beatmap.approved_date

        if float(api_beatmap.difficultyrating) == 0:
            beatmap.playstyle = 0.5
        else:
            beatmap.aim_stars = beatmap.aim_stars / float(api_beatmap.difficultyrating)

        for mods in UsoCore.supported_mods_combinations:
            oppai.ezpp_set_mods(oppai_beatmap, mods)
            # Adding so much mods at the same time might overflow an int32.
            # Since the database cannot handle 64bits int, we need to clamp it down to a 32bit int
            setattr(beatmap, "pp_" + UsoCore.get_mod_name(mods), min(oppai.ezpp_pp(oppai_beatmap), 2147483647))

        oppai_beatmap = oppai.ezpp_free(oppai_beatmap)
        
        return beatmap
