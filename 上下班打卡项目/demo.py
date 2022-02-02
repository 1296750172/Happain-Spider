# -!- coding: utf-8 -!-
import random
import time
import requests
import json

headers = {'Host': 'come2.catlbattery.com:9443', 'Content-Type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 DarkMode/N',
           'Authorization': 'Bearer 5c4b1958-c0a9-4c90-8a58-200ac51a6c00'}


# 上班打卡
def shangban():
    data = {
        "attribute2": '26.7290519205' + str(random.randint(10000, 99999)),
        "attribute3": '119.5692480' + str(random.randint(10000, 99999)),
        "attribute1": "000C8FAB-D2DB-458C-B3E8-7986324C25D7",
        "oldId": "坚持打卡",
        "punchType": "P10",
        "punchId": "e09a9499-39fa-4f77-a3ba-db47211fee6a"
    }

    res = requests.post(url="https://come2.catlbattery.com:9443/hipspunch/v1/1/punch/mobile/insertRecordData", headers=headers, data=json.dumps(data))
    print(res.json())
    # while True:
    #     everyday = time.localtime(time.time())
    #     if everyday.tm_hour == 8 and everyday.tm_min > 10:
    #         res = requests.post(url="https://come2.catlbattery.com:9443/hipspunch/v1/1/punch/mobile/insertRecordData", headers=headers, data=json.dumps(data))
    #         print(res.json())
    #         break
    #     time.sleep(random.randint(30, 60))
    pass

# 下班打卡
def xiaban():
    data = {
        "attribute2": '26.7290519205' + str(random.randint(10000, 99999)),
        "attribute3": '119.5692480' + str(random.randint(10000, 99999)),
        "attribute1": "000C8FAB-D2DB-458C-B3E8-7986324C25D7",
        "oldId": "坚持打卡",
        "punchType": "P20",
        "punchId": "e09a9499-39fa-4f77-a3ba-db47211fee6a"
    }
    res = requests.post(url="https://come2.catlbattery.com:9443/hipspunch/v1/1/punch/mobile/insertRecordData", headers=headers, data=json.dumps(data))
    print(res.json())
    pass

if __name__ == '__main__':

    "26.729051920572918"
    "119.569248046875"
    # xiaban()
    # while True:
    #     everyday = time.localtime(time.time())
    #     print(everyday.tm_hour)
    #     print(everyday.tm_min)
    #     if everyday.tm_hour == 20 and everyday.tm_min > 28:
    #         print(1111111)
    #         #
    #         break
    #     time.sleep(random.randint(30, 60))





