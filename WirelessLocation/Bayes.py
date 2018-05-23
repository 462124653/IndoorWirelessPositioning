from RssData import DataBase
from MeanFilter import MeanFilterClass

if __name__ == '__main__':
    room = 'class'
    # 概率字典
    probability = {}
    # 指纹库字典
    finger_data = {}
    # 点所有的count和字典
    ap_count_data = {}
    # 实时采集数据权重
    all_online_count = 0
    data_bayes = DataBase()
    online_filter = MeanFilterClass()
    # 获取指纹库的数据和实时过滤数据10s的数据
    online_results = online_filter.MeanFilterMeasureData(10)
    # 获取每个点的总的Count
    ap_count = data_bayes.PlaceAPCount()
    for item in ap_count:
        ap_count_data[item[0]] = [item[1]]
    for key, value in ap_count_data.items():
        print(value[0])
    # 获取实时数据权值
    # for online_key, online_value in online_results.items():
    #     all_online_count += online_value[1]
    for online_key, online_value in online_results.items():
        finger_results = data_bayes.FingerMacAdressDataSelcet(online_key)
        finger_data.clear()
        # 指纹库比值计数
        all_finger_count = 0
        if finger_results == '':
            continue
        else:
            for item in finger_results:         # 将获取的指纹库，写入指纹库字典
                finger_data[item[1]] = [item[0], item[2]]
            # finger_data[place] = [rss_value, count]
            for finger_data_key, finger_data_value in finger_data.items():
                for ap_count_data_key, ap_count_data_value in ap_count_data.items():
                    # 当前AP的值与指纹库的值对比，取Δ<1的
                    delta_rss = finger_data_value[0] - online_value[0]
                    if abs(delta_rss) <= 3 and finger_data_key == ap_count_data_key:
                        probability[online_key, ap_count_data_key] = \
                            [finger_data_value[1] / ap_count_data_value[0], online_value[1] / 10]
                        # probability[mac_address, 地点] = [ P(点|AP),online_count ]
                        # 某个在线测试的AP在所有地点的概率 online_count 为信赖贝叶斯的权重

    for item in probability.items():
        print(item)
    # 获取概率字典的地点
    place = []
    for probability_key, probability_value in probability.items():
        place.append(probability_key[1])
    place = sorted(set(place), key=place.index)
    print(place)
    # 统计出现位置的次数字典
    place_dic = {}
    for place_simple in place:
        place_count = 0
        for probability_key, probability_value in probability.items():
            if place_simple == probability_key[1]:
                place_count += 1
        place_dic[place_simple] = [place_count]

    # max_value = 0
    for item in place_dic.items():
        print(item)
    # 计算每个点的概率，由上面的统计次数加权，求出最大概率出现的地点
    P_dic = {}
    for place_simple in place:
        P = 1
        for probability_key, probability_value in probability.items():
            if place_simple == probability_key[1]:
                    P = (float(probability_value[0])*probability_value[1])*P
        P_dic[place_simple] = P
    for item in P_dic.items():
        print(item)
    print("--------------------------")
    # 找出最小的键值对
    P_min = (min(P_dic.items(), key=lambda x: x[1]))
    del P_dic[P_min[0]]
    # 找出第二小的键值对
    P_second = (min(P_dic.items(), key=lambda x: x[1]))
    print("当前正在位置:")
    # 求出同等数据量级下值大的
    if P_second[1] / P_min[1] < 10:
        print(P_second[0])
    else:
        print(P_min[0])
    data_bayes.DbClose()




