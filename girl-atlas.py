#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import requests
from lxml import html
import re

def get_response(url):
    headers = \
        {'headers': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response

def download_image(album_dirs):
    url_prefix = 'http://girl-atlas.com/'
    for album_dir in album_dirs:
        album_url = url_prefix + album_dir
        response = get_response(album_url)
        parsed_body = html.fromstring(response.text)
        album_title = parsed_body.xpath('//title/text()')[0]
        print (album_url)
        print (album_title)




def get_girl_urls(page_urls):
    album_dirs = []
    for url in page_urls:
        response = get_response(url)
        parsed_body = html.fromstring(response.text)
        album = parsed_body.xpath('//h2/a/@href')
        album_dirs.extend(album)
    return album_dirs


def get_page_urls():
    page_urls = []
    start_url = 'http://girl-atlas.com/'
    while True:
        page_urls.append(start_url)
        response = get_response(start_url)
        parsed_body = html.fromstring(response.text)

        # TODO - Need to fix the xpath

        next_url = parsed_body.xpath('//a[@class="btn-form next"]/@href')
        if not next_url:
            break
        next_url = start_url + next_url[0]
        page_urls.append(next_url)
    return page_urls


# Get static configuration

def get_config():
    config = configparser.RawConfigParser()
    config.read('config.ini')
    return config


def main():
    config = get_config()
    page_urls = get_page_urls()
    album_dirs = get_girl_urls(page_urls)
    download_image(album_dirs)


if __name__ == '__main__':
    main()
