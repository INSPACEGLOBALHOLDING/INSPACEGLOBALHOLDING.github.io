# -*- coding: utf-8 -*-
import io, json, re

def og_block(title, desc, url, image, sitename="Inspace Global Holding", typ="website"):
    def m(prop,val,attr="property"): return f'<meta {attr}="{prop}" content="{val}" />'
    lines=[
      f'<link rel="canonical" href="{url}" />',
      m("og:type",typ), m("og:site_name",sitename), m("og:title",title),
      m("og:description",desc), m("og:url",url), m("og:image",image), m("og:locale","en"), m("og:locale:alternate","zh_CN"),
      m("twitter:card","summary_large_image","name"), m("twitter:title",title,"name"),
      m("twitter:description",desc,"name"), m("twitter:image",image,"name"),
    ]
    return "\n".join(lines)

def jsonld(obj):
    return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>'

# ========== HOME ==========
p="index.html"; s=io.open(p,encoding="utf-8").read(); o=s
s=s.replace("<title>Inspace Global Holding Pte. Ltd.</title>",
            "<title>Inspace Global Holding — Green Steel &amp; AI Infrastructure in Aceh, Indonesia</title>",1)
old='<meta name="description" content="Singapore-based industrial and energy infrastructure development group, executing integrated EPC projects across Indonesia and Southeast Asia." />'
homedesc="Inspace Global Holding (IGH) is a Singapore-incorporated industrial holding group developing the Atjeh Quantum Industrial Park green steel complex (DRI-EAF, green-hydrogen ready) with co-located AI compute in Aceh, Indonesia — structured for project finance and EPC across Southeast Asia."
new=f'<meta name="description" content="{homedesc}" />\n<meta name="keywords" content="Inspace Global Holding, IGH, Atjeh Quantum Industrial Park, Aceh green steel, Indonesia green steel, DRI-EAF, green hydrogen, project finance, EPC, AI compute, KEK Special Economic Zone, decarbonization, Southeast Asia infrastructure" />'
assert old in s; s=s.replace(old,new,1)
# hero chip4 -> Project Finance (EN + zh)
assert 'data-i18n="hero.chip4">EPC Development</span>' in s
s=s.replace('data-i18n="hero.chip4">EPC Development</span>','data-i18n="hero.chip4">EPC &middot; Project Finance</span>',1)
s=s.replace("'hero.chip4': 'EPC 总承包',","'hero.chip4': 'EPC · 项目融资',",1)
org={"@context":"https://schema.org","@type":"Organization",
 "name":"Inspace Global Holding Pte. Ltd.","alternateName":["IGH","InSpace Global Holdings"],
 "url":"https://inspaceglobal.com/","logo":"https://inspaceglobal.com/favicon.svg",
 "description":homedesc,"foundingLocation":"Singapore",
 "areaServed":["Indonesia","Aceh","Southeast Asia"],
 "knowsAbout":["Green steel","DRI-EAF steelmaking","Green hydrogen","Decarbonization","Project finance","EPC","AI compute","KEK Special Economic Zone","CBAM"],
 "subOrganization":{"@type":"Organization","name":"PT Atjeh Quantum Industrial Group",
   "description":"Indonesian operating entity for the Atjeh Quantum Industrial Park green steel complex in Aceh, Indonesia."}}
inject = og_block("Inspace Global Holding — Green Steel & AI Infrastructure in Aceh, Indonesia", homedesc,
                  "https://inspaceglobal.com/","https://inspaceglobal.com/project-map.jpg")+"\n"+jsonld(org)+"\n</head>"
s=s.replace("</head>",inject,1)
io.open(p,"w",encoding="utf-8").write(s); print("HOME patched, +%d bytes"%(len(s)-len(o)))

# ========== AGSC ==========
p="projects/agsc/index.html"; s=io.open(p,encoding="utf-8").read(); o=s
s=s.replace("<title>AGSC — Aceh Integrated Green Steel Complex</title>",
            "<title>AGSC — Aceh Green Steel Complex at Atjeh Quantum Industrial Park | Inspace Global Holding</title>",1)
oldd='<meta name="description" content="Southeast Asia\'s First AI-Native Green Manufacturing Platform. From Indonesian Captive Ore to European Clean Mobility." />'
agdesc="The Aceh Integrated Green Steel Complex (AGSC) at Atjeh Quantum Industrial Park, KEK Southwest Aceh, Indonesia — a hydrogen-ready DRI-EAF green steel line with a co-located 100 MW AI supercomputing center, developed by PT Atjeh Quantum Industrial Group and structured for project finance and EPC engagement."
newd=f'<meta name="description" content="{agdesc}" />\n<meta name="keywords" content="Atjeh Quantum Industrial Park, PT Atjeh Quantum Industrial Group, AGSC, Aceh green steel, Indonesia green steel, DRI-EAF, green hydrogen, AI supercomputing, project finance, EPC, KEK Southwest Aceh, CBAM, Inspace Global Holding" />'
assert oldd in s, "agsc desc anchor missing"; s=s.replace(oldd,newd,1)
# visible Atjeh Quantum in hero region (EN + zh)
s=s.replace('data-i18n="hero.region">— KEK Southwest Aceh, Indonesia</span>',
            'data-i18n="hero.region">— Atjeh Quantum Industrial Park · KEK Southwest Aceh, Indonesia</span>',1)
s=s.replace("'hero.region': '— 印度尼西亚 亚齐西南 KEK 经济特区',",
            "'hero.region': '— Atjeh Quantum 工业园区 · 印度尼西亚 亚齐西南 KEK 经济特区',",1)
agorg={"@context":"https://schema.org","@type":"Organization",
 "name":"PT Atjeh Quantum Industrial Group","alternateName":["Atjeh Quantum Industrial Park","AGSC"],
 "url":"https://inspaceglobal.com/projects/agsc/",
 "parentOrganization":{"@type":"Organization","name":"Inspace Global Holding Pte. Ltd.","url":"https://inspaceglobal.com/"},
 "description":agdesc,"areaServed":["Indonesia","Aceh","European Union"],
 "knowsAbout":["Green steel","DRI-EAF","Green hydrogen","AI supercomputing","Project finance","EPC","CBAM","KEK Special Economic Zone"]}
inj = og_block("AGSC — Aceh Green Steel Complex at Atjeh Quantum Industrial Park", agdesc,
               "https://inspaceglobal.com/projects/agsc/","https://inspaceglobal.com/project-map.jpg",typ="article")+"\n"+jsonld(agorg)+"\n</head>"
s=s.replace("</head>",inj,1)
io.open(p,"w",encoding="utf-8").write(s); print("AGSC patched, +%d bytes"%(len(s)-len(o)))

# ========== robots.txt ==========
io.open("robots.txt","w",encoding="utf-8").write(
"User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: https://inspaceglobal.com/sitemap.xml\n")
print("robots.txt written")

# ========== sitemap.xml ==========
today="2026-08-09"
urls=[("https://inspaceglobal.com/","1.0"),
      ("https://inspaceglobal.com/news/","0.8"),
      ("https://inspaceglobal.com/projects/agsc/","0.9")]
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u,pr in urls:
    sm.append(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>')
sm.append('</urlset>')
io.open("sitemap.xml","w",encoding="utf-8").write("\n".join(sm)+"\n")
print("sitemap.xml written")
