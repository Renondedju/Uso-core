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

import pyosu
import datetime

from usocore.db import db

class Beatmap(db.Model):
    __tablename__ = 'beatmaps'

    uso_id           = db.Column(db.Integer, primary_key = True)              
    approved         = db.Column(db.Integer, default  = pyosu.types.BeatmapApprovedState.Pending)
    beatmap_id       = db.Column(db.Integer, default  = 0, unique = True)
    beatmapset_id    = db.Column(db.Integer, default  = 0)
    genre_id         = db.Column(db.Integer, default  = pyosu.types.BeatmapGenre.Any)
    language_id      = db.Column(db.Integer, default  = pyosu.types.Language.Any)
    mode             = db.Column(db.Integer, default  = pyosu.types.GameMode.Osu)
    favourite_count  = db.Column(db.Integer, default  = 0)
    playcount        = db.Column(db.Integer, default  = 0)
    passcount        = db.Column(db.Integer, default  = 0)
    max_combo        = db.Column(db.Integer, default  = 0)
    artist           = db.Column(db.String , default  = "")
    creator          = db.Column(db.String , default  = "")
    source           = db.Column(db.String , default  = "")
    file_md5         = db.Column(db.String , default  = "")
    title            = db.Column(db.String , default  = "")
    version          = db.Column(db.String , default  = "")
    tags             = db.Column(db.String , default  = "")
    pp               = db.Column(db.Float  , default  = 0)
    bpm              = db.Column(db.Float  , default  = 0)
    difficultyrating = db.Column(db.Float  , default  = 0)
    diff_size        = db.Column(db.Float  , default  = 0)
    diff_overall     = db.Column(db.Float  , default  = 0)
    diff_approach    = db.Column(db.Float  , default  = 0)
    diff_drain       = db.Column(db.Float  , default  = 0)
    hit_length       = db.Column(db.Float  , default  = 0)
    total_length     = db.Column(db.Float  , default  = 0)
    aim_stars        = db.Column(db.Float  , default  = 0)
    speed_stars      = db.Column(db.Float  , default  = 0)
    playstyle        = db.Column(db.Float  , default  = 0.5)
    last_update      = db.Column(db.Date)
    approved_date    = db.Column(db.Date)

    # PP data

    # HR -> DT -> FL -> HD -> EZ
    pp_HR           = db.Column(db.Integer, default = 0)
    pp_DT           = db.Column(db.Integer, default = 0)
    pp_FL           = db.Column(db.Integer, default = 0)
    pp_HD           = db.Column(db.Integer, default = 0)
    pp_EZ           = db.Column(db.Integer, default = 0)
    pp_HDEZ         = db.Column(db.Integer, default = 0)
    pp_FLEZ         = db.Column(db.Integer, default = 0)
    pp_DTEZ         = db.Column(db.Integer, default = 0)
    pp_FLHD         = db.Column(db.Integer, default = 0)
    pp_DTHD         = db.Column(db.Integer, default = 0)
    pp_HRHD         = db.Column(db.Integer, default = 0)
    pp_HRDT         = db.Column(db.Integer, default = 0)
    pp_DTFL         = db.Column(db.Integer, default = 0)
    pp_HRFL         = db.Column(db.Integer, default = 0)
    pp_FLHDEZ       = db.Column(db.Integer, default = 0)
    pp_DTHDEZ       = db.Column(db.Integer, default = 0)
    pp_DTFLEZ       = db.Column(db.Integer, default = 0)
    pp_DTFLHD       = db.Column(db.Integer, default = 0)
    pp_HRFLHD       = db.Column(db.Integer, default = 0)
    pp_HRDTHD       = db.Column(db.Integer, default = 0)
    pp_DTFLHD       = db.Column(db.Integer, default = 0)
    pp_DTFLHDEZ     = db.Column(db.Integer, default = 0)
    pp_HRDTFLHD     = db.Column(db.Integer, default = 0)
