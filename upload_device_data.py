# coding: utf-8
# /! author liangben
# /! create_time {{create_time()}}

import base64
import datetime
import json
import os
import time
import requests
import logging
import shutil
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import configparser
from logging.handlers import TimedRotatingFileHandler
# 递归限制 50000，网络断开超过10000分钟，也就是超过7天则程序会挂掉
# import sys
# sys.setrecursionlimit

headers = {
    "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36"
                  r" (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    "method": "POST",
    "scheme": "http",
    "content-type": "application/json",
    "Connection": "close",
    "cookie": ""
}


def _logging(**kwargs):
    level = kwargs.pop('level', None)
    filename = kwargs.pop('filename', None)
    date_fmt = kwargs.pop('date_fmt', None)
    format_str = kwargs.pop('format', None)
    if level is None:
        level = logging.INFO
    if filename is None:
        filename = 'default.log'
    if date_fmt is None:
        date_fmt = '%Y-%m-%d %H:%M:%S'
    if format_str is None:
        format_str = '%(asctime)s [%(module)s] %(levelname)s [%(lineno)d] %(message)s'

    log = logging.getLogger(filename)
    format_str = logging.Formatter(format_str, date_fmt)
    # backupCount 保存日志的数量，过期自动删除
    # when 按什么日期格式切分(这里方便测试使用的秒)
    th = TimedRotatingFileHandler(filename=filename, when='midnight', backupCount=1, encoding='utf-8')
    th.setFormatter(format_str)
    th.setLevel(logging.INFO)
    log.addHandler(th)
    log.setLevel(level)
    return log


os.makedirs('./logs', exist_ok=True)
# logger = _logging(filename=f'./logs/upload.log')
logger = _logging(filename=f'./logs/upload.log')


def parser_config() -> tuple:
    """
    解析配置文件
    :return:
    """
    config = configparser.ConfigParser()
    config.read_file(open(r'.\application.cfg', encoding="gbk"))
    upload_url = config.get("配置", "upload_url")
    file_path = config.get("配置", "file_path")
    days = config.getint("配置", "delete_days")
    hour = config.getint("配置", "hour")
    minute = config.getint("配置", "minute")
    return upload_url, file_path, days, hour, minute


def delete_file(path_deleted: str, days: int):
    """
    删除文件树
    :param path_deleted:
    :param days:
    :return:
    """
    logger.info("正在执行定时删除任务")
    print(f"正在执行定时删除任务 | {datetime.datetime.now()}")
    today = datetime.datetime.today()
    days = datetime.timedelta(days=days)
    for file_name in os.listdir(path_deleted):
        abs_filename = os.path.join(path_deleted, file_name)
        if os.path.isdir(abs_filename):
            try:
                datetime_of_filename = datetime.datetime.strptime(file_name, "%Y%m%d")
            except:
                continue
            if (today - datetime_of_filename) > days:
                logger.info(f"正在删除 {abs_filename}")
                print(f"正在删除 {abs_filename} | {datetime.datetime.now()}")
                try:
                    shutil.rmtree(abs_filename)
                except Exception as e:
                    logger.error(f"删除失败 {abs_filename}")
                    print(f"删除失败 {abs_filename} | {datetime.datetime.now()}")
                    logger.error(e)
                else:
                    logger.info(f"删除成功 {abs_filename}")
                    print(f"删除成功 {abs_filename} | {datetime.datetime.now()}")


def timer_of_delete(hour: int, minute: int, path_to_delete: str, deleted_days: int):
    """
    删除文件的定时器
    :param hour:
    :param minute:
    :param path_to_delete:
    :param deleted_days:
    :return:
    """
    # 创建调度器 BlockingScheduler和BackgroundScheduler,
    # 当调度器是应用中唯一要运行的定时任务时，使用BlockingScheduler，如果希望调度器在后台执行，使用BackgroundScheduler.
    logger.info("初始化定时器")
    print(f"初始化定时器 | {datetime.datetime.now()}")
    scheduler = BackgroundScheduler()
    logger.info(f"将于每天{hour}:{minute}执行删除任务，目录树:{path_to_delete}")
    print(f"将于每天{hour}:{minute}执行删除任务，目录树:{path_to_delete} | {datetime.datetime.now()}")
    trigger = CronTrigger(hour=hour, minute=minute)
    scheduler.add_job(delete_file, trigger=trigger, args=[path_to_delete, deleted_days])
    # scheduler.add_job(delete_file, trigger="cron", hour=hour, minute=minute, args=[path_to_delete, deleted_days])
    logger.info("初始化定时器完成")
    print(f"初始化定时器完成 | {datetime.datetime.now()}")
    scheduler.start()


def encodeBase64Pic(picFilePath):
    """
    将图片转成base64格式
    :param picFilePath:
    :return:
    """
    with open(picFilePath, 'rb') as fp:
        data = fp.read()
        encode_str = base64.b64encode(data)  # 得到 byte 编码的数据
        fp.close()
    return str(encode_str, 'utf-8')


def post_api(url: str, data_dict: dict) -> tuple:
    """
    请求接口，传入数据
    :param url:
    :param data_dict:
    :return:
    """
    # 头部信息
    requestTime = data_dict["uploadTime"]
    sessionId = data_dict["deviceCode"]
    data = {
        "id": "00791ea20f994cc0a764009f6f671aa1",
        "requestTime": requestTime,
        "sessionId": sessionId,
        "command": "device.data.acquisition",
        "params": data_dict
    }
    response_time, response = "", ""
    while True:
        try:
            # requests.adapters.HTTPAdapter.DEFAULT_RETRIES = 50  # 增加重连次数
            requests.DEFAULT_RETRIES = 99999  # 增加重连次数
            ses = requests.session()
            ses.keep_alive = False
            res = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=(120, 120))
            res.raise_for_status()  # 如果响应状态码不是 200，抛出异常
        except TimeoutError as e:
            print(f"连接超时 车牌:{data_dict['plateNumber']} 抓拍时间：{data_dict['uploadTime']},"
                  f" 上传时间：{datetime.datetime.now()}\n")
            logger.error(e)
            time.sleep(1)
            continue
        except Exception as e:
            print(f"{datetime.datetime.now()}上传错误：{e}\n")
            logger.error(e)
            time.sleep(1)
            continue
        else:
            response = res.text
            response_time = res.elapsed
            break
    return response, response_time


def read_json_data(json_path: str, encoding: str = "UTF-8") -> dict:
    """
    读取json内容，返回JSON对象
    :param json_path:
    :param encoding:
    :return:
    """
    with open(json_path, "r", encoding=encoding) as jf:
        json_data = json.load(jf)
        return json_data


def dump_upload_info(filename: str, json_data: dict):
    """
    将上次文件的信息dump到json文件里
    :param filename:
    :param json_data:
    :return:
    """
    with open(filename, "w", encoding="utf-8") as fp:
        json.dump(json_data, fp)


def gen_image_path(json_data: dict, jfp: str) -> dict:
    """
    获取当前json对应的图片路径,并进行base64编码
    :param json_data:
    :param jfp:
    :return:
    """
    for image in ["plateImage", "headImage", "sideImage", "tailImage"]:
        if (not json_data[image] is None) and (json_data[image] != ""):
            json_data[image] = jfp.split(r"G006952004000510010_")[0] + json_data[image]
            json_data[image] = encodeBase64Pic(json_data[image])
    return json_data


def day_hour_add(hor: int, day: str) -> tuple:
    """
    返回增加后的时间
    :param day:
    :param hor:
    :return:
    """
    now_hour = hor + 1 if hor != 23 else 0
    if not now_hour:
        day = datetime.datetime.strptime(day, "%Y%m%d")
        day = day + datetime.timedelta(days=1)
        day = day.strftime("%Y%m%d")
    return now_hour, day


def get_st_mtimes(filename: str) -> datetime.datetime:
    """
    获取文件的修改时间
    :param filename:
    :return:
    """
    m_time = os.stat(filename).st_mtime
    # file_modify_time = datetime.strftime('%Y-%m-%d %H:%M:%S', mtime)
    file_modify_time = datetime.datetime.fromtimestamp(m_time)
    return file_modify_time


def iter_upload(dir_path, upload_url):
    """
    循环遍历文件夹，将没有上传过的json文件上传
    :return:
    """
    global success_time, fail_time, upload_info_dict, upload_info_file
    print(f"开始遍历{dir_path} {datetime.datetime.now()}".center(100, "-"))
    logger.info(f"开始遍历{dir_path} {datetime.datetime.now()}".center(100, "-"))
    for this_path, _, json_files_list in os.walk(dir_path):
        if len(json_files_list) == 0:
            time.sleep(3)
            break
        json_files_list = list(filter(lambda x: x.endswith(".json"), json_files_list))
        json_files_list = map(lambda f: dir_path + os.sep + f, json_files_list)
        no_upload_json_file_list = list(filter(lambda f: f not in upload_info_dict["success_list"], json_files_list))
        if len(no_upload_json_file_list) == 0:
            time.sleep(3)
            break
        no_upload_json_file_list = sorted(no_upload_json_file_list, key=get_st_mtimes)
        for no_upload_json_file in no_upload_json_file_list:
            try:
                car_json_data = read_json_data(no_upload_json_file)
                car_json_data = gen_image_path(car_json_data, no_upload_json_file)
            except Exception as e:
                # print(f"读取{no_upload_json_file}失败\n{e}", flush=True)
                logger.error(f"读取{no_upload_json_file}失败\n{e}")
                fail_list.append(no_upload_json_file)
                fail_time += 1
                continue
            success_time += 1
            upload_result, res_time = post_api(upload_url, car_json_data)
            upload_info_dict["success_list"].append(no_upload_json_file)
            dump_upload_info(upload_info_file, upload_info_dict)
            print(
                f"正在上传 第{success_time}个json，{car_json_data['plateNumber']} 抓拍时间：{car_json_data['uploadTime']}\n",
                f"{upload_result}\n",
                f"响应时间：{res_time} s\n",
                f"-" * 80, flush=False)
            logger.info(
                f"正在上传 第{success_time}个json，{car_json_data['plateNumber']}"
                f" 抓拍时间：{car_json_data['uploadTime']}\n{upload_result}\n响应时间：{res_time} s")


def main(file_path: str, upload_url: str):
    """
    主循环
    :return:
    """
    global fail_time, fail_list, success_time, upload_info_dict, upload_info_file
    root_path = file_path
    if os.path.exists(upload_info_file):
        upload_info_dict = read_json_data(upload_info_file)
        now_hour = upload_info_dict["now_hour"]
        today = upload_info_dict["upload_day"]
    else:
        now_hour = datetime.datetime.now().hour - 1
        today = datetime.datetime.now().date().strftime("%Y%m%d")
        upload_info_dict = {"now_hour": now_hour, "upload_day": today, "success_list": []}
    while True:
        dirpath = root_path + os.sep + today + os.sep + str(now_hour)
        iter_upload(dirpath, upload_url)
        now_day = datetime.datetime.now().date().strftime("%Y%m%d")
        nh = datetime.datetime.now().hour
        if (nh != now_hour) or (today != now_day):
            time.sleep(30)
            iter_upload(dirpath, upload_url)
            time.sleep(30)
            iter_upload(dirpath, upload_url)
            now_hour, today = day_hour_add(now_hour, today)
            upload_info_dict["success_list"].clear()
            upload_info_dict["now_hour"] = now_hour
            upload_info_dict["upload_day"] = today
            dump_upload_info(upload_info_file, upload_info_dict)
        time.sleep(30)


if __name__ == '__main__':
    # 初始化日志生成器
    # log_gen = getDayLog()
    # print(f"程序开始 {datetime.datetime.now()}".center(100, "-"))
    logger.info(f"程序开始 {datetime.datetime.now()}".center(100, "-"))
    print(f"程序开始 {datetime.datetime.now()}".center(100, "-"))
    # 定时器
    logger.info(f"解析配置文件......")
    print(f"解析配置文件 {datetime.datetime.now()}".center(100, "-"))
    device_upload_url, to_delete_path, delete_days, timer_hour, timer_minute = parser_config()
    timer_of_delete(timer_hour, timer_minute, to_delete_path, delete_days)
    # 上传设备数据-------
    fail_list = []
    fail_time = 0
    success_time = 0
    upload_info_dict = {}
    upload_info_file = r".\now_upload.json"
    try:
        main(to_delete_path, device_upload_url)
    except KeyboardInterrupt or SystemExit as err:
        print(f"共上传{success_time}个json文件\n" + f"失败文件：\n{fail_list}" + f"\n上传失败的文件数{fail_time}")
        logger.info(f"共上传{success_time}个json文件\n" + f"失败文件：\n{fail_list}" + f"\n上传失败的文件数{fail_time}")
