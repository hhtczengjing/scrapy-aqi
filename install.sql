CREATE DATABASE `aqi`;

CREATE TABLE `tbl_live_data` (
  `id` varchar(50) NOT NULL,
  `pm2_5_1h` varchar(50) DEFAULT NULL,
  `no2_1h` varchar(50) DEFAULT NULL,
  `o3_1h` varchar(50) DEFAULT NULL,
  `so2_1h` varchar(50) DEFAULT NULL,
  `quality` varchar(100) DEFAULT NULL,
  `primary_pollutant` varchar(500) DEFAULT NULL,
  `pm10_1h` varchar(50) DEFAULT NULL,
  `city_name` varchar(100) DEFAULT NULL,
  `city_pinyin` varchar(100) DEFAULT NULL,
  `action` varchar(500) DEFAULT NULL,
  `affect` varchar(500) DEFAULT NULL,
  `o3_8h` varchar(50) DEFAULT NULL,
  `data_unit` varchar(100) DEFAULT NULL,
  `aqi` varchar(50) DEFAULT NULL,
  `time_point` varchar(50) DEFAULT NULL,
  `co_1h` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `time_point` (`time_point`) USING BTREE,
  KEY `city_pinyin` (`city_pinyin`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tbl_live_data_sites` (
  `id` varchar(50) NOT NULL,
  `city_name` varchar(100) DEFAULT NULL,
  `city_pinyin` varchar(100) DEFAULT NULL,
  `site_name` varchar(100) DEFAULT NULL,
  `pm10` varchar(50) DEFAULT NULL,
  `pm2_5` varchar(50) DEFAULT NULL,
  `co` varchar(50) DEFAULT NULL,
  `o3_8h` varchar(50) DEFAULT NULL,
  `so2` varchar(50) DEFAULT NULL,
  `o3_1h` varchar(50) DEFAULT NULL,
  `no2` varchar(50) DEFAULT NULL,
  `primary_pollutant` varchar(500) DEFAULT NULL,
  `aqi` varchar(50) DEFAULT NULL,
  `time_point` varchar(50) DEFAULT NULL,
  `data_unit` varchar(100) DEFAULT NULL,
  `quality` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `time_point` (`time_point`) USING BTREE,
  KEY `city_pinyin` (`city_pinyin`) USING BTREE,
  KEY `site_name` (`site_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;