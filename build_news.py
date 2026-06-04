# -*- coding: utf-8 -*-
import io, re, json, html

src = io.open("index.html", encoding="utf-8").read()

def grab(pattern, s, flags=re.S):
    m = re.search(pattern, s, flags)
    if not m:
        raise SystemExit("could not extract: " + pattern[:40])
    return m.group(1)

head      = grab(r"<head>(.*?)</head>", src)
header    = grab(r"(<header.*?</header>)", src)
footer    = grab(r"(<footer.*?</footer>)", src)
scripts   = re.findall(r"<script>.*?</script>", src, re.S)
reveal_js = next(x for x in scripts if "IntersectionObserver" in x)
dict_js   = next(x for x in scripts if "const I18N" in x)
lang_js   = next(x for x in scripts if "STORAGE_KEY" in x)

# nav for subpage: point anchors back to homepage
nav = header.replace('href="#', 'href="/#').replace('<a href="/#"', '<a href="/"')

data = json.load(io.open("news/data.json", encoding="utf-8"))
issues = sorted(data["issues"], key=lambda i: i["sort_date"], reverse=True)

def L(en, zh):
    return ('<span class="lang-en">' + en + '</span>'
            '<span class="lang-zh">' + zh + '</span>')

# ---------- build news page cards ----------
cards = []
for it in issues:
    rows = []
    for n, q in enumerate(it["items"], 1):
        rows.append(
f'''        <details class="brief">
          <summary><span class="qn">{n:02d}</span><span class="qt">{L(html.escape(q["t_en"]), html.escape(q["t_zh"]))}</span><span class="chev">&rsaquo;</span></summary>
          <div class="qb">{L(html.escape(q["b_en"]), html.escape(q["b_zh"]))}</div>
        </details>''')
    cards.append(
f'''      <article id="{it["id"]}" class="reveal panel rounded-lg p-8 sm:p-10 scroll-mt-28">
        <div class="flex items-center gap-3 mb-5 flex-wrap">
          <span class="chip">{L(it["date_en"], it["date_zh"])}</span>
          <span class="label">{L(it["tags_en"], it["tags_zh"])}</span>
        </div>
        <h2 class="font-serif text-2xl sm:text-3xl leading-snug mb-4">{L(html.escape(it["title_en"]), html.escape(it["title_zh"]))}</h2>
        <p class="text-stone font-light leading-relaxed mb-2">{L(html.escape(it["intro_en"]), html.escape(it["intro_zh"]))}</p>
{chr(10).join(rows)}
      </article>''')

extra_css = '''<style>
  .lang-zh{display:none;}
  body[data-lang="zh"] .lang-en{display:none;}
  body[data-lang="zh"] .lang-zh{display:revert;}
  details.brief>summary{list-style:none;cursor:pointer;display:flex;gap:14px;align-items:baseline;padding:18px 0;transition:color .25s ease;border-top:1px solid rgba(255,255,255,.07);}
  details.brief>summary::-webkit-details-marker{display:none;}
  details.brief>summary:hover{color:#E3CFA0;}
  details.brief .qn{font-family:'Spline Sans Mono',monospace;color:var(--champ);font-size:13px;flex:none;}
  details.brief .qt{font-family:'Fraunces',serif;font-size:18px;line-height:1.45;}
  details.brief .chev{margin-left:auto;color:var(--champ);transition:transform .3s ease;flex:none;font-size:20px;}
  details.brief[open]>summary .chev{transform:rotate(90deg);}
  details.brief .qb{color:#c9d2cb;font-weight:300;line-height:1.85;padding:2px 0 22px 34px;font-size:15px;}
</style>'''

news_html = f'''<!DOCTYPE html>
<html lang="en">
<head>{head}{extra_css}
<title>Market Intelligence · Inspace Global Holding Pte. Ltd.</title>
</head>
<body>
<div class="grain"></div>
{nav}
<main class="pt-[68px]">
  <section class="relative pt-24 pb-14 overflow-hidden" style="background:radial-gradient(130% 90% at 70% 0%, #1a3a2a 0%, #13291e 42%, #0d1f16 100%);">
    <div class="aura" style="width:520px;height:520px;background:rgba(45,125,70,.2);top:-180px;right:-120px;"></div>
    <div class="max-w-4xl mx-auto px-6 relative z-10">
      <div class="kick text-[11px] gold font-mono uppercase mb-5">Market Intelligence</div>
      <h1 class="font-serif font-light leading-[1.06] tracking-tight text-4xl sm:text-5xl lg:text-6xl">{L("The <em class='it serif-gold'>developments</em> that shape our region.", "关注与我们相关的<em class='it serif-gold'>区域动态</em>。")}</h1>
      <p class="mt-7 max-w-2xl text-lg text-stone font-light leading-relaxed">{L("Curated developments across Indonesia, AI infrastructure and green steel — the operating environment around our projects.", "精选印度尼西亚、AI 基础设施与绿色钢铁的关键动态——我们项目所处的运营环境。")}</p>
    </div>
  </section>
  <section class="py-20" style="background:#0d1f16;">
    <div class="max-w-4xl mx-auto px-6 space-y-8">
{chr(10).join(cards)}
      <p class="text-center text-[11px] text-stone/50 font-mono pt-4">{L("Updated weekly · indicative summaries, not investment advice.", "每周更新 · 仅为指示性摘要，非投资建议。")}</p>
    </div>
  </section>
</main>
{footer}
{reveal_js}
{dict_js}
{lang_js}
</body>
</html>'''

io.open("news/index.html", "w", encoding="utf-8").write(news_html)

# ---------- homepage teaser: latest 3 ----------
rows = []
for k, it in enumerate(issues[:3]):
    bt = "" if k == 0 else "border-top:1px solid rgba(255,255,255,.06);"
    rows.append(
f'''      <a href="/news/#{it["id"]}" class="flex items-center justify-between gap-5 px-6 py-5 transition group hover:bg-white/[0.02]" style="{bt}">
        <span class="font-serif text-[17px] sm:text-[18px] leading-snug pr-4">{L(html.escape(it["title_en"]), html.escape(it["title_zh"]))}</span>
        <span class="shrink-0 flex items-center gap-3 num text-[12px] text-stone">{L(it["date_en"], it["date_zh"])}<span class="gold transition group-hover:translate-x-1">&rarr;</span></span>
      </a>''')
block = "<!--INTEL_LATEST_START-->\n" + "\n".join(rows) + "\n<!--INTEL_LATEST_END-->"
src2 = re.sub(r"<!--INTEL_LATEST_START-->.*?<!--INTEL_LATEST_END-->", lambda m: block, src, flags=re.S)
io.open("index.html", "w", encoding="utf-8").write(src2)

print("news/index.html bytes:", len(news_html))
print("teaser rows:", len(rows))
