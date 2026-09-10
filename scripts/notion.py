from pathlib import Path
from lxml import html
import copy
p=Path(site_dir)
parser=html.HTMLParser(encoding='utf-8')
# Recover exported page emoji icons that Markdown does not carry as page metadata.
import json
icons=json.loads(Path('scripts/icons.json').read_text(encoding='utf-8'))
for f in p.glob('page-*.html'):
    d=html.parse(str(f),parser);article=d.xpath('//article')[0]
    if f.name in icons:
        e=html.Element('div',{'class':'notion-icon','aria-hidden':'true'});e.text=icons[f.name];article.insert(0,e)
    f.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode'),encoding='utf-8')
d=html.parse(str(p/'index.html'),parser)
main=d.xpath('//main')[0];nav=d.xpath('//nav')[0]
main.clear();main.set('id','main');main.set('class','notion-home')
source=html.parse(str(Path(source_dir)/'page-48.html'),parser).xpath('//article')[0]
article=copy.deepcopy(source);article.set('class','notion-hub')
icon=html.Element('div',{'class':'notion-icon','aria-hidden':'true'});icon.text=icons.get('page-48.html','⌚');article.insert(0,icon)
# Preserve source ordering and wording while presenting Notion's directory groups as panels.
for heading in list(article.xpath('./h1')):
    if heading.text_content().strip() in ['System Components','Guides','Features']:
        panel=html.Element('section',{'class':'notion-panel'})
        heading.addprevious(panel);panel.append(heading)
        nxt=panel.getnext()
        while nxt is not None and nxt.tag not in ['h1','h2']:
            after=nxt.getnext();panel.append(nxt);nxt=after
for e in article.xpath('./p'):
    if e.text_content().lstrip().startswith('💡'):
        e.set('class','notion-welcome')
main.append(article)
search=html.Element('section',{'class':'notion-directory'})
h=html.Element('h2');h.text='Browse all documentation';search.append(h);search.append(nav);main.append(search)
(p/'index.html').write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode'),encoding='utf-8')
with (p/'site.css').open('a',encoding='utf-8') as f:
    f.write('''.notion-home{max-width:1040px;margin:0 auto;padding:48px 40px 70px}.notion-icon{font-size:64px;line-height:1.3;margin:0 0 20px}.notion-hub>h1:first-of-type{font-size:42px;letter-spacing:-1.4px;margin-top:0}.notion-hub{font-size:16px;line-height:1.85}.notion-hub h1:not(:first-of-type){font-size:26px;border-bottom:1px solid #e0e5dc;padding-bottom:10px;margin-top:36px}.notion-hub h2{font-size:25px;letter-spacing:-.5px}.notion-welcome{background:#edf3e8;border-left:4px solid #8da780;padding:20px 24px;border-radius:5px;color:#314e3c!important}.notion-panel{background:#f1f5ee;border:1px solid #dce6d6;border-radius:10px;padding:22px 28px;margin:28px 0}.notion-panel:nth-of-type(2){background:#f0f3f7}.notion-panel:nth-of-type(3){background:#f8f4eb}.notion-panel h1{margin:0 0 15px;font-size:25px}.notion-panel p{margin:8px 0}.notion-panel a{display:block;padding:7px 12px;border-radius:5px;text-decoration:none;background:#ffffff88;border:1px solid #dce4d980}.notion-panel a:hover{background:white}.notion-directory{margin-top:48px;border-top:1px solid #dce4d9;padding-top:20px}.notion-directory nav{position:static;height:400px;border:1px solid #dce4d9;border-radius:8px}.notion-hub li{margin:8px 0}@media(max-width:760px){.notion-home{padding:28px 22px}.notion-hub>h1:first-of-type{font-size:32px}.notion-icon{font-size:52px}.notion-panel{padding:18px}.notion-hub{font-size:15px}}''')
