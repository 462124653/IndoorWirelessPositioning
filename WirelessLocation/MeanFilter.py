from RssData import DataBase
import datetime
import GetRss
import time


class MeanFilterClass:
    # 生成指纹库的过滤
    def MeanFilterFigerData(self, place, frequency):
        # 求均值字典
        averages = {}
        # 获取时间
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 权重 AP出现的次数
        count = 1
        # MeanCount
        mean_count = 0
        # 遍历时新增加的键值对
        add_dic = {}
        add_key = 0
        add_value = 0
        data_select = DataBase()
        zeros = data_select.RssSelect(place, 0)
        for zero in zeros:
            averages[zero[0]] = [zero[1], count]
        for i in range(1, int(frequency)):
            # print('%s点的第%d组数据:' % (place, i))
            results = data_select.RssSelect(place, i)
            add_dic.clear()
            for result in results:
                i = 0
                for key, value in averages.items():
                    if key == result[0]:
                        average_value = (value[0] + result[1]) / 2
                        average_count = value[1] + 1
                        averages[key] = [average_value, average_count]
                        break
                    else:
                        i += 1
                    if i == len(averages):
                        add_key = result[0]
                        add_value = result[1]
                        add_dic[add_key] = add_value
            if len(add_dic) != 0:
                for add_key, add_value in add_dic.items():
                    averages[add_key] = [add_value, count]

        print("均值滤波，加权过滤")
        for view in averages.items():
            print(view)
        print("---------------------")
        for finger_key, finger_value in averages.items():
            mean_count = mean_count + finger_value[1]
            count = count + 1
        mean_count = (mean_count / count) * (2 / 3)
        print(count-1, mean_count)
        averages = {k: v for k, v in averages.items() if v[1] > mean_count}
        for view in averages.items():
            print(view)
        print("--------------------------------")
        # for key, value in averages.items():
        #     averages[key] = [value[0], value[1]]
        # for view in averages.items():
        #     print(view)
        return averages

    # 实时采集数据时的过滤
    def MeanFilterMeasureData(self, frequency):
        # 求均值字典
        averages = {}
        # 权重 AP出现的次数
        count = 1
        # MeanCount
        meancount = 0
        # 遍历时新增加的键值对
        add_key = 0
        add_value = 0
        get_data = GetRss.get_BSSI()
        for key, value in get_data.items():
            averages[key] = [int(value[1]), count]
        for i in range(1, frequency):
            time.sleep(1)  # 1秒钟收集一次数据
            # print('%s点的第%d组数据:' % (place, i))
            data = GetRss.get_BSSI()
            results = {}
            for key, value in data.items():
                results[key] = [int(value[1])]
            print("第%d组数据" % (i))
            for item in results.items():
                print(item)
            for key, value in averages.items():
                i = 0
                for result_key, result_value in results.items():
                    if key == result_key:
                        average_value = (value[0] + result_value[0]) / 2
                        average_count = value[1] + 1
                        averages[key] = [average_value, average_count]
                        continue
                    else:
                        i += 1
                    if i == len(results) - 1:
                        add_key = result_key
                        add_value = result_value[0]
            if add_key != 0 and add_value != 0:
                averages[add_key] = [add_value, count]
        print("----------")
        for view in averages.items():
            print(view)
        print("---------------------")
        for finger_key, finger_value in averages.items():
            meancount = meancount + finger_value[1]
            count = count + 1
        meancount = (meancount / count) * (2 / 3)
        print(count-1, meancount)
        averages = {k: v for k, v in averages.items() if v[1] > meancount}
        for view in averages.items():
            print(view)
        print("--------------------------------")
        # for key, value in averages.items():
        #     averages[key] = [value[0], value[1]]
        # for view in averages.items():
        #     print(view)
        return averages

