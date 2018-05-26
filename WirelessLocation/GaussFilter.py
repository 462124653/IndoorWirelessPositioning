from RssData import DataBase
from scipy.ndimage import filters
import pylab
import numpy as np


def gauss_filter(place):
    # 存放mac地址
    mac_list = []
    # 存放rss值
    rss_dic = {}
    # 高斯滤波后的值
    rss_gauss_dic = {}
    gauss_data_sql = DataBase()
    results = gauss_data_sql.SelectMac_address(place)
    for result in results:
        mac_list.append(result[0])
    for i in mac_list:
        rss_dic[i] = gauss_data_sql.SelectRss_valueByMac_address(i)
    for mac_address, rss_value in rss_dic.items():
       rss_list = rss_value
       # 参数10为高斯函数标准差σ，正态分布的期望值μ决定了其位置，其标准差σ决定了分布的幅度
       rss_gauss_dic[mac_address] = filters.gaussian_filter(rss_list, 10)
    # for item in rss_gauss_dic.items():
    #     print(item)
    for show_count in range(0, len(rss_dic)):
        front_value = list(rss_dic.values())[show_count]
        print(front_value)
        tail_values = list(rss_gauss_dic.values())[show_count].tolist()
        tail_value = []
        for i in tail_values:
            tail_value.append(i[0])
        tail_value = np.array(tail_value)
        print(tail_value)
        # 显示图像
        pylab.figure()
        pylab.title(list(rss_dic.keys())[show_count])
        pylab.plot(front_value, 'b-', label='collect value')  # 过滤前的值
        pylab.plot(tail_value, color='g', label='filter value')  # 过滤后的值
        pylab.legend()
        pylab.xlabel('count')
        pylab.ylabel('rss_value')
        pylab.show()
