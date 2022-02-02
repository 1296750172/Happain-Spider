# -!- coding: utf-8 -!-
import time

import requests
import execjs
import os




lan_dict= {
    '中文':'zh',
    '英文': 'en',
    "日文": 'jp'
}


def loadjs(data):
    with open(os.path.join(os.path.dirname(__file__),'main.js'),'r',encoding='utf-8') as f:
        file = f.read()
    jscode = execjs.compile(file)
    res = jscode.call('decode',data)
    return res

def translate(key,src="en",tar="zh"):
    num = 1

    while 1:
        try:
            res = requests.post(url="https://fanyi.baidu.com/v2transapi", headers={'User-Agent': 'Mozilla/5.0 ('
                                                                                                               'Windows NT 10.0; '
                                                                                                               'Win64; x64) '
                                                                                                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                                                                                                 'X-Requested-With': 'XMLHttpRequest',
                                                                                                 'Cookie': 'BIDUPSID=D910AF52E929729220801858236AD2DD; PSTM=1605731908; BAIDUID=D910AF52E9297292F52C3D5E8248C82C:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDUSS=NnVjBaSk5mTnlha3NPZEMxZDVubDdTbFFiMVAwZ29iLW1ua1RHTTY2UWwybFZnRVFBQUFBJCQAAAAAAAAAAAEAAABj1CQ3xOPOqrrOzaPWudbOwcYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACVNLmAlTS5gYz; BDUSS_BFESS=NnVjBaSk5mTnlha3NPZEMxZDVubDdTbFFiMVAwZ29iLW1ua1RHTTY2UWwybFZnRVFBQUFBJCQAAAAAAAAAAAEAAABj1CQ3xOPOqrrOzaPWudbOwcYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACVNLmAlTS5gYz; __yjs_duid=1_dd40607758ad71af17efc5fc5b7958731619533619483; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=110085_127969_175667_178384_178631_179348_179430_179623_181133_181481_181588_182000_182238_182273_182530_182847_183035_183327_184010_184267_184441_184560_184735_184793_184811_185029_185224_185268_185517_185880_186038_186155_186316_186412_186595_186635_186662_186820_187021_187042_187045_187088_187121_187186_187287_187356_187386_187421_187432_187487_187529_187532_187669_187816_187828_187928_187965_188181_188224_188267_188427_188467_188592_188660_188664_188731_188741_188753_188844_188870_188895; BDSFRCVID_BFESS=Ps4OJeC62u6c-NbHjrXx7ArOiaGgMEoTH6aoPwoU-HQWJo7TghRnEG0PMf8g0KuMVkacogKK3mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tRk8oI0aJDvDqTrP-trf5DCShUFsQM3JB2Q-XPoO3KJ-OKQ_y-CKh55WLq5dttbiW5cpoMbgylRM8P3y0bb2DUA1y4vpKhbBt2TxoUJ2abjne-53qtnWeMLebPRiJ-r9Qg-JslQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI8Rej-KjT5MKhuHetvab5T83Ru8bn72bU7hLfnkbfJBDl7TXJKHJebBKRI5JhjK_IQMDMJZ-lD7yajK25c7-J5kbbQ1M4oKMqjeKIcpQT8rqfDOK5Oi0CuJ5JOqab3vOIOzXpO1jxPzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqj_ffR4f_CLQKt8_HRjYbb__-P4DenjbyMRZ56bHWh0MbqP-OlnFQtncjU_XBNjMBMnqQJ7nKUT1bp7boMJRK5bdQUIT3xJUajJ43bRTLn7q3bbh_T6v257phP-UyNbLWh37JPjlMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafDLbbKL4jj-3-RJH-xQ0KnLXKKOLVMLabp7ketn4hUt25l_fXP7B04RwJ26H2KD-Whv-SCO2Qhrd5M4WWb3ebTJr32Qr-J3qLMbpsIJM557SbUtl5eFHXt7MaKviaKOEBMb1DqbDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6J3jNAjtj_jf5bEsJQHaJ3Dq5rnh6RmKT0gyxomtjjtJDAL2Jod2toiJK3qKxnE-f-sXtoyLUkqKCOTLb7GHlnGSpcvjpOJMhDHQttjQUrhfIkja-5zQJvHHn7TyU45hf47yaji0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OhJRQ2QJ8BJCKMhI5P; H_PS_PSSID=; delPer=0; PSINO=1; BAIDUID_BFESS=D776F397F069F8C243C41B32B626295B:FG=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1634137680,1634314083; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1634314083; __yjs_st=2_YTQ3Y2FiMTYwZjk5NWZhMThhNDM4ODg3MjI4ZjFmZjIwZjJlMmQ5ZTUwZTg1NTIzYmFmNGE0OTA5MzQ2NGQ2NDVjMjFiNjgyN2NjZmZhM2I4ZDY1NjkyNzYwOTA3YmZiNDY1Nzk5YjUxMjE2MTdiNjA0YWQ4MDg2M2FjN2JiOTZmYTAyZWI3NDRkYzU3YTE0MWJmMjRjNWU2ZWMzZDA3ZTUzNmIwMjRhYjk4YTM1MzU0Mzc1NmU4YTEwMGY1ZjhlMWQ3M2FlMWRmZmVlZTkyZmNiNDQzNDU0NjRiOWI1YWJmOGFlMDBmNTY2NDNmYjQzMDA5NzI3NDhmMGY2Y2Y2ZV83X2I5OGQ2MTUx; ab_sr=1.0.1_ZGExNTI5NTY2NDkzNWFkNzkyNGM5OTgxMjQ5NzJhNGUwZjM0ODQ2MzU1NDZmYmM3MTg3NzY5NzY2MDY4MGFlZjMwZTkwZjcwM2VhYjZkMmIyNTRlOGJlMThhNjc0OTA3NzcwMzIyMmUzNzNiNjg3NWYwZmU3MjNjN2RhMTk4OWI3YjMwZjdjNmIxMjI5Y2ZkOWQ1MDUzNGE0Y2NlZTNiM2ZmYzc2MzcwMDEyNzM1N2FhZTJlOGJkNzYxMGQwYzcx; BA_HECTOR=8h2hah25ah8ka4ahu11gmjdbg0q'},
                                data={'from': src, 'to': tar, 'query': key, 'sign': loadjs(key),
                                      'token': '3da933392a32a0dc28a2ddba5fdc4e09'})
            break
        except Exception as e:
            time.sleep(3)
            num+=1
            if num >5:
                break


    try:
        return res.json()['trans_result']['data'][0]['dst']
    except:
        return ""
if __name__ == '__main__':

    result  = translate(key="世界大战",src="zh",tar="jp")
    print(result)

