import re,html
def cell_text(inner):
    # returns (normal text, cursed text or None)
    m=re.search(r'<span[^>]*>(.*?)</span>',inner,re.S)
    cursed=None
    if m:
        cursed=re.sub(r'<[^>]+>','',m.group(1)).strip()
    t=re.sub(r'<span[^>]*>.*?</span>','',inner,flags=re.S)
    t=re.sub(r'<br\s*/?>','\n',t)
    t=html.unescape(re.sub(r'<[^>]+>','',t)).strip()
    return t,cursed
def parse(table):
    rows=re.findall(r'<tr.*?</tr>',table,re.S)
    grid=[];pending={}
    for r,row in enumerate(rows):
        cells=re.findall(r'<(t[hd])([^>]*)>(.*?)</\1>',row,re.S)
        out={};c=0
        for tag,attrs,inner in cells:
            while c in pending and pending[c][0]>0:
                n,v=pending[c]; out[c]=v; pending[c]=(n-1,v); c+=1
            rs=int(re.search(r'rowspan="?(\d+)',attrs).group(1)) if 'rowspan' in attrs else 1
            cs=int(re.search(r'colspan="?(\d+)',attrs).group(1)) if 'colspan' in attrs else 1
            bg=re.search(r'background-color:\s*(#[0-9a-fA-F]+)',attrs)
            val=dict(tag=tag,txt=cell_text(inner),bg=bg.group(1).lower() if bg else None,span=(rs>1 or cs>1))
            for k in range(cs):
                out[c+k]=val
                if rs>1: pending[c+k]=(rs-1,val)
            c+=cs
        while c in pending and pending[c][0]>0:
            n,v=pending[c]; out[c]=v; pending[c]=(n-1,v); c+=1
        grid.append([out[i] for i in sorted(out)])
    return grid
