# PantheonWebcam.py
import requests
import re
import concurrent.futures
from config import PantheonConfiguration
from headers.agents import Agents
import random

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
