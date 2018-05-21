from GetRss import get_BSSI
from RssData import DataBase
from MeanFilter import MeanFilterClass
import datetime
import time


if __name__ == '__main__':
    database = DataBase()
    test = get_BSSI()
    room = "class"
    # 获取划分区域
    place = input("请输入划分的区域:")
    # 收集100组数据
    frequency = 100
    for i in range(0, frequency):
        time.sleep(1)  # 1秒钟收集一次数据
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
        oldTest = test
        test = get_BSSI()
        print ("Teste: " + str(i))
        if oldTest == test:
            print ("IGUAL")
        else:
            print ("DIFERENTE")
        for key, value in test.items():
            print(key)
            print(value[0])
            print(value[1])
            database.RssInsert(key, value[0], value[1], nowtime, place, i)
            print("----")
    print("收集完成")
    meanfilter = MeanFilterClass()
    results = meanfilter.MeanFilterFigerData(place, frequency)
    fingertime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 指纹生成时间
    for key, value in results.items():
        database.FingerDataInsert(place, key, value[0], fingertime, value[1], room)
    print("数据处理完成，存入指纹库中")
    database.DbClose()

