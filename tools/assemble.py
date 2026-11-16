import json,base64,io
from fontTools import subset
from fontTools.ttLib import TTFont
items=[i for i in json.load(open('items.json')) if not i['known']]
data=[]
for i in items:
    d={'c':i['cat'],'n':i['name']}
    if i['prompt']: d['p']=1
    v=[]
    for x in i['v']:
        row=[x['st'],x['b'],x['s']]
        if 'n' in x: row+=[x['n'],x['fl']]
        v.append(row)
    d['v']=v
    data.append(d)
data_json=json.dumps(data,ensure_ascii=False,separators=(',',':'))
t=open('template.html',encoding='utf8').read()
readings=json.load(open('readings.json',encoding='utf8'))
ws=json.load(open('ws_data.json',encoding='utf8'))
def ws_item(x): return {'n':x['n'],'base':x['base'],'slots':x['slots'],'buy':x['buy'],'seal':x['seal']}
ws_data={'weapons':[ws_item(x) for x in ws['weapons']],'shields':[ws_item(x) for x in ws['shields']],
         'seals':[{'k':x['k'],'no':x['no'],'ab':x['ab'],'n':x['n'],'nat':x['nat'],'buy':x['buy']} for x in ws['seals']]}  # 売値は使わない
ws_read=json.load(open('ws_readings.json',encoding='utf8'))
dump=lambda o: json.dumps(o,ensure_ascii=False,separators=(',',':'))
text=t.replace('/*DATA*/',data_json).replace('/*READINGS*/',dump(readings)).replace('/*WS*/',dump(ws_data)).replace('/*WSREAD*/',dump(ws_read))
chars=set(text)|set(chr(c) for c in range(0x20,0x7f))|set('、。・「」（）×✓…·→％％：／〜ー　')
chars|={chr(c) for c in range(0x3040,0x3100)}
import os
kit=os.environ.get('LINESEED_DIR','fonts/')
def sub(fn):
    opt=subset.Options(); opt.flavor='woff2'; opt.layout_features=['*']; opt.notdef_outline=True
    f=TTFont(kit+fn); s=subset.Subsetter(opt); s.populate(unicodes=[ord(c) for c in chars if ord(c)>0x1f]); s.subset(f)
    b=io.BytesIO(); f.flavor='woff2'; f.save(b); return base64.b64encode(b.getvalue()).decode()
reg=sub('LINESeedJP-Regular.woff2'); bold=sub('LINESeedJP-Bold.woff2')
out=text.replace('/*FONT_REG*/',reg).replace('/*FONT_BOLD*/',bold).replace('/*GTM*/',open('gtm.html',encoding='utf8').read().rstrip('\n'))
open('../public/index.html','w',encoding='utf8').write(out)
print(len(data),len(data_json),len(reg),len(bold),len(out))
