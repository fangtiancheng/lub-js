from utils.responseImage_beta import ResponseImage
from utils.sjtuClassroomApi import getRoomCourse
from typing import Optional, List, Dict, Any, Tuple
import datetime
import json

def processJsInfo(jsInfo: Dict[str, List[Dict[str, Any]]]) -> List[Tuple[str, List[bool]]]:
    result:List[Tuple[str, List[bool]]] = []
    for floor in jsInfo.get('floorList', []):
        for room in floor.get('children', {}):
            roomName:str = room.get('name', 'unknow')
            roomSecs = [False] * 15 # 是否有课
            for course in room.get('roomCourseList', []):
                startSec:int = course.get('startSection', 0)
                endSec:int = course.get('endSection', 0)
            for sec in range(startSec, endSec + 1):
                roomSecs[sec] = True # TODO: IndexError
            result.append((roomName, roomSecs))
    return result

def drawJs(jsInfo: List[Tuple[str, List[bool]]], savePath: str) -> Optional[str]:
    # TODO:
    return savePath

if __name__ == '__main__':
    targetBuilding = '东下院'
    jsInfoSavePath = targetBuilding + '.json'
    jsInfo = getRoomCourse(targetBuilding, datetime.date.today())
    # with open(jsInfoSavePath, 'w') as f:
    #     json.dump(jsInfo, f, ensure_ascii=False, indent=2)
    # print('save to:', jsInfoSavePath)
    jsInfo = processJsInfo(jsInfo)
    print(jsInfo)
