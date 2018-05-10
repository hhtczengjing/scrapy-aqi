# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import Pm25ResultItem
from tutorial.items import Pm25CityItem
from tutorial.items import Pm25CityLiveDataItem
from tutorial.items import Pm25CityLiveSiteDataItem

class Pm25Spider(scrapy.Spider):
    name = "pm25"
    allowed_domains = ["pm25.in"]

    def start_requests(self):
        yield scrapy.Request('http://www.pm25.in/', self.parse_city)

    def parse_city(self, response):
        sel = scrapy.Selector(response)
        citys = sel.xpath("//div[@class='all']/div[@class='bottom']/ul[@class='unstyled']/div[2]/li")
        for city in citys:
            item = Pm25CityItem()
            href = ''.join(city.xpath('a/@href').extract()).strip()
            item['name'] = ''.join(city.xpath('a/text()').extract()).strip().encode("UTF-8")
            item['link'] = 'http://www.pm25.in' + href
            item['pinyin'] = href.split('/')[1]
            yield scrapy.Request(item['link'], meta={'city': item}, callback=self.parse_data)

    def parse_data(self, response):
        city_item = response.meta['city']
        self.log("开始采集[%s]城市的数据:" % city_item['name'])
        # 开始解析数据
        live_data_item = self.parse_city_live_data(response)
        site_data_items = self.parse_city_site_data(response, live_data_item)
        # 组装数据
        result_item = Pm25ResultItem()
        result_item['city_name'] = city_item['name']
        result_item['city_pinyin'] = city_item['pinyin']
        result_item['home_link'] = city_item['link']
        result_item['live_data'] = dict(live_data_item)
        result_item['site_data'] = site_data_items
        result_item['time_point'] = live_data_item['time_point']
        result_item['data_unit'] = live_data_item['data_unit']
        self.log("采集[%s]城市的数据完成" % city_item['name'])
        return result_item

    def parse_city_live_data(self, response):
        city_item = response.meta['city']
        self.logger.info("start parse %s live data." % city_item['name'])
        # 开始解析数据
        sel = scrapy.Selector(response)
        # 解析当前城市的实时数据
        live_data_item = Pm25CityLiveDataItem()
        live_data = sel.xpath("//div[@class='span12 avg']")[0]
        #  实时数据 --> 城市名称、空气质量等级
        city_name = ''.join(live_data.xpath("//div[1]/div[@class='city_name']/h2/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        level = ''.join(live_data.xpath("//div[1]/div[@class='level']/h4/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_item['city_name'] = city_name
        live_data_item['city_pinyin'] = city_item['pinyin']
        live_data_item['quality'] = level
        #  实时数据 --> 数据更新时间、数值单位
        live_data_time = ''.join(live_data.xpath("//div[2]/div[@class='live_data_time']/p/text()").extract()).strip().encode("UTF-8").split('：')[1].replace('\n', '')
        live_data_unit = ''.join(live_data.xpath("//div[2]/div[@class='live_data_unit']/text()").extract()).strip().encode("UTF-8").split('：')[1].replace('\n', '').replace(' ', '')
        live_data_item['time_point'] = live_data_time
        live_data_item['data_unit'] = live_data_unit
        #  实时数据 --> AQI、PM2.5/1h、PM10/1h、CO/1h、NO2/1h、O3/1h、O3/8h、SO2/1h
        live_data_aqi = ''.join(live_data.xpath("//div[3]/div[1]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_pm25_1h = ''.join(live_data.xpath("//div[3]/div[2]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_pm10_1h = ''.join(live_data.xpath("//div[3]/div[3]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_co_1h = ''.join(live_data.xpath("//div[3]/div[4]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_no2_1h = ''.join(live_data.xpath("//div[3]/div[5]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_o3_1h = ''.join(live_data.xpath("//div[3]/div[6]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_o3_8h = ''.join(live_data.xpath("//div[3]/div[7]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_so2_1h = ''.join(live_data.xpath("//div[3]/div[8]/div[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
        live_data_item['aqi'] = live_data_aqi
        live_data_item['pm2_5_1h'] = live_data_pm25_1h
        live_data_item['pm10_1h'] = live_data_pm10_1h
        live_data_item['co_1h'] = live_data_co_1h
        live_data_item['no2_1h'] = live_data_no2_1h
        live_data_item['o3_1h'] = live_data_o3_1h
        live_data_item['o3_8h'] = live_data_o3_8h
        live_data_item['so2_1h'] = live_data_so2_1h
        #  实时数据 --> 首要污染物、对健康影响情况、建议采取的措施
        primary_pollutant = ''.join(live_data.xpath("//div[4]/div[@class='primary_pollutant']/p/text()").extract()).strip().encode("UTF-8").split('：')[1].replace('\n', '').replace(' ', '')
        affect = ''.join(live_data.xpath("//div[4]/div[@class='affect']/p/text()").extract()).strip().encode("UTF-8").split('：')[1].replace('\n', '').replace(' ', '')
        action = ''.join(live_data.xpath("//div[4]/div[@class='action']/p/text()").extract()).strip().encode("UTF-8").split('：')[1].replace('\n', '').replace(' ', '')
        live_data_item['primary_pollutant'] = primary_pollutant
        live_data_item['affect'] = affect
        live_data_item['action'] = action
        return live_data_item

    def parse_city_site_data(self, response, live_data_item):
        city_item = response.meta['city']
        self.logger.info("start parse %s site data." % city_item['name'])
        # 开始解析数据
        sel = scrapy.Selector(response)
        # 解析站点的数据
        site_data_items = []
        site_data_tables = sel.xpath("//*[@id='detail-data']/tbody/tr")
        for site_data_table in site_data_tables:
            site_data_item = Pm25CityLiveSiteDataItem()
            site_data_item['city_name'] = live_data_item['city_name']
            site_data_item['city_pinyin'] = live_data_item['city_pinyin']
            site_data_item['time_point'] = live_data_item['time_point']
            site_data_item['data_unit'] = live_data_item['data_unit']
            site_data_item['site_name'] = ''.join(site_data_table.xpath("td[1]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['aqi'] = ''.join(site_data_table.xpath("td[2]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['quality'] = ''.join(site_data_table.xpath("td[3]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['primary_pollutant'] = ''.join(site_data_table.xpath("td[4]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['pm2_5'] = ''.join(site_data_table.xpath("td[5]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['pm10'] = ''.join(site_data_table.xpath("td[6]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['co'] = ''.join(site_data_table.xpath("td[7]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['no2'] = ''.join(site_data_table.xpath("td[8]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['o3_1h'] = ''.join(site_data_table.xpath("td[9]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['o3_8h'] = ''.join(site_data_table.xpath("td[10]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_item['so2'] = ''.join(site_data_table.xpath("td[11]/text()").extract()).strip().encode("UTF-8").replace(' ', '').replace('\n', ' ')
            site_data_items.append(dict(site_data_item))
        return site_data_items
