# -*- coding: UTF-8 -*-
import json

from tencent_aiplat.apiutil import AiPlat

app_key = 'xxx'
app_id = 'xxx'

if __name__ == '__main__':
    str_text = '今天天气怎么样'
    type = 0
    ai_obj = AiPlat(app_id, app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.get_nlp_text_trans(str_text, type)
    if rsp['ret'] == 0:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        # print rsp
        print('----------------------API FAIL----------------------')
