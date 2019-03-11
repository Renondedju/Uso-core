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

from os      import listdir, makedirs, remove
from os.path import isfile, isdir
from typing  import Set

class Cache:
    """ Cache class.
        Allows for beatmap storage to avoid redownloads.
    """

    def __init__(self, location: str, max_size: int = 1000000):

        self.max_size = max(1, max_size)
        self.location = location
        # Creating the cache if needed
        if not isdir(self.location):
            makedirs(self.location)

        self.content: Set[str] = set(listdir(self.location))

    def update_content_list(self):
        """ Updates the content list
        """

        self.content = set(os.listdir(self.location))

    def clear_cache(self):
        """ Clears the cache if needed (if there is too much files)
        """

        if len(self.content) > self.max_size:
            files_to_remove = self.content[self.max_size:len(self.content) - 1]
            for file in files_to_remove:
                if isfile(self.location + file):
                    remove(self.location + file)

            self.update_content_list()

        return

    def read(self, file_name: str) -> str:
        """ Retruns the requested file content or none if nothing has been found.
        """

        if not file_name in self.content:
            return None

        try:
            with open(self.location + file_name, "rt", encoding='utf-8') as file:
                return file.read()

        # Someone might have deleted files without us noticing it
        # updating the content list.
        except OSError:
            self.update_content_list()
            return None

    def write(self, file_name: str, content: str) -> bool:
        """ Writes the content of a file into the cache.
            False is returned if the operation failed.
        """

        try:
            with open(self.location + file_name, "w+", encoding='utf-8', newline='\n') as file:
                file.write(content)
            self.content.add(file_name)
            self.clear_cache()
            return True

        # Something went wrong when writing the file, attempting to create the cache dir
        # in case of it having been deleted.
        except OSError:
            if not isdir(self.location):
                makedirs(self.location)
            self.update_content_list()
        
        return False