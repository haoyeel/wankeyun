#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64
import json
import logging
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL_BASE = '''https://xlact.onethingpcs.com/open/d2wky/dist/pc/?url='''

class DownloaderWky(object):
    def __init__(self, interval=0.5):
        logging.info('Wankeyun downloader initting...')
        self._interval = interval

        self._username = self._get_account_info('username')
        self._passwd = self._get_account_info('passwd')

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        self._driver = webdriver.Chrome(chrome_options=chrome_options)
        self._driver.get(URL_BASE)
        time.sleep(self._interval)

        self._driver.find_element_by_xpath("//a[@class='link-login']").click()
        time.sleep(self._interval)
        self._driver.find_element_by_xpath("//input[@id='account']").send_keys(self._username)
        self._driver.find_element_by_xpath("//input[@id='password']").send_keys(self._passwd)
        self._driver.find_element_by_xpath("//a[@class='btn btn-login']").click()
        time.sleep(self._interval)
        logging.info('Wankeyun downloader init OK.')
    
    def __del__(self):
        self._driver.quit()
        logging.info('Wankeyun downloader quit OK.')

    def _get_account_info(self, config_type):
        try:
            with open('config.json', 'r') as fd_config_file:
                config = json.loads(fd_config_file.read())
                if config_type != None:
                    config = config[config_type]
                return config
        except Exception:
            logging.error('No configuration file: config.json.')
            return None

    def _do_download(self, magnet):
        mag_base64 = str(base64.b64encode(magnet.encode('utf-8')),'utf-8')
        self._driver.get(URL_BASE + mag_base64)

        self._driver.find_element_by_xpath("//div[@id='login-download-button']").click()
        time.sleep(self._interval)
    
    def download(self, magnets):
        if type(magnets) is str:
            magnets = [magnets]

        cnt = 1
        num = len(magnets)
        for magnet in magnets:
            logging.info('Wankeyun downloading... (%s/%s)' % (cnt, num))
            self._do_download(magnet)
            logging.info('Wankeyun downloaded.... (%s/%s)' % (cnt, num))
            cnt = cnt + 1

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s]:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    magnet = '''magnet:?xt=urn:btih:14271fdc6bbc4b1b1b36dc07fbf4a667873aa0ee&tr=http://tr.cili001.com:8070/announce&tr=udp://p4p.arenabg.com:1337&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://open.demonii.com:1337'''
    dl = DownloaderWky()
    dl.download(magnet)
