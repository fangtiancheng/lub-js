import requests
import datetime
import re
import os
from typing import Optional, Any, Tuple
from utils.basicEvent import send, warning



headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "ids.sjtu.edu.cn",
    "Origin": "https://ids.sjtu.edu.cn",
    "Referer": "https://ids.sjtu.edu.cn/classroomUse/goPage?param=00f9e7d21b8915f2595bcf4c5e83d41e5fa0251ff700451747b9ebe10b033327",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    'sec-ch-ua-platform': '"Windows"',
}

def getSjtuBuilding(building:str)->Optional[Any]:
    """获取教室信息（温度、湿度、人数、PM2.5等）
    @building: 教学楼[上院/中院/...]
    """
    url = 'https://ids.sjtu.edu.cn/classroomUse/findSchoolCourseInfo'
    
    datas = {
        '上院': 'buildId=126',
        '中院': 'buildId=128',
        '下院': 'buildId=127',
        '东上院': 'buildId=122',
        '东中院': 'buildId=564',
        '东下院': 'buildId=124',
        '陈瑞球楼': 'buildId=125',
    }
    data = datas[building]
    # try:
    session = requests.session()
    session.get('https://ids.sjtu.edu.cn')
    session.get("https://jaccount.sjtu.edu.cn")
    req = session.post(url=url, headers=headers, data=data)
    session.close()
    # except BaseException as e:
    #     warning('base exception while requesting sjtu classroom: {}'.format(e))
    #     return None
    if req.status_code != requests.codes.ok:
        warning("sjtu classroom API failed!")
        return None
    try:
        result = req.json()
        if result['code'] != 200:
            warning("code != 200, sjtu classroom API failed in getSjtuBuilding")
            return None
        return result['data']
    except requests.JSONDecodeError as e:
        warning('json decode error while getting sjtu classroom: {}'.format(e))
    except BaseException as e:
        warning('base exception while getting sjtu classroom: {}'.format(e))
    return None

def getRoomCourse(building:str, targetDate:datetime.date)->Optional[Any]:
    url = 'https://ids.sjtu.edu.cn/build/findBuildRoomType'
    payload = {
        '上院': 'buildId=126',
        '中院': 'buildId=128',
        '下院': 'buildId=127',
        '东上院': 'buildId=122',
        '东中院': 'buildId=564',
        '东下院': 'buildId=124',
        '陈瑞球楼': 'buildId=125',
    }[building] + targetDate.strftime('&courseDate=%Y-%m-%d')
    try:
        result = requests.post(url=url, headers=headers, data=payload).json()
        if result['code'] != 200:
            warning("code != 200, sjtu classroom API failed in getRoomCourse")
            return None
        return result['data']
    except BaseException as e:
        warning('base exception in getRoomCourse: {}'.format(e))
        return None

def getRoomDate()->Optional[Any]:
    url = 'https://ids.sjtu.edu.cn/course/findCurSemester'
    try:
        result = requests.post(url=url, headers=headers).json()
        if result['code'] != 200:
            warning("code != 200, sjtu classroom API failed in getRoomDate")
            return None
        return result['data']
    except BaseException as e:
        warning('base exception in getRoomDate: {}'.format(e))
        return None

def standarlizingRoomStr(roomStr:str)->Optional[Tuple[str, str]]:
    """
    东上103 => (东上院, 东上院103)
    东中1-105 => (东中院, 东中院1-105)
    陈瑞球103 => (陈瑞球楼, 陈瑞球楼103)
    你好 => None
    """
    pattern1 = re.compile(r'^(上|中|下|东上|东下)院?\s*(\d{3})$')
    if pattern1.match(roomStr) != None:
        building, roomCode = pattern1.findall(roomStr)[0]
        building += '院'
        return building, building + roomCode
    pattern2 = re.compile(r'^东中(院?\s*)(\d\-\d{3})$')
    if pattern2.match(roomStr) != None:
        building = '东中院'
        _, roomCode = pattern2.findall(roomStr)[0]
        return building, building+roomCode
    pattern3 = re.compile(r'^(陈瑞球楼?|球楼?)\s*(\d{3})$')
    if pattern3.match(roomStr) != None:
        building = '陈瑞球楼'
        _, roomCode = pattern3.findall(roomStr)[0]
        return building, building + roomCode
    return None

def standarlizingBuildingStr(buildingStr:str)->Optional[str]:
    """
    东上 => 东上院
    东中 => 东中院
    陈瑞球 => 陈瑞球楼
    你好 => None
    """
    pattern1 = re.compile(r'^(上|中|下|东上|东中|东下)院?$')
    if pattern1.match(buildingStr) != None:
        building = pattern1.findall(buildingStr)[0]
        building += '院'
        return building
    pattern3 = re.compile(r'^(陈瑞球楼?|球楼?)$')
    if pattern3.match(buildingStr) != None:
        building = '陈瑞球楼'
        return building
    return None
