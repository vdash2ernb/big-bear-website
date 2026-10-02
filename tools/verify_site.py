"""Check every local page, reference, anchor, title, and JSON-LD block."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

root=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__()
        self.path=path; self.ids=[]; self.refs=[]; self.title=''; self.h1=0
        self.title_on=False; self.schema_on=False; self.schema=''; self.schemas=[]
        self.description=None; self.canonical=None
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.title_on=True
        if tag=='meta' and a.get('name')=='description':self.description=a.get('content')
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href')
        for key in ('src','href'):
            if a.get(key):self.refs.append(a[key])
        if a.get('srcset'):
            self.refs.extend(item.strip().split()[0] for item in a['srcset'].split(','))
        if tag=='img':assert 'alt' in a,f'{self.path}: missing image alt'
        if tag=='script' and a.get('type')=='application/ld+json':self.schema_on=True
    def handle_endtag(self,tag):
        if tag=='title':self.title_on=False
        if tag=='script' and self.schema_on:
            self.schemas.append(json.loads(self.schema)); self.schema_on=False; self.schema=''
    def handle_data(self,data):
        if self.title_on:self.title+=data
        if self.schema_on:self.schema+=data

pages={p.resolve():Page(p) for p in root.rglob('*.html')}
assert len(pages)==12,f'Expected 12 pages, found {len(pages)}'
titles=[]; descriptions=[]
for path,p in pages.items():
    assert p.h1==1,f'{path}: expected one H1'
    assert p.title and p.description and p.canonical and p.schemas,f'{path}: missing metadata'
    assert len(p.ids)==len(set(p.ids)),f'{path}: duplicate IDs'
    assert '{P}' not in path.read_text(encoding='utf-8'),f'{path}: unresolved template prefix'
    titles.append(p.title); descriptions.append(p.description)
    for ref in p.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc:continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        assert target.is_relative_to(root.resolve()),f'Outside public folder: {ref}'
        assert target.is_file(),f'{path.name}: missing {ref}'
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids,f'{path.name}: missing anchor {ref}'
assert len(titles)==len(set(titles)),'Duplicate titles'
assert len(descriptions)==len(set(descriptions)),'Duplicate descriptions'
print(f'PASS: {len(pages)} pages; local links, assets, anchors, unique metadata, headings, and JSON-LD.')
images=list((root/'images').glob('*.webp'))
print(f'{len(images)} responsive image files; {sum(p.stat().st_size for p in images)/1024:.0f} KiB total across all sizes.')
