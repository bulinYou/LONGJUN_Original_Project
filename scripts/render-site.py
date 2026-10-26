"""Render independent static pages from a shared shell and extensible catalog."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from lxml import html, etree
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
CONTENT=json.loads((ROOT/'site/content.json').read_text())
EN=CONTENT['en']
SECTIONS=json.loads((ROOT/'site/sections.json').read_text())
PRODUCTS=json.loads((ROOT/'site/products.json').read_text())
MARKETS=json.loads((ROOT/'site/markets.json').read_text())
CATEGORIES=[('health','healthCategory','healthSummary'),('fragrance','fragranceCategory','fragranceSummary'),('derivatives','derivativesCategory','derivativesSummary')]
CAT={slug:(key,summary) for slug,key,summary in CATEGORIES}
CAT_IMAGES={'health':'sophora-health.webp','fragrance':'rosa-damascena.webp','derivatives':'derivatives-structure.svg'}
ASSETS={a['file']:a for a in json.loads((ROOT/'site/asset-sources.json').read_text())['assets']}
def t(key,tag='span',cls=''):
    return f'<{tag} data-i18n="{key}"'+(f' class="{cls}"' if cls else '')+'>'+escape(EN[key])+f'</{tag}>'
def link(route,key,cls='text-link'):
    return f'<a href="{route}" data-route class="{cls}">{t(key)}<span aria-hidden="true">↗</span></a>'
def head(eyebrow,line1,line2,intro):
    return '<section class="page-head page-width">'+t(eyebrow,'p','eyebrow')+'<h1>'+t(line1)+t(line2,'em')+'</h1>'+t(intro,'p','page-lead')+'</section>'
def photo_credit():
    return '<p class="history-image-note">'+t('historyImageNote')+' '+t('historyPhotoCredit')+' <a href="https://commons.wikimedia.org/wiki/File:PagodaTreeFlowers3.jpg">Fanghong / Wikimedia Commons</a> · <a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="license">CC BY-SA 3.0</a></p>'
def category_cards():
    return '<div class="category-grid">'+''.join('<a class="category-card" data-route href="/'+slug+'/"><div class="category-image"><img src="/assets/'+CAT_IMAGES[slug]+'" width="1200" height="800" alt="'+escape(EN[slug+'Alt'])+'" data-alt="'+slug+'Alt" loading="lazy" decoding="async"><span class="category-index">0'+str(i+1)+'</span></div><div class="category-card-copy">'+t(key,'h3')+t(summary,'p')+'<span class="card-link">'+t('viewProducts')+' <span aria-hidden="true">↗</span></span></div></a>' for i,(slug,key,summary) in enumerate(CATEGORIES))+'</div>'
def product_image(p):
    image_key=p['slug']+'StructureAlt' if p.get('isStructure') else p['imageAltKey']
    alt=escape(EN[image_key])
    altkey=' data-alt="'+image_key+'"'
    return '<img class="'+('structure-image' if p.get('isStructure') else 'botanical-image')+'" src="/assets/'+p['image']+'" width="900" height="900" alt="'+alt+'"'+altkey+' loading="lazy" decoding="async">'
def product_cards(products):
    cards=[]
    for p in products:
        cards.append('<a class="product-card" data-route href="/ingredients/'+p['slug']+'/"><div class="product-card-image">'+product_image(p)+'</div><div class="product-card-copy">'+t(CAT[p['category']][0],'p','eyebrow')+t(p['nameKey'],'h3')+'<p class="international-name" dir="ltr">'+escape(p['name'])+'</p>'+t(p['descriptionKey'],'p','card-description')+'<span class="card-link">'+t('viewProduct')+' <span aria-hidden="true">↗</span></span></div></a>')
    return '<div class="product-grid">'+''.join(cards)+'</div>'
def growth():
    return '<section class="growth-panel page-width">'+t('growthTitle','h2')+t('growthBody','p')+link('/contact/','navContact')+'</section>'
def map_block():
    return '<div class="world-map"><div class="map-legend"><span><i class="legend-client" aria-hidden="true"></i>'+t('mapClientLegend')+'</span><span><i class="legend-base" aria-hidden="true"></i>'+t('mapChinaLegend')+'</span></div><div class="map-viewport" tabindex="0" role="region" aria-label="Customer markets map" data-aria="mapRegionLabel"><img src="/assets/customer-markets.svg" width="1000" height="430" alt="'+escape(EN['mapAlt'])+'" data-alt="mapAlt" loading="lazy"></div>' + t('mapHint','p','map-hint') + '<ol class="market-list">'+''.join('<li><span class="market-number" dir="ltr">'+m['number']+'</span>'+t(m['nameKey'])+'</li>' for m in MARKETS)+'</ol>'+t('mapNote','p','map-note')+'<p class="map-source"><a href="https://www.naturalearthdata.com/about/terms-of-use/">'+t('sourceMap')+'</a></p></div>'
def evaluation(p):
    return '<section class="page-width section-space evaluation"><div>'+t('productInfoTitle','h2')+t('productInfoBody','p')+t('productInfoBody2','p')+'</div>'+link('/contact/?material='+p['slug']+'#enquiry','discussMaterial','button button-dark')+'</section>'
def breadcrumb(category=None):
    return '<nav class="breadcrumbs page-width" aria-label="Page navigation" data-aria="breadcrumbLabel">'+link('/ingredients/','allIngredients','')+(('<span aria-hidden="true">/</span>'+link('/'+category+'/',CAT[category][0],'')) if category else '')+'</nav>'
def buying_path():
    return '<section class="buying-path"><div class="page-width section-space">'+t('flowEyebrow','p','eyebrow')+t('flowTitle','h2')+'<ol class="buying-steps">'+''.join('<li><span class="step-number">0'+str(i)+'</span>'+t(f'flow{i}Title','h3')+t(f'flow{i}Body','p')+'</li>' for i in range(1,5))+'</ol>'+link('/contact/#enquiry','navContact','text-link')+'</div></section>'
def related():
    return '<section class="page-width related-block">'+t('relatedTitle','h2')+'<div>'+link('/quality/','qualityPageTitle')+link('/contact/#enquiry','navContact')+link('/ingredients/','allIngredients')+'</div></section>'

pages=[]
home=SECTIONS['hero']+'<section class="page-width section-space home-catalog">'+t('catalogEyebrow','p','eyebrow')+'<h2>'+t('catalogTitle1')+t('catalogTitle2','em')+'</h2>'+t('catalogIntro','p','section-intro')+category_cards()+'</section>'
home+='<section class="signature-preview"><div class="page-width signature-grid"><img src="/assets/rose-oil.webp" width="1122" height="1402" alt="'+escape(EN['oilAlt'])+'" data-alt="oilAlt" loading="lazy"><div>'+t('roseEyebrow','p','eyebrow')+t('roseTitle','h2')+'<p class="botanical-name" lang="la">Rosa damascena</p>'+t('fragranceSummary','p')+link('/ingredients/rose-otto/','viewProduct','button button-dark')+link('/fragrance/','fragranceCategory')+'</div></div></section>'
home+=buying_path()
home+='<section class="home-story"><div class="page-width story-preview"><img src="/assets/sophora-heritage.jpg" width="2560" height="1920" alt="'+escape(EN['historyRootsAlt'])+'" data-alt="historyRootsAlt" loading="lazy"><div>'+t('historyEyebrow','p','eyebrow')+t('homeHistoryTitle','h2')+t('homeHistoryBody','p')+link('/history/','navHistory')+link('/about/','navWorld')+'</div></div><div class="page-width">'+photo_credit()+'</div></section>'
home+=related()
pages.append(('', 'home',home,{}))

about=head('aboutEyebrow','aboutTitle1','aboutTitle2','aboutIntro')
about+='<section class="page-width about-detail"><figure class="about-logo"><img src="/assets/longjun-logo.png" width="1254" height="1254" alt="'+escape(EN['logoAlt'])+'" data-alt="logoAlt"><figcaption>SICHUAN LONGJUN INTERNATIONAL · 2008</figcaption></figure><div>'+t('aboutBody1','p')+t('aboutBody2','p')+link('/history/','navHistory')+'</div></section>'
about+='<section class="page-width section-space">'+t('aboutBusinessTitle','h2')+category_cards()+'</section><section class="soft-section"><div class="page-width section-space prose-columns"><article>'+t('aboutNetworkTitle','h2')+t('aboutNetworkBody','p')+link('/markets/','navMarkets')+'</article><article>'+t('aboutValuesTitle','h2')+t('aboutValuesBody','p')+link('/quality/','navQuality')+'</article></div></section>'
pages.append(('about','about',about,{}))

history=head('historyEyebrow','historyTitle1','historyTitle2','historyIntro')
history+='<section class="page-width story-gallery"><figure><img src="/assets/sophora-heritage.jpg" width="2560" height="1920" alt="'+escape(EN['historyRootsAlt'])+'" data-alt="historyRootsAlt" loading="lazy"><figcaption>'+t('historyRootsCaption')+'</figcaption></figure><figure><img src="/assets/rose-oil.webp" width="1122" height="1402" alt="'+escape(EN['historyRoseAlt'])+'" data-alt="historyRoseAlt" loading="lazy"><figcaption>'+t('historyRoseCaption')+'</figcaption></figure></section>'
history+='<section class="page-width history-long"><h2 class="sr-only">'+t('historyDetailLead')+'</h2>'
for i in range(1,7):
    history+='<article class="history-chapter"><div class="chapter-period"><span aria-hidden="true">0'+str(i)+'</span>'+t(f'h{i}Period','p')+'</div><div>'+t(f'h{i}Title','h2')+t(f'h{i}Body','p')+t(f'h{i}More','p')
    if i==3:history+=link('/health/','healthCategory')+' '+link('/derivatives/','derivativesCategory')
    if i==4:history+=link('/markets/','navMarkets')
    if i==5:history+=link('/fragrance/','fragranceCategory')+' '+link('/ingredients/rose-hydrosol/','hydrosolName')
    history+='</div></article>'
history+=photo_credit()+'</section><section class="growth-panel page-width">'+t('historyCloseTitle','h2')+t('historyCloseBody','p')+link('/ingredients/','viewProducts')+'</section>'
pages.append(('history','history',history,{}))

catalog=head('catalogEyebrow','catalogTitle1','catalogTitle2','catalogIntro')+'<section class="page-width">'+category_cards()+'</section>'
for slug,key,summary in CATEGORIES:
    catalog+='<section class="page-width section-space catalog-group"><div class="section-top">'+t(key,'h2')+link('/'+slug+'/','viewProducts')+'</div>'+product_cards([p for p in PRODUCTS if p['category']==slug])+'</section>'
catalog+=growth()
pages.append(('ingredients','ingredients',catalog,{}))
for slug,key,summary in CATEGORIES:
    body=breadcrumb()+'<section class="category-hero page-width"><div>'+t('catalogEyebrow','p','eyebrow')+t(key,'h1')+t(slug+'Intro','p','page-lead')+link('#materials','viewProducts','text-link')+'</div><figure><img src="/assets/'+CAT_IMAGES[slug]+'" width="1200" height="800" alt="'+escape(EN[slug+'Alt'])+'" data-alt="'+slug+'Alt" fetchpriority="high"><figcaption>'+t(slug+'Caption')+'</figcaption></figure></section><section class="page-width category-products" id="materials">'+t('currentRange','h2','eyebrow')+product_cards([p for p in PRODUCTS if p['category']==slug])+t('professionalNote','p','professional-note')+'</section>'+related()+growth()
    pages.append((slug,slug,body,{'data-title-key':key}))
for p in PRODUCTS:
    body=breadcrumb(p['category'])
    if p['slug']=='rose-otto':
        body+=SECTIONS['rose'].replace('<h2 id="rose-title"','<h1 id="rose-title"').replace('Rose Otto</h2>','Rose Otto</h1>').replace('href="#contact"','href="/contact/?material=rose-otto#enquiry" data-route')
    else:
        body+='<section class="page-width product-detail"><div>'+t(CAT[p['category']][0],'p','eyebrow')+t(p['nameKey'],'h1')+'<p class="international-name" dir="ltr">'+escape(p['name'])+'</p>'+t(p['descriptionKey'],'p','page-lead')+'<dl class="specifications"><div>'+t('productInternationalName','dt')+'<dd dir="ltr">'+escape(p['name'])+'</dd></div><div>'+t('productCategoryLabel','dt')+'<dd>'+t(CAT[p['category']][0])+'</dd></div><div>'+t('productOfferLabel','dt')+'<dd>'+t('productOfferValue')+'</dd></div>'
        if p['slug']=='rose-hydrosol':body+='<div>'+t('sourceLabel','dt')+'<dd>'+t('sourceValue')+'</dd></div>'
        body+='</dl></div><aside class="product-aside">'
        body+='<figure>'+product_image(p)
        if p.get('isStructure'):
            asset=ASSETS[p['image']]
            body+='<figcaption><span dir="ltr">'+escape(asset['subject'])+' · <a href="'+asset['source_url']+'">PubChem CID '+str(asset['pubchem_cid'])+'</a></span>'+t('structureNote','p')+'</figcaption>'
        else:body+='<figcaption>'+t('fragranceCaption')+'</figcaption>'
        body+='</figure>'
        body+='</aside></section>'
    body+=evaluation(p)+related()
    pages.append(('ingredients/'+p['slug'],'ingredients',body,{'data-title-key':p['nameKey']}))

markets=head('marketsEyebrow','marketsTitle1','marketsTitle2','marketsIntro')+'<section class="page-width">'+map_block()+'</section><section class="page-width section-space prose-columns"><article>'+t('marketsNetworkTitle','h2')+t('marketsNetworkBody','p')+link('/contact/','navContact')+'</article><article>'+t('marketsDomesticTitle','h2')+t('marketsDomesticBody','p')+link('/ingredients/','allIngredients')+'</article></section>'
pages.append(('markets','markets',markets,{}))
quality=SECTIONS['quality'].replace('<h2 id="quality-title"','<h1 id="quality-title"').replace('</em></h2>','</em></h1>')+'<section class="page-width section-space prose-columns"><article>'+t('productInfoTitle','h2')+t('productInfoBody','p')+'</article><article>'+t('productOfferLabel','h2')+t('productInfoBody2','p')+link('/contact/','navContact')+'</article></section>'
pages.append(('quality','quality',quality+buying_path(),{}))
contact=SECTIONS['contact'].replace('<h2 id="contact-title"','<h1 id="contact-title"').replace('</em></h2>','</em></h1>')
contact+='<section class="page-width enquiry-section" id="enquiry"><div class="enquiry-heading">'+t('formTitle','h2')+t('formIntro','p')+t('formRequired','small')+'</div><form id="enquiry-form" class="enquiry-form"><div class="field full"><label for="material">'+t('materialField')+' *</label><select id="material" name="material" required><option value="" data-i18n="chooseMaterial">'+EN['chooseMaterial']+'</option>'+''.join('<option value="'+p['slug']+'" data-name="'+p['name']+'" data-i18n="'+p['nameKey']+'">'+EN[p['nameKey']]+'</option>' for p in PRODUCTS)+'<option value="other" data-i18n="otherMaterial">'+EN['otherMaterial']+'</option></select></div>'
for field,key,required,kind in [('application','applicationField',True,'text'),('destination','destinationField',True,'text'),('quantity','quantityField',False,'text'),('company','companyField',False,'text'),('email','emailField',False,'email')]:
    contact+='<div class="field"><label for="'+field+'">'+t(key)+(' *' if required else '')+'</label><input id="'+field+'" name="'+field+'" type="'+kind+'" maxlength="180"'+(' required' if required else '')+(' autocomplete="email" dir="ltr"' if kind=='email' else '')+'></div>'
contact+='<div class="field full"><label for="requirements">'+t('documentsField')+'</label><textarea id="requirements" name="requirements" rows="4" maxlength="1800"></textarea></div><div class="form-actions full"><button type="submit" class="button button-dark">'+t('formSubmit')+'<span aria-hidden="true">↗</span></button><button type="button" id="copy-enquiry" class="text-link">'+t('copyEnquiry')+'</button></div>'+t('formNote','p','form-note full')+'<p id="form-status" class="form-status full" role="status" aria-live="polite"></p><div class="field full enquiry-result" id="enquiry-result" hidden><label for="enquiry-draft">'+t('draftLabel')+'</label><textarea id="enquiry-draft" readonly rows="12"></textarea><a id="open-email" class="button button-dark" href="mailto:yutengma@longjunintl.com">'+t('openEmail')+'<span aria-hidden="true">↗</span></a></div></form></section>'
pages.append(('contact','contact',contact,{}))

ROUTES={'#world':'/about/','#history':'/history/','#rose':'/ingredients/rose-otto/','#quality':'/quality/','#contact':'/contact/#enquiry'}
# Remove obsolete public pages. The old taxonomy is retained only as redirects.
for obsolete in ['origin','ingredients/plant-extracts','ingredients/essential-oils','ingredients/hydrosols']:
    target=ROOT/'dist'/obsolete
    if target.exists():shutil.rmtree(target)
for route,page,body,attrs in pages:
    doc=html.fromstring((ROOT/'site/shell.html').read_text())
    main=doc.xpath('//main')[0]
    for fragment in html.fragments_fromstring(body):main.append(fragment)
    doc.xpath('//body')[0].set('data-page',page)
    for k,v in attrs.items():doc.xpath('//body')[0].set(k,v)
    for el in doc.xpath('//*[@data-i18n]'):el.text=EN[el.get('data-i18n')]
    for el in doc.xpath('//*[@data-alt]'):el.set('alt',EN[el.get('data-alt')])
    for el in doc.xpath('//*[@data-aria]'):el.set('aria-label',EN[el.get('data-aria')])
    for el in doc.xpath('//a'):
        href=el.get('href','')
        if href in ROUTES:el.set('href',ROUTES[href]);el.set('data-route','')
        if el.get('data-mail')=='documentation':
            del el.attrib['data-mail'];el.set('href','/contact/?request=documents#enquiry');el.set('data-route','')
        elif page=='contact' and el.get('data-mail')=='enquiry':
            del el.attrib['data-mail'];el.set('href','#enquiry');el.set('data-route','')
    for el in doc.xpath('//*[@id="main-nav"]/a'):
        if el.get('href')==f'/{page}/':el.set('aria-current','page')
        if el.get('href')=='/contact/':el.set('class','mobile-contact')
        if page=='ingredients' and attrs.get('data-title-key') in [p['nameKey'] for p in PRODUCTS]:
            product=next(p for p in PRODUCTS if p['nameKey']==attrs['data-title-key'])
            if el.get('href')=='/'+product['category']+'/':el.set('aria-current','page')
    title_key=attrs.get('data-title-key',page+'PageTitle')
    doc.xpath('//title')[0].text=EN.get(title_key,EN['title'])+(' | LONGJUN' if title_key in EN else '')
    doc.xpath('//meta[@name="description"]')[0].set('content',EN['metaDescription'])
    target=ROOT/'dist'/route/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('<!doctype html>\n'+etree.tostring(doc,encoding='unicode',method='html'))
(ROOT/'dist/translations.js').write_text('window.LONGJUN_TRANSLATIONS = '+json.dumps(CONTENT,ensure_ascii=False,separators=(',',':'))+';\n')
(ROOT/'dist/_redirects').write_text('/origin /ingredients/ 301\n/origin/ /ingredients/ 301\n/ingredients/plant-extracts/ /ingredients/ 301\n/ingredients/essential-oils/ /fragrance/ 301\n/ingredients/hydrosols/ /derivatives/ 301\n')
print(f'Rendered {len(pages)} independent pages with {len(PRODUCTS)} current products in {len(CATEGORIES)} categories.')
