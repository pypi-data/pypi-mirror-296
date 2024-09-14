# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from typing import Dict, List
from dateutil import parser
from datetime import datetime, timedelta, timezone
from dateutil.tz import tzutc
from collections import OrderedDict
from itertools import groupby
from operator import itemgetter
import csv
import json
from typing import Optional
import pytz
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 模拟进度条
def progress_bar(progress, total):
    bar_length = 50
    percent = (progress / float(total)) * 100
    bar = '=' * int(percent / (100 / bar_length))
    progress_str = '\r[{0}] {1:.2f}%'.format(bar + '-' * (bar_length - len(bar)), percent)
    if progress == total:
        progress_str += ' Done\n'
    else:
        progress_str += ' ' * (len(str(total)) + 7)  # 清除之前的进度数字
    logger.info(progress_str)


def get_influx_db_connection(host, port, username, password, timeout):
    """
    获取InfluxDB连接，使用完必须使用close()关闭。

    :param host: 数据库连接地址ip，必填参数
    :param port: 数据库连接地址端口，必填参数
    :param username: 用户名，必填参数
    :param password: 密码，必填参数
    :param timeout: 设置HTTP客户端超时时间（单位：秒），必填参数
    :return: InfluxDBClient实例
    """
    # 创建InfluxDBClient实例，并设置超时
    client = InfluxDBClient(host=host, port=port, username=username, password=password, timeout=timeout)

    # 尝试连接到数据库
    try:
        client.ping()
        logger.info("InfluxDB connection successful")
    except InfluxDBClientError as e:
        logger.error(f"InfluxDB connection failed: {e}")
        return None

    return client


def get_time_list(start_time: int, end_time: int, interval: int) -> List[int]:
    """
    获取时间集合

    :param start_time: 开始时间（时间戳，单位：毫秒）
    :param end_time: 结束时间（时间戳，单位：毫秒）
    :param interval: 时间间隔（单位：秒）
    :return: 包含时间戳的列表
    """
    time_list = []
    while start_time <= end_time:
        time_list.append(start_time)
        start_time += interval * 1000  # 将秒转换为毫秒
    return time_list


def utc_get_time(utc_time: str) -> int:
    """
    获取UTC时间对应的时间戳

    :param utc_time: UTC时间字符串
    :return: 返回UTC时间的时间戳（毫秒）
    """
    # 使用 dateutil.parser 解析UTC时间字符串
    time = parser.parse(utc_time)
    # 转换为时间戳（毫秒）
    timestamp = int(time.timestamp() * 1000)
    return timestamp


def timestamp_to_beijing_time(timestamp):
    # 将毫秒级时间戳转换为秒级时间戳
    timestamp_seconds = timestamp / 1000.0
    # 假设timestamp是自1970年1月1日以来的秒数
    utc_dt = datetime.utcfromtimestamp(timestamp_seconds)
    # 将UTC时间转换为北京时间（东八区）
    beijing_dt = utc_dt + timedelta(hours=8)
    # 格式化时间字符串
    formatted_date = beijing_dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def utc_time_add_one_day_time(utc_time: str) -> int:
    """
    UTC时间增加一天的时间戳

    :param utc_time: 传入的UTC时间, 时间格式：2024-03-13T16:00:00Z
    :return: UTC时间增加一天的时间戳（毫秒）
    """
    # 使用dateutil.parser解析UTC时间字符串
    time = parser.parse(utc_time)
    # 把日期往后增加一天
    new_time = time + timedelta(days=1)
    # 转换为时间戳（毫秒）
    timestamp = int(new_time.timestamp() * 1000)
    return timestamp


def utc_time_add_one_day(utc_time: str) -> str:
    """
    UTC时间增加一天

    :param utc_time: 传入的UTC时间, 时间格式：2024-03-13T16:00:00Z
    :return: 返回增加一天后的UTC时间，时间格式：2024-03-14T16:00:00Z
    """
    # 使用dateutil.parser解析UTC时间字符串
    time = parser.parse(utc_time)
    # 把日期往后增加一天
    new_time = time + timedelta(days=1)
    # 转换回UTC时间字符串
    utc_add_day = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return utc_add_day


def utc_time_to_timestamp(utc: str) -> int:
    """
    UTC时间转换成毫秒时间戳

    :param utc: UTC时间字符串
    :return: 毫秒级时间戳
    """
    # 使用dateutil.parser解析UTC时间字符串
    utc_datetime = parser.parse(utc)
    # 转换为timestamp（毫秒）
    timestamp = int(utc_datetime.timestamp() * 1000)
    return timestamp


def convert_utc_to_beijing_time(utc_time: str) -> str:
    """
    UTC时间转换成北京时间，时间格式："yyyy-MM-dd HH:mm:ss"

    :param utc_time: UTC时间字符串
    :return: 北京时间字符串
    """
    # 将UTC时间字符串解析为datetime对象
    utc_datetime = parser.parse(utc_time)
    # utc_datetime = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    # 将UTC时间转换为UTC时区对应的datetime对象
    utc_aware = utc_datetime.replace(tzinfo=timezone.utc)
    # 将UTC时间转换为北京时间（东八区）
    beijing_aware = utc_aware + timedelta(hours=8)
    # 格式化时间为指定格式
    beijing_time_str = beijing_aware.strftime('%Y-%m-%d %H:%M:%S')
    return beijing_time_str


def convert_beijing_time_to_utc(beijing_time_str):
    # 解析北京时间字符串
    beijing_time = datetime.strptime(beijing_time_str, "%Y-%m-%d %H:%M:%S")
    # 设置北京时区
    beijing_tz = pytz.timezone('Asia/Shanghai')
    # 将北京时间转换为带有时区的datetime对象
    beijing_datetime = beijing_tz.localize(beijing_time)
    # 转换为UTC时间
    utc_datetime = beijing_datetime.astimezone(pytz.UTC)
    # 转换为ISO 8601格式（包含Z结尾）
    utc_time_str = utc_datetime.isoformat().replace('+00:00', 'Z')

    return utc_time_str


def get_new_set_data(database: str, tableName: str, pointList: List[str],
                     influxDB: InfluxDBClient, queryTime: Optional[str] = None) -> str:
    """
        查询最新的测点数据或查询某个时刻的测点数据（需时间对齐）。

        Args:
            database (str): 数据库名。必填参数
            tableName (str): 表名。必填参数
            queryTime (str, optional): 查询时刻。默认值为None，表示查询最新时间。
                格式要求：'YYYY-MM-DD HH:mm:ss'。
            pointList (list[str]): 一个或多个点号。必填参数，表示查询所有点。
            influxDB (InfluxDBClient): 数据库连接对象。必填参数，表示使用默认连接。

        Returns:
            Any: 查询结果，具体类型取决于查询内容和返回的数据结构。

        说明：
            本函数可同时满足以下四个场景要求：
            1. 获取一个点的最新值。
            2. 获取一个点在特定时刻的值。
            3. 获取多个点的最新值。
            4. 获取多个点在特定时刻的值。
        """
    # 1. 初始化 resultList
    resultList = []
    # 2. 使用join方法将pointList中的字符串用'|'连接起来
    pointStr = '$|'.join(pointList)
    # 3. 构建SQL查询字符串
    SQLForMaxTime = f"SELECT LAST(VALUE), UUID FROM {tableName} WHERE UUID =~ /{pointStr}$/"

    # 4. 如果queryTime不为空，则添加时间条件
    if queryTime is not None and queryTime != "":
        queryTime = convert_beijing_time_to_utc(queryTime)
        SQLForMaxTime += f" AND time <= '{queryTime}'"

    # 5. 执行查询
    queryResult = influxDB.query(SQLForMaxTime, database=database)

    # 6. 从查询结果中提取最大的时间戳
    maxTime = ""
    # 检查查询结果是否为空
    if queryResult.error:
        logger.error(f"查询出错: {queryResult.error}")
    else:
        # 将生成器转换为列表
        series_list = list(queryResult.get_points())
        if series_list:
            maxTime = series_list[0]['time']
            # for point in series:
            #     maxTime = point['time']

    # 添加 group by UUID 到查询字符串
    SQLForData = SQLForMaxTime + " GROUP BY UUID"

    # 执行查询
    query_result_for_data = influxDB.query(SQLForData, database=database)

    # 初始化结果列表
    resultList = []

    # 进行数据时间对齐处理
    if query_result_for_data.error:
        logger.info(f"查询出错: {query_result_for_data.error}")
    else:
        series = query_result_for_data.get_points()
        if series:
            for point in series:
                obj_list = [maxTime, point['last'], point['UUID']]
                resultList.append(obj_list)

    data_map = OrderedDict()

    if len(resultList) > 0:
        # 假设resultList的每个子列表的第一个元素是时间，我们将其转换为北京时间
        data_map["time"] = convert_utc_to_beijing_time(resultList[0][0])

        # 遍历resultList的每个子列表
        for sublist in resultList:
            # 假设每个子列表的第三个元素是键，第二个元素是值
            data_map[sublist[2]] = sublist[1]

            # 将字典转换为JSON字符串
    toJSONString = json.dumps(data_map)

    # 返回JSON字符串
    return toJSONString


def get_new_data_map(database: str, tableName: str, queryTime: str, pointList: List[str],
                     influxDB: InfluxDBClient) -> Dict:
    """
    查询最新的测点数据或查询某个时刻的测点数据，返回Map集合（在Python中为字典）。

    Args:
        database (str): 数据库名。
        tableName (str): 表名。
        queryTime (str, optional): 查询时刻。默认为None，表示查询最新时间。格式应为'YYYY-MM-DDTHH:MM:SSZ'。
        pointList (List[str], optional): 一个或多个点号。默认为None，表示查询所有点。
        influxDB (object, optional): 数据库连接对象。默认为None，表示使用默认连接。

    Returns:
        Dict: 字典，包含查询结果的键值对。

    """
    # 将点号列表连接成一个字符串，使用'|'作为分隔符
    point_str = '$|'.join(pointList)

    # 构建SQL查询语句
    sql_query = f"SELECT LAST(VALUE), UUID FROM {tableName} WHERE UUID =~ /{point_str}$/"

    # 如果查询时间不为空，则添加时间条件和分组
    if queryTime:
        sql_query += f" AND time <= '{queryTime}' GROUP BY UUID"

    logger.info(f"------------get_new_data_map方法sql: {sql_query}")

    # 执行查询
    result = influxDB.query(sql_query, database=database)

    # 初始化一个有序字典来存储结果
    data_map = OrderedDict()

    # 遍历查询结果
    if result.error:
        logger.info(f"------------查询出错: {result.error}")
        # print("查询出错: ", result.error)
    else:
        series = result.get_points()
        if series:
            for point in series:
                uuid = point['UUID']
                value_obj = point['last']
                data_map[uuid] = value_obj

    return data_map


def get_his_set_data_by_complete(database: str, tableName: str, startTime: str, endTime: str, pointList: List[str],
                                 influxDB: InfluxDBClient, interval: Optional[int] = None):
    """
    查询历史时间段一个或多个测点数据（进行数据补齐）

    可同时满足下面4个场景要求：
    1、获取一个[点]的[开始，结束]段的历史数据;
    2、获取一个[点]的[开始，结束]段的[间隔秒]的历史数据;
    3、获取多个[点...] 的[开始，结束] 段的历史数据;
    4、获取多个[点...] 的[开始，结束] 段的[间隔秒] 的历史数据;

    Args:
        database (str): 数据库名，必填参数
        tableName (str): 表名，必填参数
        startTime (str): 开始时间，必填参数，表示使用当前时间。
        endTime (str): 结束时间，必填参数，表示使用当前时间。
        pointList (list of str): 一个或多个点号列表，必填参数，表示查询所有点。
        interval (int, optional): 时间间隔（单位秒），默认为None，表示不使用间隔查询。
        influxDB (InfluxDBClient): InfluxDB连接对象，必填参数，表示使用默认连接。

    Returns:
        dict: 包含查询结果的字典，具体结构根据实际应用情况确定。
    """
    startTime = convert_beijing_time_to_utc(startTime)
    endTime = convert_beijing_time_to_utc(endTime)
    # 构建点号字符串
    point_str = '$|'.join(pointList)

    # 构建查询语句
    query = f"SELECT LAST(VALUE), UUID FROM {tableName} WHERE UUID =~ /{point_str}$/ AND time>='{startTime}' AND time<='{endTime}' GROUP BY UUID, time({interval}s) FILL(previous) "

    # 执行查询
    result = influxDB.query(query, database=database)

    # 获取数据映射，这里需要相应的Python实现
    map_data = get_new_data_map(database, tableName, startTime, pointList, influxDB)

    timeList = get_time_list(utc_get_time(startTime), utc_get_time(endTime), interval)

    result_value_map = OrderedDict()
    for series in result.raw['series']:
        result_value_map[series['tags']['UUID']] = series['values']

    map_record = OrderedDict()
    sb = '['
    index = 0
    for time_stamp in timeList:
        dataTimeStr = timestamp_to_beijing_time(time_stamp)
        map_record['time'] = dataTimeStr  # 添加时间戳
        for point in pointList:
            values_list = result_value_map.get(point)
            if values_list and values_list[index][1]:
                # 假设 values_list 是一个包含时间戳和值的元组列表
                map_record[point] = values_list[index][1]
            elif point in map_data:
                map_record[point] = map_data[point]
            else:
                map_record[point] = ''

        if index >= 1:
            sb += ','
        sb += json.dumps(map_record)
        index += 1
    sb += ']'

    return sb


def get_his_set_data_by_complete_FQ(database: str, tableName: str, startTime: str, endTime: str, pointList: List[str],
                                 influxDB: InfluxDBClient, interval: Optional[int] = None):
    """
    查询历史时间段一个或多个测点数据（进行数据补齐）

    可同时满足下面4个场景要求：
    1、获取一个[点]的[开始，结束]段的历史数据;
    2、获取一个[点]的[开始，结束]段的[间隔秒]的历史数据;
    3、获取多个[点...] 的[开始，结束] 段的历史数据;
    4、获取多个[点...] 的[开始，结束] 段的[间隔秒] 的历史数据;

    Args:
        database (str): 数据库名，必填参数
        tableName (str): 表名，必填参数
        startTime (str): 开始时间，必填参数，表示使用当前时间。格式应为ISO 8601。
        endTime (str): 结束时间，必填参数，表示使用当前时间。格式应为ISO 8601。
        pointList (list of str): 一个或多个点号列表，必填参数，表示查询所有点。
        interval (int, optional): 时间间隔（单位秒），默认为None，表示不使用间隔查询。
        influxDB (InfluxDBClient): InfluxDB连接对象，必填参数，表示使用默认连接。

    Returns:
        dict: 包含查询结果的字典，具体结构根据实际应用情况确定。
    """
    startTime = convert_beijing_time_to_utc(startTime)
    endTime = convert_beijing_time_to_utc(endTime)
    # 构建点号字符串
    point_str = '$|'.join(pointList)

    # 构建查询语句
    query = f"SELECT LAST(VALUE), UUID FROM {tableName} WHERE UUID =~ /{point_str}$/ AND time>='{startTime}' AND time<='{endTime}' GROUP BY UUID, time({interval}s) FILL(previous) "

    # 执行查询
    result = influxDB.query(query, database=database)

    # 获取查询结果的点
    points = result.get_points()

    # 获取数据映射，这里需要相应的Python实现
    map_data = get_new_data_map(database, tableName, startTime, pointList, influxDB)

    # 初始化结果列表
    result_list = []

    # 处理查询结果
    for point in points:
        time = point['time']
        uuid = point['UUID']
        value = point['last']

        # 根据条件选择使用查询结果中的UUID还是map中的UUID
        if uuid is not None or uuid not in map_data:
            uuid_to_add = value
        else:
            uuid_to_add = map_data[uuid]

            # 构建结果列表
        result_list.append([time, uuid_to_add, uuid])

    # print(result_list)
    # 初始化最外层的字典
    map_all = OrderedDict()
    if result_list:
        for item_list in result_list:
            # 转换UTC时间为北京时间
            time_beijing = convert_utc_to_beijing_time(item_list[0])

            # 获取或创建当前时间对应的字典
            map2 = map_all.get(time_beijing)
            if map2 is None:
                map2 = OrderedDict()
                map2["time"] = time_beijing
                map_all[time_beijing] = map2

            map2[item_list[2]] = item_list[1]

    values_set = []
    for d in map_all.values():
        values_set.append(d)
    # 转换为JSON字符串
    to_json_string = json.dumps(values_set)

    return to_json_string


def get_his_set_data(database: str, tableName: str, startTime: str, endTime: str,
                     pointList: List[str], influxDB: InfluxDBClient) -> str:
    """
    查询历史一个或多个测点数据（不进行数据补齐）

    Args:
        database (str): 数据库名，必填参数
        tableName (str): 表名，必填参数
        startTime (str): 开始时间，必填参数(格式要求："2023-12-27 13:42:00")
        endTime (str): 结束时间，必填参数(格式要求："2023-12-27 13:42:00")
        pointList (List[str]): 一个或多个点号，必填参数
        influxDB (InfluxDBClient): 数据库连接，必填参数

    Returns:
        str: 查询结果

    """
    startTime = convert_beijing_time_to_utc(startTime)
    endTime = convert_beijing_time_to_utc(endTime)
    # 将点号列表转换为str
    pointStr = '$|'.join(pointList)

    # 构建查询语句
    query = f"SELECT time,VALUE, UUID FROM {tableName} WHERE UUID =~ /{pointStr}$/ AND time>='{startTime}' AND time<='{endTime}' "

    # 执行查询
    result = influxDB.query(query, database=database)

    od = OrderedDict()

    resultValueMap = OrderedDict()

    map_record = OrderedDict()

    # 解析查询结果并提取数据
    result_list = []
    for point in result.get_points():
        od[point['time']] = point['time']
        obj_list = [point['time'], point['VALUE'], point['UUID']]
        # 获取VALUE和UUID字段的值，假设还有其他字段则继续添加
        result_list.append(obj_list)
        resultValueMap[point['UUID']+'|'+point['time']] = point['VALUE']

    keys_list = [key for key in od.keys()]

    sb = '['
    index = 0
    for time_temp in keys_list:
        map_record['time'] = convert_utc_to_beijing_time(time_temp)
        for point in pointList:
            value = resultValueMap.get(point+'|'+time_temp, '')
            if value:
                map_record[point] = value
            else:
                map_record[point] = ''
        if index >= 1:
            sb += ','
        sb += json.dumps(map_record)
        index += 1

    sb += ']'
    # # 将结果转换为JSON字符串
    # json_string = json.dumps(result_list)

    # 返回JSON字符串
    return sb


def write_history_data_to_csv(database: str, tableName: str, startTime: str, endTime: str, pointList: List[str],
                              interval: int, influxDB: InfluxDBClient, filePath: str, batchSize: int = 100):
    """
    将历史时间段一个或多个测点数据写入到CSV文件中（进行数据补齐）

    可同时满足下面4个场景要求：
    1、获取一个点的[开始，结束]段的历史数据;
    2、获取一个点的[开始，结束]段的[间隔秒]的历史数据;
    3、获取多个点...的[开始，结束]段的历史数据;
    4、获取多个点...的[开始，结束]段的[间隔秒]的历史数据;

    Args:
        database (str): 数据库名，必填参数
        tableName (str): 表名，必填参数 (在InfluxDB中通常是measurement名)
        startTime (str): 开始时间，必填参数(格式要求："YYYY-MM-DD HH:mm:ss")
        endTime (str): 结束时间，必填参数(格式要求："YYYY-MM-DD HH:mm:ss")
        pointList (List[str]): 一个或多个点号（测点标识），必填参数
        interval (int): 时间间隔（单位秒），必填参数
        batchSize (int): 当点位过多时，分批处理数量，选填填参数，默认100
        influxDB (InfluxDBClient): InfluxDB客户端连接，必填参数
        filePath (str): 文件路径，必填参数，例如："D:\\temp\\202401.csv" 或 "/opt/202401.csv"
    """
    startTime = convert_beijing_time_to_utc(startTime)
    endTime = convert_beijing_time_to_utc(endTime)
    # 打开文件以写入CSV数据
    with open(filePath, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        # 写头信息（测点点号）
        title_list = ['timestamp']
        for point in pointList:
            title_list.append(point)

        csv_writer.writerow(title_list)

        # pointStr = '|'.join(pointList)
        startTime_temp = startTime
        endTime_temp = ''
        startTimeStamp_all = 0
        endTimeStamp_all = 0
        endTimeStamp_all = utc_get_time(endTime)
        if startTimeStamp_all > endTimeStamp_all:
            return
        time_list = []
        while True:
            logger.info(f"------------startTime: {startTime_temp}")
            result_value_map = OrderedDict()
            # 分批处理
            for i in range(0, len(pointList), batchSize):
                logger.info(f"开始分批查询，此时i = {i}")
                batch_points = pointList[i:i + batchSize]
                pointStr = '$|'.join(batch_points)
                # print("startTime: ", startTime_temp)
                SQLForHisDate = f"select LAST(VALUE), UUID from {tableName} where UUID =~/{pointStr}$/ "
                if utc_time_add_one_day_time(startTime_temp) < endTimeStamp_all:
                    endTime_temp = utc_time_add_one_day(startTime_temp)
                    SQLForHisDate += f"and time>='{startTime_temp}' and time<'{endTime_temp}'"
                    time_list = get_time_list(utc_get_time(startTime_temp), utc_get_time(endTime_temp) - 1000, interval)
                else:
                    endTime_temp = endTime
                    SQLForHisDate += f"and time>='{startTime_temp}' and time<='{endTime_temp}'"
                    time_list = get_time_list(utc_get_time(startTime_temp), utc_get_time(endTime_temp), interval)
                SQLForHisDate += f"group by UUID, time({interval}s) fill(previous)"
                logger.info("get_new_data_map开始运行-----")
                s_time = time.time()
                data_map = get_new_data_map(database, tableName, startTime_temp, batch_points, influxDB)
                # # 记录结束时间
                e_time = time.time()
                # # 计算运行时间（秒）
                run_time = e_time - s_time
                logger.info("get_new_data_map结束运行-----")
                logger.info(f"get_new_data_map方法运行时间：{run_time:.6f} 秒")

                logger.info("SQLForHisDate开始运行-----")
                s_time = time.time()
                result = influxDB.query(SQLForHisDate, database=database)
                # # 记录结束时间
                e_time = time.time()
                # # 计算运行时间（秒）
                run_time = e_time - s_time
                logger.info("SQLForHisDate结束运行-----")
                logger.info(f"SQLForHisDate方法运行时间：{run_time:.6f} 秒")
                # result_value_map = OrderedDict()
                for series in result.raw['series']:
                    result_value_map[series['tags']['UUID']] = series['values']

            # 遍历时间列表并构建CSV记录
            logger.info(f"开始遍历时间列表并构建CSV记录")
            index = 0
            for time_stamp in time_list:
                record = [time_stamp]  # 添加时间戳
                logger.info(f"时间戳:{time_stamp}")
                for inx, point in enumerate(pointList):
                    values_list = result_value_map.get(point)
                    if values_list and values_list[index][1]:
                        # 假设 values_list 是一个包含时间戳和值的元组列表
                        record.append(values_list[index][1])
                    elif point in data_map:
                        record.append(data_map[point])
                    else:
                        record.append('')
                    # 打印进度条
                    progress_bar(inx+1, len(pointList))

                # 写入CSV记录
                csv_writer.writerow(record)
                index += 1
                # 检查是否进行下一次查询

            if utc_time_add_one_day_time(startTime_temp) <= endTimeStamp_all:
                startTime_temp = utc_time_add_one_day(startTime_temp)
                # 在这里，你可能需要调用一个函数来执行下一次查询，并更新 query_result
            else:
                return  # 退出函数或方法
