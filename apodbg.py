#! /usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import print_function
import urllib2
import subprocess
import os

APOD_URL = 'http://apod.nasa.gov/apod/'


def get_html_contents(url):
    return urllib2.urlopen(url).read()


def get_text_between_tokens(s, start, end):
    start_pos = s.find(start) + len(start)
    end_pos = s.find(end, start_pos)
    return s[start_pos:end_pos]


def get_latest_apod_url():
    html = get_html_contents(APOD_URL)
    start_token = '<IMG SRC=\"'
    end_token = '\"'
    img_url = get_text_between_tokens(html, start_token, end_token)
    return APOD_URL + img_url


def download_image(url, filename):
    with open(filename, 'w') as imgfile:
        imgfile.write(get_html_contents(url))


def set_as_wallpaper(img_filename):
    img_uri = 'file://' + os.path.abspath(img_filename)
    subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
                     'picture-uri', img_uri])


if __name__ == '__main__':
    filename = 'latest.jpg'
    try:
        img_url = get_latest_apod_url()
        download_image(img_url, filename)
        set_as_wallpaper(filename)
    except:
        print('Could not download image')
