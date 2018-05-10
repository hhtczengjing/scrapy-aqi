# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Pm25ResultItem(scrapy.Item):
    city_name   = scrapy.Field() #城市的名称
    city_pinyin = scrapy.Field() #城市的拼音
    home_link   = scrapy.Field() #主页链接
    live_data   = scrapy.Field() #实时数据
    site_data   = scrapy.Field() #站点数据
    time_point  = scrapy.Field() #数据更新时间
    data_unit   = scrapy.Field() #数值单位

class Pm25CityItem(scrapy.Item):
    name = scrapy.Field() #城市的名称
    link = scrapy.Field() #对应数据的链接地址
    pinyin = scrapy.Field() #城市的拼音

class Pm25CityLiveDataItem(scrapy.Item):
    city_name           = scrapy.Field() #城市的名称
    city_pinyin         = scrapy.Field() #城市的拼音
    quality             = scrapy.Field() #空气质量指数类别，有“优、良、轻度污染、中度污染、重度污染、严重污染”6类
    time_point          = scrapy.Field() #数据更新时间
    data_unit           = scrapy.Field() #数值单位
    aqi                 = scrapy.Field() #AQI,空气质量指数(AQI)，即air quality index，是定量描述空气质量状况的无纲量指数
    pm2_5_1h            = scrapy.Field() #PM2.5/1h,颗粒物（粒径小于等于2.5μm）1小时平均
    pm10_1h             = scrapy.Field() #PM10/1h,颗粒物（粒径小于等于10μm）1小时平均
    co_1h               = scrapy.Field() #CO/1h,一氧化碳1小时平均
    no2_1h              = scrapy.Field() #NO2/1h,二氧化氮1小时平均
    o3_1h               = scrapy.Field() #O3/1h,臭氧1小时平均
    o3_8h               = scrapy.Field() #O3/8h,臭氧8小时滑动平均
    so2_1h              = scrapy.Field() #SO2/1h,二氧化硫1小时平均
    primary_pollutant   = scrapy.Field() #首要污染物
    affect              = scrapy.Field() #对健康影响情
    action              = scrapy.Field() #建议采取的措施

class Pm25CityLiveSiteDataItem(scrapy.Item):
    city_name           = scrapy.Field() #城市的名称
    city_pinyin         = scrapy.Field() #城市的拼音
    time_point          = scrapy.Field() #数据更新时间
    data_unit           = scrapy.Field() #数值单位
    site_name           = scrapy.Field() #监测点
    quality             = scrapy.Field() #空气质量指数类别，有“优、良、轻度污染、中度污染、重度污染、严重污染”6类
    aqi                 = scrapy.Field() #AQI,空气质量指数(AQI)，即air quality index，是定量描述空气质量状况的无纲量指数
    primary_pollutant   = scrapy.Field() #首要污染物
    pm2_5               = scrapy.Field() #PM2.5,颗粒物（粒径小于等于2.5μm）
    pm10                = scrapy.Field() #PM10,颗粒物（粒径小于等于10μm）
    co                  = scrapy.Field() #CO,一氧化碳
    no2                 = scrapy.Field() #NO2,二氧化氮
    o3_1h               = scrapy.Field() #O3/1h,臭氧1小时平均
    o3_8h               = scrapy.Field() #O3/8h,臭氧8小时滑动平均
    so2                 = scrapy.Field() #SO2，二氧化硫
