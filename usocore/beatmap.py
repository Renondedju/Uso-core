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

from osupy import pyosu

class Beatmap():
    
    def __init__(self, apibeatmap : pyosu.Beatmap):
        
        self.is_empty         = apibeatmap.is_empty
        self.approved         = apibeatmap.approved
        self.approved_date    = apibeatmap.approved_date
        self.last_update      = apibeatmap.last_update
        self.artist           = apibeatmap.artist
        self.beatmap_id       = apibeatmap.beatmap_id
        self.beatmapset_id    = apibeatmap.beatmapset_id
        self.bpm              = apibeatmap.bpm
        self.creator          = apibeatmap.creator
        self.difficultyrating = apibeatmap.difficultyrating
        self.diff_size        = apibeatmap.diff_size
        self.diff_overall     = apibeatmap.diff_overall
        self.diff_approach    = apibeatmap.diff_approach
        self.diff_drain       = apibeatmap.diff_drain
        self.hit_length       = apibeatmap.hit_length
        self.source           = apibeatmap.source
        self.genre_id         = apibeatmap.genre_id
        self.language_id      = apibeatmap.language_id
        self.title            = apibeatmap.title
        self.total_length     = apibeatmap.total_length
        self.version          = apibeatmap.version
        self.file_md5         = apibeatmap.file_md5
        self.mode             = apibeatmap.mode
        self.tags             = apibeatmap.tags
        self.favourite_count  = apibeatmap.favourite_count
        self.playcount        = apibeatmap.playcount
        self.passcount        = apibeatmap.passcount
        self.max_combo        = apibeatmap.max_combo

        self.aim_stars        = 0
        self.speed_stars      = 0
        self.playstyle        = 0.5 # 0 = aim (jumps) , 1 = speed (stream)

                     #  acc    mods pp. Every field in the dict is an int value
        self.pp = {} # {100 : {HD : 50, HDDT : 64}, 99 ...}