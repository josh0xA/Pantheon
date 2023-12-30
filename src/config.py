'''
MIT License

Copyright (c) 2023 Josh Schiavone

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
import tkinter as tk

class PantheonConfiguration:

    PANTHEON_ERROR_CODE_STANDARD = -1
    PANTHEON_SUCCESS_CODE_STANDARD = 0
    PANTHEON_OS = ""
    PANTHEON_REQUESTS_SUCCESS_CODE = 200
    PANTHEON_PROXY = False
    PANTHEON_DEFAULT_COUNT = 0
    webcams_found = []
    intel_map_webcams_found = []
    intel_markers = []
    num_webcams_found = 0
    just_ip_addresses = []

    proxy_api = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite"

    controls = {
        'view-feed': "[Enter]",
        'view-http': "Right-click (Win/Linux) or Control-click (Mac)",
        'verbosity': "Adjust verbosity slider for more results", 
        'save-crawl': "Pantheon File Controller -> Save Pantheon Crawl",
        'load-crawl': "Pantheon File Controller -> Load Pantheon Crawl",
        'search-http': "Use the search bar on the HTTP window to search for keywords"
    }

    @staticmethod 
    def pantheon_icon_handler(root):
        if PantheonConfiguration.PANTHEON_OS == "Windows":
            root.iconbitmap("imgs/pantheon_icon.ico")
        if PantheonConfiguration.PANTHEON_OS == "Linux":
            root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='imgs/pantheon_icon.png'))
        if PantheonConfiguration.PANTHEON_OS == "Darwin":
            img = tk.Image("photo", file="imgs/pantheon_icon.png")
            root.call('wm', 'iconphoto', root._w, img)
        else:
            return None
    