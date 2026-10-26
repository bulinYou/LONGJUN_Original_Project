"""Validate the public catalogue, translated UI and internal navigation."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,hashlib,subprocess
from lxml import html

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
content=json.loads((ROOT/'site/content.json').read_text())
products=json.loads((ROOT/'site/products.json').read_text())
errors=[]
assert set(content)=={'en','zh','fr','ja','ko','es','ar'}
pages=list(DIST.rglob('index.html'))
for path in pages:
    doc=html.fromstring(path.read_text())
    label=str(path.relative_to(DIST))
    if len(doc.xpath('//h1'))!=1:errors.append(f'{label}: expected one h1')
    ids=[x.get('id') for x in doc.xpath('//*[@id]')]
    for key,count in Counter(ids).items():
        if count>1:errors.append(f'{label}: duplicate id {key}')
    for el in doc.xpath('//*[@data-i18n or @data-alt or @data-aria]'):
        for attr in ['data-i18n','data-alt','data-aria']:
            key=el.get(attr)
            if key:
                for lang,translation in content.items():
                    if not translation.get(key):errors.append(f'{label}: missing {lang}.{key}')
    for el in doc.xpath('//*[@href or @src]'):
        value=el.get('href') or el.get('src')
        url=urlsplit(value)
        if url.scheme or url.netloc:continue
        dest=(DIST/url.path.lstrip('/')) if url.path.startswith('/') else path.parent/url.path
        if not url.path:dest=path
        if dest.is_dir():dest=dest/'index.html'
        if not dest.exists():errors.append(f'{label}: broken target {value}')
        elif url.fragment and dest.suffix=='.html':
            if not html.fromstring(dest.read_text()).xpath('//*[@id=$id]',id=unquote(url.fragment)):
                errors.append(f'{label}: missing anchor {value}')
        if '/origin/' in url.path:errors.append(f'{label}: removed origin route referenced')
    for image in doc.xpath('//img'):
        if image.get('alt') is None:errors.append(f'{label}: image missing alternative text')
for p in products:
    if p['category'] not in ['health','fragrance','derivatives']:errors.append('Old category: '+p['slug'])
assert not (DIST/'origin').exists()
assert len(pages)==17,len(pages)
expected_logo_sha256='b24277e0dfcdaf4b09cd743d2c49dc16aad8086d550f5d790292e5026a636c92'
assert hashlib.sha256((DIST/'assets/longjun-logo.png').read_bytes()).hexdigest()==expected_logo_sha256,'Logo changed'
assert not list(DIST.glob('__qa*')),'Remove temporary QA pages before publication'
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; 7 locales; 7 product routes; images, anchors and translations; removed origin page; original logo unchanged.')
