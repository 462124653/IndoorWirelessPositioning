import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "indoorwrielesslocation")
# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

class DataBase:
    def RssInsert(self, mac_address, wifi_name, rss_value, data_time, place, count):
        try:
            cursor.execute('insert into collection_data(`mac_address`,`wifi_name`,`rss_value`,`data_time`,`place`,`count`) values ("%s", "%s","%s","%s","%s","%d")' % (mac_address, wifi_name, rss_value, data_time, place, count))
            db.commit()
            print("插入成功！")
        except:
            print("插入失败！")
            db.rollback()

    def DbClose(self):
        db.close()
