'''
MIT License

Copyright (c) 2021 Josh Schiavone

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
from src.config import PantheonConfiguration

class PantheonLogger:
    def __init__(self, logfile):
        self.logfile = logfile

    def log(self, scan_contents):
        with open(self.logfile, 'a') as f:
            for line in scan_contents:
                f.write(f"{str(line)}\n")
        f.close()

    def log_text(self, text):
        with open(self.logfile, 'a') as f:
            f.write(f'{text}\n')
        f.close()

    def log_info(self, info):
        with open(self.logfile, 'a') as f:
            f.write(f'[INFO] {info}\n')
        f.close()
