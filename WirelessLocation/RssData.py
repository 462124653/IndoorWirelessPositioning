import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "indoorwrielesslocation")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()


class DataBase:
    def RssInsert(self, mac_address, wifi_name, rss_value, data_time, place, collect_count):
        try:
            cursor.execute('insert into collection_data(`mac_address`,`wifi_name`,`rss_value`,`data_time`,`place`,`collect_count`) values ("%s", "%s","%s","%s","%s","%d")' % \
                           (mac_address, wifi_name, rss_value, data_time, place, collect_count))
            db.commit()
            print("插入成功！")
        except:
            print("插入失败！")
            db.rollback()

    def RssSelect(self, place, collect_count):
        sql = "select mac_address,rss_value from collection_data where place = '%s' and collect_count = '%d'" % \
              (place, collect_count)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            # print("取值成功！")
        except:
            print("取值失败！")
            db.rollback()
        else:
            return results

    def FingerDataInsert(self, mac_address, rss_value, data_time, place, collect_count, room):
        try:
            cursor.execute('insert into finger_data(`place`,`mac_address`,`rss_value`,`data_time`,`collect_count`,`room`) values ("%s", "%s","%s","%s","%d","%s")' % \
                           (mac_address, rss_value, data_time, place, collect_count, room))
            db.commit()
            # print("插入成功！")
        except:
            print("插入失败！")
            db.rollback()

    def FingerDataSelcet(self, place):
        sql = "select `mac_address`,`rss_value` from `finger_data` where `place` = '%s' " % \
              place
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print("取值成功！")
        except:
            print("读取数据失败！")
            db.rollback()
        else:
            return results

    def FingerMacAdressDataSelcet(self, mac_address):
        sql = "select `rss_value`,`place`,`collect_count` from `finger_data` where `mac_address` = '%s' " % \
              mac_address
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            # print("取值成功！")
        except:
            print("读取数据失败！")
            db.rollback()
        else:
            return results

    def PlaceAPCount(self):
        sql = "select place,sum(collect_count) from finger_data group by place"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            # print("取值成功！")
        except:
            print("读取数据失败！")
            db.rollback()
        else:
            return results

    def SelectPlace(self):
        sql = "select place from finger_data group by place"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print("读取数据失败！")
            db.rollback()
        else:
            return results

    def SelectMac_address(self, place):
        sql = "select `mac_address`,`place` from collection_data group by mac_address having place = '%s'" % \
            place
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print("读取数据失败！")
            db.rollback()
        else:
            return results

    def SelectRss_valueByMac_address(self, mac_address):
        sql = "select rss_value from collection_data where mac_address = '%s'" % \
              mac_address
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print("读取数据失败！")
            db.rollback()
        else:
            return results

    def DbClose(self):
        db.close()
