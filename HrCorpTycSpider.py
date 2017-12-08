#encoding=utf-8
import os
import sys
import traceback
import urllib
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import time
import jsonpickle
from MysqlClient import *


send_headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
	'Cookie':'TYCID=84db9ca0da8511e7b939739ce762c285; undefined=84db9ca0da8511e7b939739ce762c285; ssuid=9270378770; aliyungf_tc=AQAAAIBGGXHiegUAwPSh08uvaIEuJTTb; csrfToken=A0pPWVxTvO5PEKI6RLiSz0pa; _csrf=qDl0VLwBHOeYS7MghkIP4g==; OA=eRomgnd63pxCrSvQHf6IRdXZU1KUTPIZVkWZfYx0n1gynJxiXkoNzDa7iM4Th9HIKmHywJLTMuhLap0IPAG1m8iJOe5gywecn3DPnEZta/c=; _csrf_bk=13608bbac8afd3111b72a7cbf1f69874; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1512565365; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1512565412'
}

def get_city_symbol_map():

    try:

        category_urls = []

        base_url = 'https://www.tianyancha.com/search?key={0}&searchType=company'

        req = urllib2.Request(base_url.format('人力资源'), headers=send_headers)

	html = urllib2.urlopen(req)

        bsObj = BeautifulSoup(html,"lxml")
	city_url_map = {}
        items = bsObj.findAll("a",{"class":"new-list"})
	print 'city_url_size = ' + str(len(items))
	for item in items:
	    city_name = item.text.strip()
	    orgin_href = item["href"]
	    city_symbol = orgin_href[orgin_href.find('/')+2: orgin_href.find('.')]
	    city_url_map[city_name] = city_symbol
	return city_url_map

    except Exception, e:
	traceback.print_exc()


def get_city_corp_list(city_symbol):
    try:
	base_url = 'https://{0}.tianyancha.com/search/p{1}?key={2}&searchType=company'
	page = 1
	keyword = urllib.quote('人力资源'.decode(sys.stdin.encoding).encode('utf8'))
	url = base_url.format(city_symbol, page, keyword)
	corps = get_page_corp_list(url)
	print 'city_corps_size = ' + str(len(corps))	
	while corps is not None and len(corps) > 0:
	    #process corps persist
	    print "collect base_url = {0}, page = {1}, corp_num = {2}".format(base_url, page, len(corps))
	    MysqlClient.get_instance().add_batch_hr_corps(corps)

	    page += 1
	    url = base_url.format(city_symbol, page, keyword)
	    corps = get_page_corp_list(url)
	    time.sleep(1)


    except Exception, e:
	traceback.print_exc()

def get_page_corp_list(url):
    try:
	
	time.sleep(2)

	print 'page_corp_url : ' + url

        req = urllib2.Request(url, headers=send_headers)

        html = urllib2.urlopen(req)

        bsObj = BeautifulSoup(html,"lxml")

        items = bsObj.findAll("div",{"class":"search_right_item"})

	corps = []
	if items is not None and len(items) > 0:
	    for item in items:
		corp_name = item.find("a", {"class":"query_name"}).text
		corp_rigister_info = item.find("div", {"class":"search_row_new"}).text

		print 'corp_name:\t' + corp_name
		print 'corp_rigister_info:\t' + corp_rigister_info
		print '*' * 120

		corps.append({"name":corp_name, "rigister_info":corp_rigister_info})
	return corps

    except Exception, e:
	traceback.print_exc()

city_symbol_maps = get_city_symbol_map()
city_index = 0
for city_name in city_symbol_maps.keys()[200:300]:
    get_city_corp_list(city_symbol_maps[city_name])
    city_index = city_index + 1
    print city_name + ':' + city_symbol_maps[city_name] + ', city_index = ' + str(city_index)

#get_page_corp_list('https://chenzhou.tianyancha.com/search/p1?key=%E4%BA%BA%E5%8A%9B%E8%B5%84%E6%BA%90&searchType=company')
