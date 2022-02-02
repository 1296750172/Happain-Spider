# -!- coding: utf-8 -!-
import json

import requests
import execjs
import base64


node = execjs.get()

with open('demo.js','r',encoding='utf-8') as f:
    data = f.read()



def decode():
    ctx = node.compile(data, cwd=r'./node_modules')
    result = ctx.call('decode')
    d = json.dumps({'data':result,"key_id":"78a95375e30448e4"})
    res = base64.b64encode(d.encode('utf-8')).decode("utf-8")
    return res
if __name__ == '__main__':
    cookies= 'BIDUPSID=D910AF52E929729220801858236AD2DD; PSTM=1605731908; __yjs_duid=1_dd40607758ad71af17efc5fc5b7958731619533619483; H_WISE_SIDS=110085_127969_175667_178384_178631_179348_179430_179623_181133_181481_181588_182000_182238_182273_182530_182847_183035_183327_184010_184267_184441_184560_184735_184793_184811_185029_185224_185268_185517_185880_186038_186155_186316_186412_186595_186635_186662_186820_187021_187042_187045_187088_187121_187186_187287_187356_187386_187421_187432_187487_187529_187532_187669_187816_187828_187928_187965_188181_188224_188267_188427_188467_188592_188660_188664_188731_188741_188753_188844_188870_188895; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; __sec_t_key=cce29a96-15ef-4bd3-a6a8-23773d03e7a3; BDSFRCVID=rSLOJeC62iNH5gvHkEe1UuGOvzdh2N3TH6aoEzlQiY1CIFuQfD9CEG0Phf8g0Ku-S2MhogKK3mOTHmLF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tJIe_C-atC-3Hn7gMtTJq4FDhUn2etJyaR0H-CbvWJ5TMC_CbhjxbRDn2bJnyhQt32Oq-U74Wpj-ShPC-tnZD-vB-fJh-JohJ2nILDod3l02V-OIe-t2ynLV2xbRbtRMW20eWl7mWn6dsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjCKjjJ0ja_DtTn2aKn0WJ082R6oDn8k-PnVePk-Q-nZKxtqtJcDo-_MKqnSfUPm3JonXnKsLnuL0ponWncKWhj92-JvMnuG5tnkKM7D0fo405OTKHIO0KJc0Ro0Hpb4hPJvyTtDXnO72x7lXbrtXp7_2J0WStbKy4oTjxL1Db3JKjvMtIFtVDDbfIDhMCtrbDTD-tFO5eT22-us-H7r2hcH0KLKjqrSjtJ-y-PkbHQP-xb9bjQbBIoktMb1MRjvQJ6S0tF4DtbA0JQI5eP85h5TtUJseCnTDMRhqqJXXf7yKMnitKj9-pnEBpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKu-n5jHjjWeHAO3f; BDSFRCVID_BFESS=rSLOJeC62iNH5gvHkEe1UuGOvzdh2N3TH6aoEzlQiY1CIFuQfD9CEG0Phf8g0Ku-S2MhogKK3mOTHmLF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tJIe_C-atC-3Hn7gMtTJq4FDhUn2etJyaR0H-CbvWJ5TMC_CbhjxbRDn2bJnyhQt32Oq-U74Wpj-ShPC-tnZD-vB-fJh-JohJ2nILDod3l02V-OIe-t2ynLV2xbRbtRMW20eWl7mWn6dsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjCKjjJ0ja_DtTn2aKn0WJ082R6oDn8k-PnVePk-Q-nZKxtqtJcDo-_MKqnSfUPm3JonXnKsLnuL0ponWncKWhj92-JvMnuG5tnkKM7D0fo405OTKHIO0KJc0Ro0Hpb4hPJvyTtDXnO72x7lXbrtXp7_2J0WStbKy4oTjxL1Db3JKjvMtIFtVDDbfIDhMCtrbDTD-tFO5eT22-us-H7r2hcH0KLKjqrSjtJ-y-PkbHQP-xb9bjQbBIoktMb1MRjvQJ6S0tF4DtbA0JQI5eP85h5TtUJseCnTDMRhqqJXXf7yKMnitKj9-pnEBpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKu-n5jHjjWeHAO3f; delPer=0; PSINO=3; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BAIDUID_V4=B40E4A7F1CDE6456E004AC7DA7F38C1A:FG=1; BAIDUID=7A5466C3584FA9C09EFAF27F2962F84E:FG=1; BAIDUID_BFESS=7A5466C3584FA9C09EFAF27F2962F84E:FG=1; H_PS_PSSID=34445_35106_31254_35436_35456_34584_35491_35582_34579_35167_35320_26350_35478; BA_HECTOR=a4ak8525ag0l05809d1gs66ok0r; BDUSS=0dZRUUtR01PNXdld0o5dnpuWXc3UnJhVWJ4RFVMclBGN3dETkFkcXp-U3pxT3BoRVFBQUFBJCQAAAAAAAAAAAEAAABj1CQ3xOPOqrrOzaPWudbOwcYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALMbw2GzG8NhN; BDUSS_BFESS=0dZRUUtR01PNXdld0o5dnpuWXc3UnJhVWJ4RFVMclBGN3dETkFkcXp-U3pxT3BoRVFBQUFBJCQAAAAAAAAAAAEAAABj1CQ3xOPOqrrOzaPWudbOwcYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALMbw2GzG8NhN; Hm_lvt_71927aaa06a0dc9d2d16f927f1f6937f=1640170841,1640170995,1640176565,1640176572; Hm_lpvt_71927aaa06a0dc9d2d16f927f1f6937f=1640176572; ab_sr=1.0.1_ZDZiMjAwOTU1ZTc4YzRiNTM1OGQxOTlkYTY4MjJhZjU3ZDdlNzRlZWM2NGI1NDNhODE3YTA0MmUzNjMwNzgxMDgxYmU0ZTkyZTFjMDhlMjliZmY0ODk2NjdiMGRkNTExY2Y5YTFiYTM3MThjNThhNjk1MzA0OWU5Mzc4YjI1YTgxZWUzM2EwNzE3NzFkMTE0YjRjMTRkZWQxMjRhMjMwMg=='
    res = requests.post(url='https://miao.baidu.com/abdr',data=decode(),headers= {'Cookie':cookies,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.3611','Host':'miao.baidu.com','Content-Type':'text/plain;charset=UTF-8'})

    # 关键数据
    key = res.json()
    key['search']='110'
    print(key)

    res1 = requests.post(url="https://haoma.baidu.com/api/v1/appeal/search",headers={'Host':'haoma.baidu.com','User-Agent':'Openwave/ UCWEB7.0.2.37/28/999','Content-Type':'application/json;charset=UTF-8','Cookie':cookies,
                                                                                     'Origin':'https://haoma.baidu.com',
                                                                                     'Referer':'https://haoma.baidu.com/appeal','sec-ch-ua':'" Not '
                                                                                                                                            'A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'},data=json.dumps(key))
    print(res1.text)

