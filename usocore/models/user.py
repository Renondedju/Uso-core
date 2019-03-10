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

class User(db.Model):
    __tablename__ = 'users'

    uso_id             = db.Column(db.Integer, primary_key = True)
    user_id            = db.Column(db.Integer, unique  = True)
    count300           = db.Column(db.Integer, default = 0)
    count100           = db.Column(db.Integer, default = 0)
    count50            = db.Column(db.Integer, default = 0)
    playcount          = db.Column(db.Integer, default = 0)
    pp_rank            = db.Column(db.Integer, default = 0)
    count_rank_ss      = db.Column(db.Integer, default = 0)
    count_rank_ssh     = db.Column(db.Integer, default = 0)
    count_rank_a       = db.Column(db.Integer, default = 0)
    count_rank_s       = db.Column(db.Integer, default = 0)
    count_rank_sh      = db.Column(db.Integer, default = 0)
    pp_country_rank    = db.Column(db.Integer, default = 0)
    username           = db.Column(db.String , default = "Unknown")
    country            = db.Column(db.String , default = "NA")

    #TODO add playstyle (for mods)

    ranked_score       = db.Column(db.Float, default = 0.0)
    total_score        = db.Column(db.Float, default = 0.0)
    level              = db.Column(db.Float, default = 0.0)
    pp_raw             = db.Column(db.Float, default = 0.0)
    accuracy           = db.Column(db.Float, default = 0.0)
    pp_average         = db.Column(db.Float, default = 0.0)
    bpm_low            = db.Column(db.Float, default = 0.0)
    bpm_average        = db.Column(db.Float, default = 0.0)
    bpm_high           = db.Column(db.Float, default = 0.0)
    od_average         = db.Column(db.Float, default = 0.0)
    ar_average         = db.Column(db.Float, default = 0.0)
    cs_average         = db.Column(db.Float, default = 0.0)
    len_average        = db.Column(db.Float, default = 0.0)
    playstyle          = db.Column(db.Float, default = 0.5)
    last_update        = db.Column(db.Date , default = datetime.datetime.now())