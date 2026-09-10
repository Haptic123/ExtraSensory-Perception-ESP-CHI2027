"""Build the static documentation from the editable Markdown files."""
from pathlib import Path
from lxml import html
from html import escape
from urllib.parse import urlsplit
import markdown,runpy,os
os.chdir(Path(__file__).resolve().parent.parent)
out=Path('.build/rendered');out.mkdir(parents=True,exist_ok=True)
for source in sorted(Path('markdown').glob('page-*.md')):
    text=source.read_text(encoding='utf-8')
    rendered=markdown.markdown(text,extensions=['tables','fenced_code','sane_lists'])
    article=html.fragment_fromstring(rendered,create_parent='article')
    headings=article.xpath('.//h1')
    if not headings:raise ValueError(f'{source}: add a # page title')
    title=headings[0].text_content()
    for a in article.xpath('.//a[@href]'):
        href=a.get('href');url=urlsplit(href)
        if not url.scheme and url.path.endswith('.md'):
            a.set('href',url.path[:-3]+'.html'+('#'+url.fragment if url.fragment else ''))
    for e in article.xpath('.//script|.//iframe|.//object|.//embed'):
        raise ValueError(f'{source}: unsupported embedded content {e.tag}')
    page='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body>'+html.tostring(article,encoding='unicode')+'</body></html>'
    (out/source.with_suffix('.html').name).write_text(page,encoding='utf-8',newline='\n')
runpy.run_path('scripts/layout.py')
