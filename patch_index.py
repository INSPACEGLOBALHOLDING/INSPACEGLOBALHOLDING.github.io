# -*- coding: utf-8 -*-
import io, sys
p = "index.html"
s = io.open(p, encoding="utf-8").read()
orig = s

# 1) nav: add Intelligence link before Contact
nav_old = '      <a href="#contact"    class="nav-link transition" data-i18n="nav.contact">Contact</a>'
nav_new = '      <a href="/news/"      class="nav-link transition" data-i18n="nav.intel">Intelligence</a>\n' + nav_old
assert nav_old in s, "nav anchor missing"
s = s.replace(nav_old, nav_new, 1)

# 2) renumber contact kicker (EN inline + zh dict)
assert "05 — Engage With Inspace Global" in s
s = s.replace("05 — Engage With Inspace Global", "06 — Engage With Inspace Global", 1)
s = s.replace("'contact.kicker': '05 — 业务联络',", "'contact.kicker': '06 — 业务联络',", 1)

# 3) add lang-span CSS before </style>
css = """  .lang-zh{display:none;}
  body[data-lang="zh"] .lang-en{display:none;}
  body[data-lang="zh"] .lang-zh{display:revert;}
</style>"""
assert s.count("</style>") >= 1
s = s.replace("</style>", css, 1)

# 4) insert intelligence teaser section before CONTACT
teaser = '''<!-- ===== INTELLIGENCE ===== -->
<section id="intelligence" class="relative py-24" style="background:#0d1f16;border-top:1px solid rgba(255,255,255,.05);">
  <div class="max-w-6xl mx-auto px-6">
    <div class="reveal flex items-end justify-between flex-wrap gap-6 mb-9">
      <div>
        <div class="kick text-[11px] gold font-mono uppercase mb-5" data-i18n="intel.kicker">05 — Market Intelligence</div>
        <h2 class="font-serif font-light text-4xl sm:text-5xl leading-tight" data-i18n="intel.heading">The <em class="it serif-gold">developments</em> that shape our region.</h2>
      </div>
      <a href="/news/" class="cta-pill" data-i18n="intel.viewall">View all intelligence</a>
    </div>
    <div class="reveal panel rounded-md overflow-hidden">
<!--INTEL_LATEST_START-->
<!--INTEL_LATEST_END-->
    </div>
  </div>
</section>

<!-- ===== CONTACT ===== -->'''
assert "<!-- ===== CONTACT ===== -->" in s
s = s.replace("<!-- ===== CONTACT ===== -->", teaser, 1)

# 5) add zh i18n keys (anchor on first zh key)
anchor = "    'lightbox.hint': '点击任意位置或按 ESC 关闭',"
assert anchor in s
addkeys = anchor + """
    'nav.intel': '市场情报',
    'intel.kicker': '05 — 市场情报',
    'intel.heading': '关注与我们相关的<em class=\\"it serif-gold\\">区域动态</em>。',
    'intel.viewall': '查看全部情报',"""
s = s.replace(anchor, addkeys, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("patched index.html OK; delta bytes:", len(s)-len(orig))
