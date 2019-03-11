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

import json
import time
import asyncio

from usocore import *

async def main():

    settings = json.load(open('test-config.json'))
    core     = UsoCore()

    if await core.connect(settings.get('api_key'), settings.get('dsn')):
        await import_user(core)
        await core.close()

    return

async def import_user(core: UsoCore):
    return await core.request_user(718454)

async def import_beatmaps(core: UsoCore):

    file = open("D:\\Basile\\Downloads\\list.txt", "r")
    ids = [int(id[:-1]) for id in file.readlines()]
    file.close()

    print(f"Found {len(ids)} beatmaps !")

    imported_ids = await core.get_beatmaps_ids()
    ids = set(ids) - set(imported_ids)

    print(f"Starting importation of {len(ids)} beatmaps ...")

    for index, bmap_id in enumerate(ids):
        print(f"[{index}/{len(ids)}] Importing {bmap_id}")
        await core.request_beatmap(beatmap_id=bmap_id)

if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(main())