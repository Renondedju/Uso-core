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

from usocore.db import db

class Beatmap(db.Model):
    __tablename__ = 'beatmap'

    approved         = db.Column(db.Integer())
    approved_date    = db.Column(db.Date())
    last_update      = db.Column(db.Date())
    artist           = db.Column(db.String())
    beatmap_id       = db.Column(db.Integer())
    beatmapset_id    = db.Column(db.Integer())
    bpm              = db.Column(db.Float())
    creator          = db.Column(db.String())
    difficultyrating = db.Column(db.Float())
    diff_size        = db.Column(db.Float())
    diff_overall     = db.Column(db.Float())
    diff_approach    = db.Column(db.Float())
    diff_drain       = db.Column(db.Float())
    hit_length       = db.Column(db.Float())
    source           = db.Column(db.String())
    genre_id         = db.Column(db.Integer())
    language_id      = db.Column(db.Integer())
    title            = db.Column(db.String())
    total_length     = db.Column(db.Float())
    version          = db.Column(db.String())
    file_md5         = db.Column(db.String())
    mode             = db.Column(db.Integer())
    tags             = db.Column(db.String())
    favourite_count  = db.Column(db.Integer())
    playcount        = db.Column(db.Integer())
    passcount        = db.Column(db.Integer())
    max_combo        = db.Column(db.Integer())
    aim_stars        = db.Column(db.Float())
    speed_stars      = db.Column(db.Float())
    playstyle        = db.Column(db.Float())

    #No idea of how to implement this ...
                 #  acc    mods pp. Every field in the dict is an int value
    #self.pp = {} # {100 : {HD : 50, HDDT : 64}, 99 ...}
