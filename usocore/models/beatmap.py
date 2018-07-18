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
    beatmap_id       = db.Column(db.Integer())
    beatmapset_id    = db.Column(db.Integer())
    genre_id         = db.Column(db.Integer())
    language_id      = db.Column(db.Integer())
    mode             = db.Column(db.Integer())
    favourite_count  = db.Column(db.Integer())
    playcount        = db.Column(db.Integer())
    passcount        = db.Column(db.Integer())
    max_combo        = db.Column(db.Integer())
    artist           = db.Column(db.String ())
    creator          = db.Column(db.String ())
    source           = db.Column(db.String ())
    file_md5         = db.Column(db.String ())
    title            = db.Column(db.String ())
    version          = db.Column(db.String ())
    tags             = db.Column(db.String ())
    pp               = db.Column(db.String ())
    bpm              = db.Column(db.Float  ())
    difficultyrating = db.Column(db.Float  ())
    diff_size        = db.Column(db.Float  ())
    diff_overall     = db.Column(db.Float  ())
    diff_approach    = db.Column(db.Float  ())
    diff_drain       = db.Column(db.Float  ())
    hit_length       = db.Column(db.Float  ())
    total_length     = db.Column(db.Float  ())
    aim_stars        = db.Column(db.Float  ())
    speed_stars      = db.Column(db.Float  ())
    playstyle        = db.Column(db.Float  ())
    last_update      = db.Column(db.Date   ())
    approved_date    = db.Column(db.Date   ())
