# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
import codecs, json
import datetime, uuid
import MySQLdb
import MySQLdb.cursors

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

'''
    存储数据到MySQL数据库中，需要在settings.py中配置相关参数
    (1)MYSQL_HOST = '192.168.3.63'  #数据库地址
    (2)MYSQL_DBNAME = 'aqi'         #数据库名字
    (3)MYSQL_USER = 'root'          #数据库账号
    (4)MYSQL_PASSWD = 'power2000'   #数据库密码
    (5)MYSQL_PORT = 3306            #数据库端口
'''
class MySQLStoreDataPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,)
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    #将每行更新或写入数据库中
    def _conditional_insert(self, conn, item):
        self.saveCityData(conn, item)
        self.saveCityLiveData(conn, item['live_data'])
        self.saveCitySiteData(conn, item['site_data'])

    #插入城市的数据到tbl_all_city中
    def saveCityData(self, conn, item):
        conn.execute("""
                select 1 from tbl_all_city where city_pinyin = %s
        """, (item['city_pinyin'],))
        ret0 = conn.fetchone()
        if not ret0:
            ret1 = conn.execute("""
                insert into tbl_all_city(city_pinyin, city_name, home_link) values(%s, %s, %s)
            """, (item['city_pinyin'], item['city_name'], item['home_link'],))
            log.msg('save to tbl_all_city: %s' % ret1, level=log.INFO)

    #插入城市的概况数据到tbl_live_data中
    def saveCityLiveData(self, conn, live_item):
        conn.execute("""
                select 1 from tbl_live_data where city_pinyin = %s and time_point = %s
        """, (live_item['city_pinyin'], live_item['time_point'],))
        ret0 = conn.fetchone()
        if not ret0:
            ret1 = conn.execute("""
                    insert into tbl_live_data(id, pm2_5_1h, no2_1h, o3_1h, so2_1h, quality, primary_pollutant, pm10_1h, city_name, city_pinyin, action, affect, o3_8h, data_unit, aqi, time_point, co_1h)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (str(uuid.uuid1()), live_item['pm2_5_1h'], live_item['no2_1h'], live_item['o3_1h'], live_item['so2_1h'], live_item['quality'], live_item['primary_pollutant'], live_item['pm10_1h'], live_item['city_name'], live_item['city_pinyin'], live_item['action'], live_item['affect'], live_item['o3_8h'], live_item['data_unit'], live_item['aqi'], live_item['time_point'], live_item['co_1h'],))
            log.msg('save to tbl_live_data: %s' % ret1, level=log.INFO)

    #插入城市的概况数据到tbl_live_data中
    def saveCitySiteData(self, conn, items):
        for site_item in items:
            conn.execute("""
                    select 1 from tbl_live_data_sites where city_pinyin = %s and time_point = %s and site_name = %s
            """, (site_item['city_pinyin'], site_item['time_point'], site_item['site_name'],))
            ret0 = conn.fetchone()
            if not ret0:
                ret1 = conn.execute("""
                    insert into tbl_live_data_sites(id, city_name, city_pinyin, site_name, pm10, pm2_5, co, o3_8h, so2, o3_1h, no2, primary_pollutant, aqi, time_point, data_unit, quality)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (str(uuid.uuid1()), site_item['city_name'], site_item['city_pinyin'], site_item['site_name'], site_item['pm10'], site_item['pm2_5'], site_item['co'], site_item['o3_8h'], site_item['so2'], site_item['o3_1h'], site_item['no2'], site_item['primary_pollutant'], site_item['aqi'], site_item['time_point'], site_item['data_unit'], site_item['quality'],))
                log.msg('save to tbl_live_data_sites: %s' % ret1, level=log.INFO)

    #异常处理
    def handle_error(self, e):
        log.err(e)

class JSONStoreDataPipeline(object):
    def __init__(self):
        #获得当前时间
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y%m%d%H%M%S")
        self.file = codecs.open(otherStyleTime+'.json', 'w', encoding='utf-8')#保存为json文件

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line) #写入文件中
        return item

    def spider_closed(self, spider):#爬虫结束时关闭文件
        self.file.close()
