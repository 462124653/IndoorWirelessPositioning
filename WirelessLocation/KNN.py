from RssData import DataBase
from MeanFilter import MeanFilterClass


if __name__ == '__main__':
    online_filter = MeanFilterClass()
    knn_data_sql = DataBase()
    # 在线数据字典
    online_data = {}
    # 存放地点list
    place_list = []
    # 存放地点的指纹数据字典
    place_data_sql = {}
    # 存放欧式距离字典
    knn_size = {}
    # 获取指纹库的数据和实时过滤数据10s的数据
    online_results = online_filter.MeanFilterMeasureData(10)
    for online_key, online_value in online_results.items():
        online_data[online_key] = online_value[0]
    # 获取到指纹库中所有的位置
    knn_place = knn_data_sql.SelectPlace()
    for data_place in knn_place:
        place_list.append(data_place[0])
    for i in place_list:
        distance = 0
        place_data_sql.clear()
        results = knn_data_sql.FingerDataSelcet(i)
        for res in results:
            place_data_sql[res[0]] = res[1]
        for online_key, online_value in online_data.items():
            count = 0
            for place_data_key, place_data_value in place_data_sql.items():
                if online_key == place_data_key:
                    distance += (online_value - place_data_value)**2
                    count += 1
                else:
                    count += 1
                if count == len(place_data_sql)-1:
                    distance += online_value**2
        knn_size[i] = distance
    for item in knn_size.items():
        print(item)
    now_place = (min(knn_size.items(), key=lambda x: x[1]))
    print("当前的位置:")
    print(now_place[0])
