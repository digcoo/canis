#encoding=utf-8
import os
import codecs
import traceback
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import time
from MysqlClient import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_university_urls():

    try:


	base_url = 'http://gkcx.eol.cn/schoolhtm/specialty/specialtyList/specialty{0}.htm'


	urls = []

	for i in range(1, 9999):
	    urls.append(base_url.format(str(i)))

	return urls

    except Exception, e:
	traceback.print_exc()


def get_university_specialist(url):

    try:

	print "*" * 120

        html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
        univ_name = bsObj.find("p",{"class":"li-school-label"}).find("span").text
	univ_specialist =  [item.text for item in  bsObj.find("ul", {"class":"li-major grid"}).findAll("li")]

	print "univ_name:\t" + univ_name
	print "univ_specialist:\t" + jsonpickle.encode(univ_specialist)
	return {"univ_name":univ_name,  "univ_specialist":univ_specialist}

    except Exception, e:
	traceback.print_exc()


def write_to_file(file_name, text):
    final_file_name = os.getcwd()  + '/univ_specialist/' + file_name
    update_file = codecs.open(final_file_name, 'w', 'utf-8')
    update_file.write(text)
    update_file.close()



university_urls = get_university_urls()
for url in university_urls[3300:]:
    print url
    university_specialist = get_university_specialist(url)
    if university_specialist is not None:
	write_to_file(university_specialist['univ_name'] + ".txt",  jsonpickle.encode(university_specialist['univ_specialist']))
#    time.sleep(2)
#    MysqlClient.get_instance().add_batch_university_specialist(special_list)


#university_specialist = get_university_specialist('http://gkcx.eol.cn/schoolhtm/specialty/specialtyList/specialty76.htm')
#write_to_file(university_specialist['univ_name'] + ".txt",  jsonpickle.encode(university_specialist['univ_specialist']))
