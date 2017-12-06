#encoding=utf-8
import os
import traceback
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import time
from MysqlClient import *


def get_university_names():

    try:

	input = open('全国大学列表.txt', 'r')

	text = input.read()

	names = text.split('\n')
	
	return names

    except Exception, e:
	traceback.print_exc()

def compose_university_info(name):
    try:

	university_info = {}
	university_info['local_name'] = name
	university_info['cn_name'] = name

	return university_info

    except Exception, e:
        traceback.print_exc()

names = get_university_names()
for name in names:
    university_info = compose_university_info(name)
    MysqlClient.get_instance().add_university(university_info)
