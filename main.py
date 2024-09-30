from utils.responseImage_beta import ResponseImage, PALETTE_SJTU_RED, PALETTE_GREEN, PALETTE_GREY_BORDER, FONT_SYHT_M28, draw_rounded_rectangle
from PIL import Image, ImageDraw
from utils.sjtuClassroomApi import getRoomCourse
from typing import Optional, List, Dict, Any, Tuple
import datetime


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
    return sorted(result, key=lambda x: x[0])

def drawJs(jsInfo: List[Tuple[str, List[bool]]], targetBuilding: str, savePath: str) -> Optional[str]:
    img = ResponseImage(
        title=f'教室空闲时间',
        titleColor=PALETTE_SJTU_RED,
        primaryColor=PALETTE_SJTU_RED,
    )

    # sub img
    cell_size = 50
    padding = 10
    width = (len(jsInfo[0][1]) - 2) * (cell_size + padding) + 100
    height = (len(jsInfo) - 1) * (cell_size + padding)
    sub_img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sub_img)

    for i, (room_name, availability) in enumerate(jsInfo):
        draw.text((0, i * cell_size + i * padding + 12), room_name.replace(targetBuilding, ""), fill="black", font = FONT_SYHT_M28)

        for j, available in enumerate(availability[1:]):
            color = PALETTE_GREY_BORDER if available else PALETTE_GREEN
            draw_rounded_rectangle(
                sub_img,
                (
                    j * cell_size + j * padding + 100,
                    i * cell_size + i * padding,
                    (j + 1) * cell_size + j * padding + 100,
                    (i + 1) * cell_size + i * padding,
                ),
                fill=color
            )

    time_slots = [
        "08:00-08:45",
        "08:55-09:40",
        "10:00-10:45",
        "10:55-11:40",
        "12:00-12:45",
        "12:55-13:40",
        "14:00-14:45",
        "14:55-15:40",
        "16:00-16:45",
        "16:55-17:40",
        "18:00-18:45",
        "18:55-19:40",
        "20:00-20:45",
        "20:55-21:40"
    ]

    time_axis_img = Image.new("RGB", (200, width), "white")
    draw = ImageDraw.Draw(time_axis_img)
    for i, time in enumerate(time_slots):
        bbox = FONT_SYHT_M28.getbbox(time)
        left = 200 - bbox[2] + bbox[0]
        draw.text((left, i * cell_size + i * padding + 112), time, fill="black", font = FONT_SYHT_M28)
    time_axis_img = time_axis_img.rotate(90, expand=True)

    img.addCard(
        ResponseImage.RichContentCard(
            raw_content=[
                ('title', f"目标楼栋: {targetBuilding}"),
                ('subtitle', f"{datetime.datetime.now().strftime("%Y-%m-%d")}，绿色为空闲"),
                ('separator', ''),
                ('illustration', sub_img),
                ('illustration', time_axis_img),
                ('text', '\n')
            ]
        )
    )
    

    img.generateImage(savePath)
    return savePath

if __name__ == '__main__':
    targetBuilding = '东下院'
    jsInfoSavePath = targetBuilding + '.json'
    jsInfo = getRoomCourse(targetBuilding, datetime.date.today())
    # with open(jsInfoSavePath, 'w') as f:
    #     json.dump(jsInfo, f, ensure_ascii=False, indent=2)
    # print('save to:', jsInfoSavePath)
    jsInfo = processJsInfo(jsInfo)
    drawJs(jsInfo, targetBuilding, 'test.png')
    # print(jsInfo)
