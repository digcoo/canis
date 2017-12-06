#encoding=utf-8
import os
import traceback
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import time


def get_university_names():

    try:

	input = open('全国大学列表.txt', 'r')

	text = input.read()

	names = text.split('\n')
	
	return names

    except Exception, e:
	traceback.print_exc()


def get_university_logo(name):
    try:
	base_url = 'https://baike.baidu.com/item/' + name
	html = urllib2.urlopen(base_url)
        bsObj = BeautifulSoup(html,"lxml")
	logo_url = bsObj.find("div",{"class":"summary-pic"}).find("img")["src"]
	print logo_url + '\n'
	return logo_url

    except Exception, e:
	traceback.print_exc()


def download_logo(local_filename, img_url):

    try:

	res = urllib2.urlopen(Request(img_url))

	with open(local_filename,'wb') as f:
	    f.write(res.read())

    except Exception, e:
	traceback.print_exc()



univ_names = get_university_names()
local_path = '/home/ubuntu/git_project/canis/univ_logo/'
for name in univ_names:
    print 'collect university logo, univ_name = ' + name
    logo_url = get_university_logo(name)
    local_filename = ''.join((local_path, str(name).strip(), '.jpg'))
    download_logo(local_filename, logo_url)
#    time.sleep(1)
