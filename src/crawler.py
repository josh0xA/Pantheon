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
import requests
import re
import concurrent.futures
from headers.agents import Agents
from src.config import PantheonConfiguration
import random

class PantheonProxy(object):
    def init(self, proxy, use_proxy):
        self.proxy = {}
        self.use_proxy = use_proxy

    def assign_proxy(self):
        proxy_req = requests.get(PantheonConfiguration.proxy_api)
        if proxy_req.status_code == PantheonConfiguration.PANTHEON_REQUESTS_SUCCESS_CODE:
            for line in proxy_req.text.splitlines():
                if line:
                    proxy = line.split(':')
                    self.proxy["http"] = "http://" + proxy[0] + ':' + proxy[1]
        else: pass

    def get_proxy(self):
        return self.proxy["http"]

    def get_proxy_dict(self):
        return self.proxy

class PantheonWebcam:
    @staticmethod
    def crawl(country):
        cfg = PantheonConfiguration()
        user_agent = {
            'User-Agent': random.choice(Agents.useragent)
        }
        base_url = f'http://www.insecam.org/en/bycountry/{country}/?page='
        with requests.Session() as session:
            webcam_pattern = re.compile(r'http://\d+.\d+.\d+.\d+:\d+/')
            def fetch_page(page):
                req_main = session.get(base_url + str(page), headers=user_agent)
                req_source = req_main.text

                webcams = webcam_pattern.findall(req_source)
                cfg.webcams_found.extend(webcams)

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(fetch_page, range(1, cfg.PANTHEON_DEFAULT_COUNT))
