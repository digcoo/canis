#encoding=utf-8

import pymysql.cursors
import datetime
import time
import traceback
import jsonpickle

class MysqlClient:

    __instance = None

    @staticmethod
    def get_instance():
        if MysqlClient.__instance is None:
            MysqlClient.__instance = MysqlClient()
        return MysqlClient.__instance

    def __init__(self):
	self.connection = None

    def conn(self):
        try:
            self.connection = pymysql.connect(host='cms-metadata-dev-117.cdslstjgevzs.rds.cn-north-1.amazonaws.com.cn',
                             user='bestv',
                             password='bestvwin',
                             db='anas',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        except Exception, e:
            traceback.print_exc()

    def close(self):
	try:
#	    self.connection.close()
	    print ''
	except Exception, e:
	    traceback.print_exc()

#//////////////////////////////////////////////////////////////////university/////////////////////////////////////////////////////////////////////////


    def add_university(self, university):
        try:
            local_universities = self.query_university_by_name(university['local_name'])
	    if local_universities == None or len(local_universities) == 0:
		self.conn()
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO `digcoo_anas_base_university` (`local_name`, `cn_name`, `nation`,  `logo`, `gmt_created`, `gmt_updated`, `del`) values(%s, %s, %s, %s, now(), now(), 0)"
		    cursor.execute(sql, (university['local_name'], university['cn_name'], university['nation'], university['logo']))
                    self.connection.commit()

        except Exception, e:    
	    traceback.print_exc()
	finally:
	    self.close()



    def query_university_by_name(self, name):
        try:
            self.conn()
            with self.connection.cursor() as cursor:
                sql = "SELECT `id`,`local_name`, `cn_name` from `digcoo_anas_base_university` where `local_name` = %s "
                cursor.execute(sql, (name, ))
                return cursor.fetchall()
        except Exception, e:
            traceback.print_exc()
        return None


    def add_batch_universities(self, universities):
        try:
            for university in universities:
                self.add_university(university)
        except Exception, e:
            traceback.print_exc()
        finally:
            self.close()




#//////////////////////////////////////////////////////////////////corp/////////////////////////////////////////////////////////////////////////


    def add_corp(self, corp):
        try:
            local_corps = self.query_corp_by_name(corp['name'])
            if local_corps == None or len(local_corps) == 0:
                self.conn()
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO `digcoo_anas_base_corp` (`name`, `logo`, `follow`, `industry`, `addr`, `summary`, `gmt_created`, `gmt_updated`, `del`) values(%s, %s, %s, %s, %s, %s, now(), now(), 0)"
                    cursor.execute(sql, (corp['name'], corp['logo'], corp['follow'], corp['industry'], corp['addr'], corp['summary']))
                    self.connection.commit()

        except Exception, e:
            traceback.print_exc()
        finally:
            self.close()



    def query_corp_by_name(self, name):
        try:
            self.conn()
            with self.connection.cursor() as cursor:
                sql = "SELECT `id`,`name`, `logo`, `follow` from `digcoo_anas_base_corp` where `name` = %s "
                cursor.execute(sql, (name, ))
                return cursor.fetchall()
        except Exception, e:
            traceback.print_exc()
        return None


    def add_batch_corps(self, corps):
        try:
	    for corp in corps:
		self.add_corp(corp)
        except Exception, e:
            traceback.print_exc()
        finally:
            self.close()

#//////////////////////////////////////////////////////////////////corp/////////////////////////////////////////////////////////////////////////



#//////////////////////////////////////////////////////////////////hr_corp/////////////////////////////////////////////////////////////////////////

    def add_hr_corp(self, corp):
        try:
            local_corps = self.query_hr_corp_by_name(corp['name'])
            if local_corps == None or len(local_corps) == 0:
                self.conn()
                with self.connection.cursor() as cursor: 
                    sql = "INSERT INTO `digcoo_anas_base_hr_corp` (`name`, `rigister_info`, `gmt_created`, `gmt_updated`, `del`) values(%s, %s, now(), now(), 0)"
                    cursor.execute(sql, (corp['name'], corp['rigister_info']))
                    self.connection.commit()
                
        except Exception, e:
            traceback.print_exc()
        finally:    
            self.close()

                        
    def query_hr_corp_by_name(self, name):
        try:        
            self.conn() 
            with self.connection.cursor() as cursor:
		sql = "SELECT `id`, `name`, `tel`, `email`, `addr` from `digcoo_anas_base_hr_corp` where `name` = %s "
                cursor.execute(sql, (name, ))
                self.connection.commit()
                
        except Exception, e:
            traceback.print_exc()
        finally:
            self.close()
                        
                
    def add_batch_hr_corps(self, corps):
        try:
            for corp in corps:
                self.add_hr_corp(corp)
        except Exception, e:
            traceback.print_exc()
        finally:
	    self.close()

#//////////////////////////////////////////////////////////////////hr_corp/////////////////////////////////////////////////////////////////////////

