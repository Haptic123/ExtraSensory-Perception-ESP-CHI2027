from pathlib import Path
from lxml import html
from html import escape
import json,re,os
src=Path('.build/rendered'); dst=Path('_site'); dst.mkdir(exist_ok=True)
pages=[]
for p in sorted(src.glob('page-*.html')):
    d=html.parse(str(p),parser=html.HTMLParser(encoding='utf-8')); article=d.xpath('//article')[0]
    for e in article.xpath('.//link | .//script | .//style'):
        e.drop_tree()
    for a in article.xpath('.//a[@href]'):
        if 'REMOVED' in a.get('href','') or 'REDACTED' in a.get('href',''): a.drop_tag()
    title=d.xpath('//title/text()')[0].strip()
    pages.append((p.name,title,html.tostring(article,encoding='unicode'),article.text_content()))
css='''*{box-sizing:border-box}body{margin:0;color:#20323e;background:#f6f8fa;font:16px/1.7 system-ui,sans-serif}a{color:#12687b}a:hover{text-decoration:underline}header.site{background:#123640;color:white;padding:22px 32px}header.site a{color:white;text-decoration:none;font-size:21px;font-weight:650}header.site p{margin:2px 0;color:#c4d9de;font-size:14px}.layout{display:grid;grid-template-columns:285px minmax(0,1fr);max-width:1450px;margin:auto}nav{padding:24px 20px;border-right:1px solid #dce4e8;height:calc(100vh - 110px);position:sticky;top:0;overflow:auto}nav a{display:block;padding:6px 10px;border-radius:5px;text-decoration:none;font-size:14px;line-height:1.5}nav a[aria-current]{background:#dcecf0;font-weight:650}input{width:100%;padding:11px;border:1px solid #9cb1ba;border-radius:6px;margin:8px 0 16px;font:inherit}main{padding:32px 48px;min-width:0;background:white}article{max-width:900px}h1{line-height:1.25;font-size:2rem}h2{margin-top:2rem}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f7;padding:16px;border-radius:8px}code{overflow-wrap:anywhere}table{display:block;overflow:auto;border-collapse:collapse;max-width:100%}td,th{border:1px solid #dce4e8;padding:8px}aside.callout{padding:16px;background:#edf5f6;border-radius:8px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}.card{padding:18px;border:1px solid #dce4e8;border-radius:8px;text-decoration:none}.card:hover{background:#edf5f6}footer{margin-top:36px;padding-top:20px;border-top:1px solid #dce4e8;color:#5c6f78;font-size:13px}.skip{position:absolute;left:-9999px}.skip:focus{left:12px;background:white;padding:8px}#empty{font-size:14px}@media(max-width:760px){.layout{display:block}nav{position:static;height:auto;max-height:280px;border-bottom:1px solid #dce4e8}main{padding:24px 20px}header.site{padding:18px 20px}}'''
(dst/'site.css').write_text(css+'[hidden]{display:none!important}')
(dst/'search.js').write_text('''const input=document.querySelector('#search');const links=[...document.querySelectorAll('nav a[data-search]')];input.addEventListener('input',()=>{const terms=input.value.toLowerCase().trim().split(/\\s+/);let count=0;for(const a of links){const match=terms.every(t=>a.dataset.search.includes(t));a.hidden=!match;if(match)count++;}document.querySelector('#empty').hidden=count>0;});''')
def shell(name,title,body):
    nav=''.join(f'<a href="{n}" data-search="{escape((t+" "+text).lower(),quote=True)}"'+(' aria-current="page"' if n==name else '')+f'>{escape(t)}</a>' for n,t,_,text in pages)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{escape(title)} | Haptic Feedback Documentation</title><link rel="stylesheet" href="site.css"><script defer src="search.js"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site"><a href="index.html">Haptic Feedback Documentation</a><p>System guides · Applications · Backend</p></header><div class="layout"><nav aria-label="Documentation"><a href="index.html">Documentation home</a><label for="search">Search documentation</label><input id="search" type="search" placeholder="Search topics or page content…">{nav}<p id="empty" role="status" hidden>No matching pages.</p></nav><main id="main">{body}<footer>Anonymous review documentation. Identifying media, attachments and credentials are omitted from this edition.</footer></main></div></body></html>'''
for n,t,body,_ in pages:(dst/n).write_text(shell(n,t,body),encoding='utf-8')
groups=[('Start here','Architecture, installation and the system overview.',[48,45,18,19]),('Phone & watch','Set up devices, sensors and haptic feedback.',[8,44,2,6,42]),('Researcher dashboard','Manage users, mappings and study schedules.',[34,28,33,30,35]),('Backend & database','Workflows, data structures and configuration.',[27,23,17,37])]
cards=''.join(f'<section class="card"><h2>{title}</h2><p>{desc}</p>'+''.join(f'<p><a href="page-{i:02}.html">{escape(pages[i-1][1])}</a></p>' for i in nums)+'</section>' for title,desc,nums in groups)
(dst/'index.html').write_text(shell('index.html','Home','<h1>Explore the haptic feedback system</h1><p>Guides to the smartwatch, phone relay, researcher dashboard and automation backend. Browse a topic below or search all 48 pages.</p><div class="cards">'+cards+'</div>'),encoding='utf-8')
(dst/'.nojekyll').write_text('')
import runpy
runpy.run_path('scripts/design.py',init_globals={'site_dir':dst})
runpy.run_path('scripts/notion.py',init_globals={'site_dir':dst,'source_dir':src})
runpy.run_path('scripts/diagrams.py',init_globals={'site_dir':dst})
# All links and assets must resolve locally; the site loads no external resources.
links=0
for p in dst.glob('*.html'):
    d=html.parse(str(p))
    for url in d.xpath('//@href | //@src'):
        if url.startswith('#'):continue
        assert not re.match(r'^[a-z]+:',url,re.I),(p,url)
        assert (dst/url.split('#')[0]).exists(),(p,url)
        links+=1
print(json.dumps({'pages':len(pages),'checked_links_and_assets':links,'output':str(dst)}))
