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

from datetime import datetime
from gino     import Gino

db = Gino()

class User(db.Model):
    __tablename__ = 'users'
        
    user_id            = db.Column(db.Integer())
    username           = db.Column(db.String())
    count300           = db.Column(db.Integer())
    count100           = db.Column(db.Integer())
    count50            = db.Column(db.Integer())
    playcount          = db.Column(db.Integer())
    ranked_score       = db.Column(db.Float())
    total_score        = db.Column(db.Float())
    pp_rank            = db.Column(db.Integer())
    level              = db.Column(db.Float())
    pp_raw             = db.Column(db.Float())
    accuracy           = db.Column(db.Float())
    count_rank_ss      = db.Column(db.Integer())
    count_rank_ssh     = db.Column(db.Integer())
    count_rank_s       = db.Column(db.Integer())
    count_rank_sh      = db.Column(db.Integer())
    count_rank_a       = db.Column(db.Integer())
    country            = db.Column(db.String())
    pp_country_rank    = db.Column(db.Integer())
    #events            = db.Column(db.) No idea of how to do this since events are a list of the user_event model
    accuracy_average   = db.Column(db.Integer())
    pp_average         = db.Column(db.Float())
    bpm_low            = db.Column(db.Float())
    bpm_average        = db.Column(db.Float())
    bpm_high           = db.Column(db.Float())
    od_average         = db.Column(db.Float())
    ar_average         = db.Column(db.Float())
    cs_average         = db.Column(db.Float())
    len_average        = db.Column(db.Float())
    playstyle          = db.Column(db.Float())
    last_update        = db.Column(db.Date())
    last_patch_used    = db.Column(db.String())

    # Same as events here

    # Every value in the dict is an int value
    # {HD : 20, HDDT : 60, ...}
    #self.playrate    = {}

    # Every value in the dict is an int value
    # mods :  beatmaps id recommended in this mods
    #  {HD : [123456, 456789, 132456, ...], HDDT : [...], ...}
    #self.recommended = {}

    