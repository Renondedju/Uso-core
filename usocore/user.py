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

class User():
    
    def __init__(self, apiuser = pyosu.models.User):
        
        self.apisuer = apiuser

        #User performances
        self.accuracy_average   = 0
        self.pp_average         = 0
        self.bpm_low            = 0
        self.bpm_average        = 0
        self.bpm_high           = 0
        self.od_average         = 0
        self.ar_average         = 0
        self.cs_average         = 0
        self.len_average        = 0   # Drain
        self.playstyle          = 0.5 # Jumps 0 -----|----- 1 Stream
        self.last_update        = datetime(1970, 1, 1)

        # This is the last core patch used to display updates if needed
        self.last_patch_used    = "0.0.0"

        # Every value in the dict is an int value
        # {HD : 20, HDDT : 60, ...}
        self.playrate    = {}

        # Every value in the dict is an int value
        # mods :  beatmaps id recommended in this mods
        #  {HD : [123456, 456789, 132456, ...], HDDT : [...], ...}
        self.recommended = {}

    