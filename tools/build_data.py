import re,sys,json
sys.path.insert(0,'.')
from grid import parse
h=open('price.utf8.html',encoding='utf8').read()
tabs=re.findall(r'<table.*?</table>',h,re.S)
def nums(s): return [int(x) for x in re.findall(r'\d+',s)]
def cur87(x): return x*87//100
items=[]
# --- scroll / herb / ring table
g=parse(tabs[0])
groups=[('巻物',0),('草・種',3),('腕輪',6)]
for r in g[2:]:
    for cat,c in groups:
        name_cell,buy_cell,sell_cell=r[c],r[c+1],r[c+2]
        name=name_cell['txt'][0]; always=False
        if not name and name_cell['txt'][1]:
            name=name_cell['txt'][1]; always=True
        if not name or not buy_cell['txt'][0]: continue
        b=nums(buy_cell['txt'][0])[0]; s=nums(sell_cell['txt'][0])[0]
        bc=nums(buy_cell['txt'][1])[0] if buy_cell['txt'][1] else cur87(b)
        sc=nums(sell_cell['txt'][1])[0] if sell_cell['txt'][1] else cur87(s)
        known = name_cell['bg']=='#b0e0e6'
        prompt = name_cell['bg']=='#fafad2'
        v=[]
        if not always:
            v.append(dict(st='n',b=b,s=s))
            if cat in('巻物','草・種'): v.append(dict(st='b',b=b*2,s=s*2))
        v.append(dict(st='c',b=bc,s=sc))
        items.append(dict(cat=cat,name=name,known=known,prompt=prompt,always=always,v=v))
# --- staff / pot tables with capacity steps
def stepped(t,cat,maxcap=None):
    g=parse(t); out=[]
    for r in g[2:]:
        name=r[0]['txt'][0]
        if not name: continue
        rng=nums(r[1]['txt'][0]); lo,hi=rng[0],rng[-1]
        v=[]
        for k,cell in enumerate(r[3:]):
            n=lo+k
            if maxcap and n>maxcap: break
            bs=nums(cell['txt'][0]); b,s=bs[0],bs[1]
            cs=nums(cell['txt'][1]) if cell['txt'][1] else [cur87(b),cur87(s)]
            floor = n<=hi
            v.append(dict(st='n',b=b,s=s,n=n,fl=floor))
            v.append(dict(st='c',b=cs[0],s=cs[1],n=n,fl=floor))
        out.append(dict(cat=cat,name=name,known=False,prompt=False,always=False,lo=lo,hi=hi,v=v))
    return out
items+=stepped(tabs[1],'杖')
items+=stepped(tabs[2],'壺',6)
# cross-check with 杖/壺 detail pages' base values
json.dump(items,open('items.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print(Counter(i['cat'] for i in items), sum(len(i['v']) for i in items))
for i in items:
    if i['always'] or i['known'] or i['prompt']: print(i['cat'],i['name'],'always' if i['always'] else '', 'known' if i['known'] else '','prompt' if i['prompt'] else '')
