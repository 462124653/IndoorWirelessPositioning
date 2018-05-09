import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "indoorwrielesslocation")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

class DataBase:
    def RssInsert(self, mac_address, wifi_name, rss_value, data_time, place, collec_count):
        try:
            cursor.execute('insert into collection_data(`mac_address`,`wifi_name`,`rss_value`,`data_time`,`place`,`collec_count`) values ("%s", "%s","%s","%s","%s","%d")' % \
                           (mac_address, wifi_name, rss_value, data_time, place, collec_count))
            db.commit()
            print("插入成功！")
        except:
            print("插入失败！")
            db.rollback()

    def RssSelect(self, place, collec_count):
        sql = "select mac_address,rss_value from collection_data where place = '%s' and collec_count = '%d'" % \
              (place, collec_count)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            # print("取值成功！")
            return results
        except:
            print("取值失败！")
            db.rollback()

    def FingerDataInsert(self, mac_address, rss_value, data_time, place, collect_count,room):
        try:
            cursor.execute('insert into finger_data(`place`,`mac_address`,`rss_value`,`data_time`,`collect_count`,`room`) values ("%s", "%s","%s","%s","%d","%s")' % \
                           (mac_address, rss_value, data_time, place, collect_count, room))
            db.commit()
            # print("插入成功！")
        except:
            print("插入失败！")
            db.rollback()

    def FingerDataSelcet(self, room):
        sql = "select mac_address,rss_value from finger_data where place = '%s' " % \
              (room)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print("取值成功！")
            return results
        except:
            print("读取数据失败！")
            db.rollback()

    def DbClose(self):
        db.close()
