#! /usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import print_function
import urllib2
import subprocess
import os
import datetime
import random
import argparse
import time

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


def get_image_url_from_date(date):
    url = get_url_from_date(date)
    html = get_html_contents(url)
    start_token = '<IMG SRC=\"'
    end_token = '\"'
    img_url = get_text_between_tokens(html, start_token, end_token)
    return APOD_URL + img_url


def download_image(url, filename):
    print('Downloading image from url %s' % url)
    with open(filename, 'w') as imgfile:
        imgfile.write(get_html_contents(url))


def download_image_from_date(date, filename):
    download_image(get_image_url_from_date(date), filename)


def get_url_from_date(date):
    return APOD_URL + 'ap%02d%02d%02d.html' % \
        (date.year % 100, date.month, date.day)


def set_as_wallpaper(img_filename):
    img_uri = 'file://' + os.path.abspath(img_filename)
    subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
                     'picture-uri', img_uri])


def get_random_date():
    MIN_DATE = datetime.date(1995, 6, 20)
    MAX_DATE = datetime.date.today()
    day_count = datetime.date.toordinal(MAX_DATE) - \
        datetime.date.toordinal(MIN_DATE)
    random_ord = datetime.date.toordinal(MIN_DATE) + \
        random.randint(0, day_count-1)
    return datetime.date.fromordinal(random_ord)


if __name__ == '__main__':
    filename = 'img.jpg'
    parser = argparse.ArgumentParser(description='Set an APOD image as \
        wallpaper')
    parser.add_argument('-r', '--random',
                        help='Random image', action='store_true')
    parser.add_argument('-p', '--period',
                        help='Change image each <period> seconds.', type=int)
    args = parser.parse_args()

    # Random image
    if args.random:
        print('Random image')
        date = get_random_date()
        print('Downloading image from date %s' % date.isoformat())
        try:
            download_image_from_date(date, filename)
            set_as_wallpaper(filename)
        except:
            print('Could not download image')

    # Change image periodically
    elif args.period is not None:
        while True:
            date = get_random_date()
            print('Downloading image from date %s' % date.isoformat())
            try:
                download_image_from_date(date, filename)
                set_as_wallpaper(filename)
            except:
                print('Could not download image')
                continue
            time.sleep(args.period)

    # Latest image
    else:
        try:
            img_url = get_latest_apod_url()
            download_image(img_url, filename)
            set_as_wallpaper(filename)
        except:
            print('Could not download image')
