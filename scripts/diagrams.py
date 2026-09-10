from pathlib import Path
from lxml import html
import re,json,zipfile
p=Path(site_dir)
pattern=re.compile(r'^```[^\n]*\n(.*?)^```\s*$',re.M|re.S)
report=[]
for md in sorted(Path('markdown').glob('page-*.md')):
    blocks=pattern.findall(md.read_text(encoding='utf-8'))
    f=p/md.with_suffix('.html').name
    d=html.parse(str(f),html.HTMLParser(encoding='utf-8'))
    pres=d.xpath('//article//pre')
    assert len(blocks)==len(pres),(md.name,len(blocks),len(pres))
    for i,(block,pre) in enumerate(zip(blocks,pres)):
        pre.clear();code=html.Element('code');code.text=block;pre.append(code)
        pre.set('tabindex','0');pre.set('aria-label','Source code or text diagram; scroll horizontally if needed')
        report.append({'page':f.name,'block':i+1,'matches_markdown':True})
    f.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode'),encoding='utf-8',newline='\n')
    verified=html.parse(str(f),html.HTMLParser(encoding='utf-8')).xpath('//article//pre')
    assert [e.text_content() for e in verified]==blocks,(f.name,[(repr(a),repr(b)) for a,b in zip(blocks,[e.text_content() for e in verified]) if a!=b])
with (p/'site.css').open('a',encoding='utf-8') as css:
    css.write('''article pre{white-space:pre;overflow-x:auto;overflow-wrap:normal;max-width:100%;tab-size:4}article pre code{display:block;padding:0;background:none;font-family:Consolas,"Courier New",monospace;font-size:13px;line-height:1.6;white-space:pre;overflow-wrap:normal;font-variant-ligatures:none}''')
Path('.build/diagram-verification.json').write_text(json.dumps(report,indent=2))
print('Verified',len(report),'source code and diagram blocks')
