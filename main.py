from utils.responseImage_beta import ResponseImage
from utils.sjtuClassroomApi import getRoomCourse
from typing import Optional
import datetime
import json

def drawJs(jsInfo, savePath:str) -> Optional[str]:
    # TODO:
    return savePath

if __name__ == '__main__':
    targetBuilding = '东下院'
    jsInfoSavePath = targetBuilding + '.json'
    jsInfo = getRoomCourse(targetBuilding, datetime.date.today())
    with open(jsInfoSavePath, 'w') as f:
        json.dump(jsInfo, f, ensure_ascii=False, indent=2)
    print('save to:', jsInfoSavePath)
