#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by huangding 2017/7/9

import json
import execjs

# 金幣: https://i.loli.net/2021/02/06/CK9mOY3xGJdlvPa.png
# 布蘭克之匙: https://i.loli.net/2021/01/14/jnczI3KC4utls6Y.png
def loop(zhs, gjson_obj2):
    global notcount  # global声明
    # if zhs["id"] in ignoreid: continue
    # if zhs["id"]==1070: print(zhs["skill"][0]["tag"])
    # print(zhs["id"], zhs["skill"][0]["tag"])
    for zhs2 in gjson_obj2:
        if zhs2["id"] == "%03d" % zhs["id"]:
            for sk in zhs["skill"][0]["tag"]:
                if sk in ignore: continue
                if "tags" not in zhs2:
                    print(zhs["id"], zhs["skill"]);
                    notcount += 1
                    # continue
                    continue
                # if zhs["id"]==1070: print(sk)
                if isinstance(sk, list):
                    # print(zhs["id"], sk[0], " -----> ", zhs2["tags"], sk[0] in zhs2["tags"])
                    if sk[0] in ignore: continue
                    # if zhs["id"] in ignoreid or sk[0] !=_tag:continue
                    if sk[0] not in zhs2["tags"]:
                        print(50*'*')
                        print("A", zhs["id"], sk[0], zhs["skill"])
                        notcount += 1
                        continue
                else :
                    # if sk != _tag or zhs["id"] in ignoreid:continue
                    # print(zhs["id"], sk, " -----> ", zhs2["tags"], sk in zhs2["tags"])
                    for i in ignoreid: 
                        for j in i.keys():
                            if "%03d" % zhs["id"] == j and i[j]==sk:
                                # print("忽略................", i[j])
                                return
                    if sk and sk not in zhs2["tags"]:
                        print("B", zhs["id"], sk, zhs["skill"])
                        notcount += 1
                        continue

f = open('static/monster_data.js', encoding='utf-8')
res = f.read()
f.close()
# print(json.dumps(json.loads(res), ensure_ascii=False))
ctx = execjs.compile(res + ";function get() {return monster_data}")
gjson_obj = ctx.call("get")


f = open('static/monster_JSON1.json', encoding='utf-8')
res = f.read()
f.close()
gjson_obj2 = json.loads(res)
# for zhs2 in gjson_obj2:
# print(zhs2["id"], zhs2["tags"])

notcount = 0
# [0-9]{1,}[.]*[0-9]*[%]*
ignore = ["強制掉落", "直行引爆", "橫行引爆", "神族符石製造", "妖族符石製造", "龍族符石製造", "魔族符石製造", "獸族符石製造", "人族符石製造", "機械族符石製造"
, "", "符石轉火強化", "符石轉木強化", "符石轉光強化", "符石轉暗強化"
, "符石轉水", "符石轉火", "符石轉木", "符石轉光", "符石轉暗", "符石轉心", "符石兼具光", "符石兼具暗", "符石兼具水", "符石兼具火"
, "敵方傷害吸收", "共鳴"]
ignoreid=[2162, 2163,2280,2383] # 火屬追打
ignoreid=[2062, 2162, 2163,2280,2383] # 屬追打
ignoreid=[2403, 1753, 1755, 1986]
ignoreid=[{"2403": "減CD"}, {"2383": "火屬追打"}, {"2280": "水屬追打"}, {"2280": "火屬追打"}, {"2280": "木屬追打"}, {"2280": "暗屬追打"}
    , {"2163": "水屬追打"}, {"2163": "火屬追打"}, {"2163": "光屬追打"}
    , {"2162": "水屬追打"}, {"2162": "火屬追打"}, {"2162": "光屬追打"}
    , {"2139": "符石轉心強化"}, {"1983": "符石轉心強化"}, {"2062": "水屬追打"}, {"2062": "火屬追打"}, {"2062": "光屬追打"}, {"2062": "暗屬追打"}
    , {"1869": "對妖精類增傷"}]


_tag = None
for zhs in gjson_obj:
    loop(zhs, gjson_obj2)
print("不匹配总数", notcount)