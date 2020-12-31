#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging
import re
import requests

# Get magnet urls from "meijutt.tv"
def get_magnets_meijutt(url):
    try:
        page_txt = requests.get(url).text
    except Exception as e:
        logging.error('[get_magnets_meijutt]requests get failed.(%s)', e)
        return None

    text_with_download_url_list = re.findall(r'class="tabs-list.*?">(.*?)<!--/Tabs List-->', page_txt)

    text_with_type_and_quality_list = re.findall(r'<div class="tabs from-tabs">(.*?)</div>', page_txt)
    if text_with_type_and_quality_list == None:  # Ideally, only one should found.
        logging.error('[get_magnets_meijutt]None from re.(text_with_type_and_quality_list).')
        return None
    download_type_list = re.findall(r'<label class="(.*?)">.*?</label>', text_with_type_and_quality_list[0])
    picture_type_list = re.findall(r'<label class=".*?">(.*?)</label>', text_with_type_and_quality_list[0])
    if (download_type_list == None) or (picture_type_list == None):
        logging.error('[get_magnets_meijutt]None from re.(download_type_list or/and picture_type_list).')
        return None

    pos = -1
    magnet_pos_list = []
    for download_type in download_type_list:
        pos = pos + 1
        if download_type == 'downcili-ico' or download_type == 'downcili-ico current':
            magnet_pos_list.append(pos)
    if len(magnet_pos_list) == 0:
        return None

    for pos in magnet_pos_list:
        if picture_type_list[pos] == 'ÖÐ×Ö1080P':   # 中字1080P
            return re.findall(r'value="(.*?)" file_name=', text_with_download_url_list[pos])
    for pos in magnet_pos_list:
        if picture_type_list[pos] == 'ÖÐ×Ö720P':   # 中字720P
            return re.findall(r'value="(.*?)" file_name=', text_with_download_url_list[pos])
    # Else, use first as default.
    return re.findall(r'value="(.*?)" file_name=', text_with_download_url_list[magnet_pos_list[0]])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s]:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    url = 'https://www.meijutt.tv/content/meiju21858.html'
    print(get_magnets_meijutt(url))