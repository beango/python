# f=open(r'/home/beango/MPPB.dat',encoding='gbk')
# print(f)
with open('/home/beango/MPPB.dat', encoding='utf-8',) as id_json: #打开json包
    print(id_json.read())
    print(type(id_json))
# sentimentlist = []
# for line in f:
#     s = line.strip().split('\t')
#     sentimentlist.append(s)
# f.close()
# df_train=pd.DataFrame(sentimentlist,columns=['s_no','deal_code','text'])