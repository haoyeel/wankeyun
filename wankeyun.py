#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging
import sys, getopt

from downloader import DownloaderWky
from urlspider import get_magnets_meijutt

def main():
    argv = sys.argv[0:]
    if len(argv) < 2:
        logging.error('No url specified. stop.')
        return False
    url = argv[1]

    dl = DownloaderWky()
    magnet_list = get_magnets_meijutt(url)
    dl.download(magnet_list)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s]:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    main()
