#!/usr/bin/env python3
"""Membangun halaman statis situs ARSH & Partners Law Office (ID dan EN).

Jalankan: python3 build.py
Halaman Inggris ditulis di root (halaman utama), halaman Indonesia di id/.
Teks bertanda .todo masih menunggu isi dari advokat.
"""
import html
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent / "public"
SITE = "https://www.arshlaw.id"
FIRM = "ARSH &amp; Partners Law Office"
EMAIL = "info@arshlaw.id"
WA_NUMBER = "6281973140134"
WA_DISPLAY = "+62 819 7314 0134"
MAPS = "https://maps.google.com/?q=Plaza+Indonesia,+Jl.+M.H.+Thamrin+Kav.+28-30,+Jakarta"
MAP_EMBED = "https://www.google.com/maps?q=Plaza+Indonesia+Jakarta&output=embed"

WA_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 '
           '11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91 '
           '0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.23 8.23 0 0 1-4.2-1.15l-.3-.18-3.12.82'
           '.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 '
           '2.41 5.83c0 4.54-3.7 8.23-8.23 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64'
           '.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.5'
           '.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56'
           '-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59'
           '.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47'
           '-.28Z"/></svg>')


def T(lang, id_text, en_text):
    return id_text if lang == "id" else en_text


# Jam kerja: isi (ID, EN) bila sudah dikonfirmasi; None menyembunyikan baris jam kerja.
HOURS = ("Setiap hari, kecuali Sabat (Jumat 18.00 &ndash; Sabtu 18.00 WIB)",
         "Every day except the Sabbath (Friday 18:00 &ndash; Saturday 18:00 WIB)")


def hours(lang):
    return T(lang, *HOURS) if HOURS else ""


def todo(text):
    return f'<span class="todo">[ISI DARI ADVOKAT: {text}]</span>'


def wa(lang):
    msg = T(lang, "Halo ARSH & Partners Law Office, saya ingin berkonsultasi mengenai ",
            "Hello ARSH & Partners Law Office, I would like to consult about ")
    return f"https://wa.me/{WA_NUMBER}?text={quote(msg)}"


def address(lang):
    return T(lang,
             "Plaza Indonesia Lt. 5, Unit E021AB<br>Jl. M.H. Thamrin Kav. 28–30<br>Jakarta Pusat 10350",
             "Plaza Indonesia, Level 5, Unit E021AB<br>Jl. M.H. Thamrin Kav. 28–30<br>Central Jakarta 10350, Indonesia")


NAV = [
    ("index.html", "Beranda", "Home"),
    ("layanan.html", "Layanan", "Services"),
    ("tentang.html", "Tentang Kami", "About"),
    ("kontak.html", "Kontak", "Contact"),
    ("tulisan/", "Tulisan", None),  # tulisan hanya berbahasa Indonesia: tidak tampil di menu EN
]

# Bidang praktik: (anchor, judul ID, judul EN, ringkas ID, ringkas EN)
PRACTICE = [
    ("usaha", "Pendampingan Hukum Usaha", "Business Legal Retainer",
     "Pengacara langganan untuk usaha yang belum memiliki bagian hukum sendiri.",
     "A retained lawyer for businesses without their own legal department."),
    ("pribadi", "Pengacara Pribadi", "Personal Lawyer",
     "Pemeriksaan dokumen dan perjanjian sebelum Anda menandatanganinya.",
     "Review of documents and agreements before you sign them."),
    ("litigasi", "Litigasi Perdata dan Pidana", "Civil and Criminal Litigation",
     "Pendampingan perkara di pengadilan, termasuk somasi sebelum gugatan.",
     "Representation in court, including demand letters before a claim."),
    ("ketenagakerjaan", "Ketenagakerjaan dan Hubungan Industrial", "Employment and Industrial Relations",
     "Perjanjian kerja, peraturan perusahaan, PHK, dan perselisihan di PHI.",
     "Employment agreements, company regulations, terminations, and labour court disputes."),
    ("pkpu", "PKPU dan Kepailitan", "Suspension of Payments and Bankruptcy",
     "Pendampingan kreditur maupun debitur dalam proses PKPU dan kepailitan.",
     "Acting for creditors and debtors in PKPU and bankruptcy proceedings."),
    ("hki", "Hak Cipta dan Merek", "Copyright and Trademarks",
     "Pendaftaran serta penegakan hak cipta dan merek.",
     "Registration and enforcement of copyright and trademarks."),
    ("sdm", "Konsultasi dan Pelatihan SDM", "HR Consulting and Training",
     "Pelatihan HRD dan HRM, konseling karyawan, dan program khusus perusahaan.",
     "HRD and HRM training, employee counselling, and tailored company programmes."),
]


# Bidang praktik ditulis sebagai hasil bagi klien: (anchor, awal ID, penekanan ID, awal EN, penekanan EN)
OUTCOMES = [
    ("usaha", "Perjanjian usaha,", "diperiksa sebelum ditandatangani.", "Business agreements,", "reviewed before you sign."),
    ("pribadi", "Dokumen pribadi,", "dibaca dengan teliti.", "Personal documents,", "read with care."),
    ("ketenagakerjaan", "Urusan karyawan,", "ditangani sesuai aturan.", "Employee matters,", "handled by the rules."),
    ("litigasi", "Sengketa di pengadilan,", "didampingi sampai tuntas.", "Disputes in court,", "seen through to the end."),
    ("pkpu", "Utang-piutang dan PKPU,", "diurus dengan tertib.", "Debts and PKPU,", "managed in good order."),
    ("hki", "Merek dan karya Anda,", "didaftarkan dan dijaga.", "Your brand and work,", "registered and protected."),
    ("sdm", "Tim dan organisasi,", "dikembangkan bersama.", "Your team and organisation,", "developed together."),
]


SHARE = {
    "wedding/special-project/index.html": {
        "image": "/wedding/special-project-share.jpg",
        "title_id": "Apabila berkenan, bolehkah kami minta tolong?",
        "title_en": "If you don&rsquo;t mind, may we ask a favour?",
        "desc_id": "Adriel &amp; Anasthasia &middot; Minggu, 18 Oktober 2026",
        "desc_en": "Adriel &amp; Anasthasia &middot; Sunday, 18 October 2026",
        "site_name": "Adriel &amp; Anasthasia",
    },
}


def page(lang, slug, title, description, body):
    # slug boleh berada di subfolder (mis. "wedding/index.html"); up = jalan kembali ke akar bahasa
    up = "../" * slug.count("/")
    depth = ("../" if lang == "id" else "") + up
    prefix = "id/" if lang == "id" else ""
    path = slug[:-len("index.html")] if slug.endswith("index.html") else slug
    other_href = (up + "id/" + slug) if lang == "en" else (up + "../" + slug)
    # Tulisan hanya berbahasa Indonesia: tanpa pasangan EN, tombol EN menuju beranda Inggris
    id_only = slug.startswith("tulisan/")
    if id_only:
        other_href = up + "../index.html"
    noindex = '<meta name="robots" content="noindex">\n' if slug.startswith("wedding/") else ""
    # Halaman pernikahan memakai tema sendiri (palet dan huruf buku acara), bukan tema kantor hukum
    wedding_theme = slug.startswith("wedding/")
    body_class = ' class="theme-wedding"' if wedding_theme else ""
    theme_color = "#7E2327" if wedding_theme else "#0B0B0B"
    wedding_fonts = ('<link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">\n'
                     if wedding_theme or id_only else "")
    nav_items = [(h, i, e) for h, i, e in NAV if e or lang == "id"]
    nav = "\n      ".join(
        f'<a href="{up}{h}"{" aria-current=\"page\"" if h == slug or (h.endswith("/") and slug.startswith(h)) else ""}>{T(lang, i, e)}</a>'
        for h, i, e in nav_items)
    lang_top = (f'<span class="on">ID</span> / <a href="{other_href}" hreflang="en">EN</a>' if lang == "id"
                else f'<a href="{other_href}" hreflang="id">ID</a> / <span class="on">EN</span>')
    lang_nav = (f'<a class="nav-lang" href="{other_href}" hreflang="en">English</a>' if lang == "id"
                else f'<a class="nav-lang" href="{other_href}" hreflang="id">Bahasa Indonesia</a>')
    full_title = title if slug == "index.html" else f"{title} | ARSH &amp; Partners Law Office"
    # Pratinjau link (WhatsApp dll.): default logo kantor; halaman tertentu punya gambar, judul, dan deskripsi sendiri
    post = POSTS_BY_SLUG.get(slug)
    og = SHARE.get(slug) or (post and {"image": post["image"], "title_id": post["title_text"], "title_en": post["title_text"],
                                       "desc_id": post["description"], "desc_en": post["description"],
                                       "site_name": "ARSH &amp; Partners Law Office"})
    og_title = T(lang, og["title_id"], og["title_en"]) if og else full_title
    og_desc = T(lang, og["desc_id"], og["desc_en"]) if og else description
    og_image = (f'<meta property="og:image" content="{SITE}{og["image"]}">\n<meta property="og:image:width" content="1200">\n'
                f'<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">'
                if og else f'<meta property="og:image" content="{SITE}/assets/logo-arsh.png">')
    foot_nav = "".join(f'<li><a href="{up}{h}">{T(lang, i, e)}</a></li>' for h, i, e in nav_items)
    foot_practice = "".join(
        f'<li><a href="{up}layanan.html#{a}">{T(lang, ti, te)}</a></li>' for a, ti, te, *_ in PRACTICE[:5])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add("js")</script>
<title>{full_title}</title>
<meta name="description" content="{description}">
{noindex}<link rel="canonical" href="{SITE}/{prefix}{path}">
{"" if id_only else f'''<link rel="alternate" hreflang="id" href="{SITE}/id/{path}">
<link rel="alternate" hreflang="en" href="{SITE}/{path}">
<link rel="alternate" hreflang="x-default" href="{SITE}/{path}">'''}
<meta property="og:site_name" content="{og["site_name"] if og else "ARSH &amp; Partners Law Office"}">
<meta property="og:type" content="{"article" if post else "website"}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{SITE}/{prefix}{path}">
<meta property="og:locale" content="{T(lang, 'id_ID', 'en_US')}">
<meta name="theme-color" content="{theme_color}">
<link rel="icon" href="{depth}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{depth}assets/apple-touch-icon.png">
{og_image}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Libre+Caslon+Text&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
{wedding_fonts}<link rel="stylesheet" href="{depth}assets/style.css">
{article_ld(post) if post else ""}<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LegalService","name":"ARSH & Partners Law Office","url":"{SITE}/","email":"{EMAIL}","telephone":"+{WA_NUMBER}","address":{{"@type":"PostalAddress","streetAddress":"Plaza Indonesia L5 Unit E021AB, Jl. M.H. Thamrin Kav. 28-30","addressLocality":"Jakarta","postalCode":"10350","addressCountry":"ID"}}}}
</script>
</head>
<body{body_class}>
<a class="skip" href="#main">{T(lang, 'Langsung ke isi', 'Skip to content')}</a>
<div class="topbar">
  <div class="wrap">
    <span class="addr">Plaza Indonesia, Jl. M.H. Thamrin, Jakarta</span>
    <a href="{wa(lang)}">{WA_DISPLAY}</a>
    <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>
    <span class="lang">{lang_top}</span>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{up}index.html"><img src="{depth}assets/logo-arsh-light.png" width="320" height="71" alt="ARSH &amp; Partners Law Office"></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="{T(lang, 'Navigasi utama', 'Main navigation')}">
      {nav}
      {lang_nav}
    </nav>
    <a class="btn btn-dark btn-small header-cta" href="{wa(lang)}">{T(lang, 'Hubungi kami', 'Contact us')}</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div class="brand">
        <a href="{up}index.html"><img src="{depth}assets/logo-arsh-stacked-light.png" width="240" height="152" alt="ARSH &amp; Partners Law Office"></a>
        <p>{address(lang)}</p>
        <p><a href="{MAPS}" rel="noopener">{T(lang, 'Petunjuk arah', 'Get directions')} &rarr;</a></p>
      </div>
      <div><h2>{T(lang, 'Halaman', 'Pages')}</h2><ul>{foot_nav}</ul></div>
      <div><h2>{T(lang, 'Layanan', 'Services')}</h2><ul>{foot_practice}</ul></div>
      <div><h2>{T(lang, 'Kontak', 'Contact')}</h2><ul>
        <li>WhatsApp <a href="{wa(lang)}">{WA_DISPLAY}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        {f"<li>{T(lang, 'Jam kerja', 'Office hours')}: {hours(lang)}</li>" if HOURS else ""}
      </ul></div>
    </div>
    <div class="legal">
      <span>&copy; 2026 {FIRM}</span>
      <span>{T(lang, 'Isi situs ini merupakan informasi umum, bukan nasihat hukum atas perkara tertentu.', 'The content of this site is general information, not legal advice on any specific matter.')}</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa(lang)}" aria-label="WhatsApp">{WA_ICON}</a>
<script>
document.querySelector('.menu-toggle').addEventListener('click', function () {{
  var nav = document.getElementById('nav'), open = nav.classList.toggle('open');
  this.setAttribute('aria-expanded', open);
}});
(function () {{
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
    els.forEach(function (el) {{ el.classList.add('in'); }}); return;
  }}
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
  }}, {{ rootMargin: '0px 0px -10% 0px' }});
  els.forEach(function (el) {{ io.observe(el); }});
}})();
</script>
</body>
</html>
"""


def practice_list(lang, linked=True):
    names = {p[0]: (p[1], p[2], p[3], p[4]) for p in PRACTICE}
    rows = []
    for a, i1, i2, e1, e2 in OUTCOMES:
        ti, te, di, de = names[a]
        rows.append(f"""<a class="outcome reveal" href="layanan.html#{a}">
        <div class="outcome-head"><h3>{T(lang, ti, te)}</h3><p class="outcome-tag">{T(lang, i1, e1)} {T(lang, i2, e2)}</p></div>
        <div class="outcome-body"><p>{T(lang, di, de)}</p></div>
      </a>""")
    return '<div class="outcomes">' + "".join(rows) + "</div>"


def marquee(lang):
    p1 = T(lang, 'Menjaga Kepentingan', 'Protecting Interests')
    p2 = T(lang, 'Memperjuangkan Hak', 'Fighting for Rights')
    item = f'<span>{p1}</span><i aria-hidden="true"></i><span>{p2}</span><i aria-hidden="true"></i>'
    return f"""<section class="marquee" aria-label="{p1}. {p2}.">
  <div class="marquee-track" aria-hidden="true">{item * 6}</div>
</section>"""


def asset(lang, name):
    return ("../" if lang == "id" else "") + "assets/" + name


TEAM = [
    ("Adriel Reyimer Samuel Hutagalung, S.H., M.H., C.C.D", "adriel.webp",
     "Managing Partner / Advokat", "Managing Partner / Lawyer",
     "Lulusan Sarjana Hukum Universitas Katolik Parahyangan dan Magister Hukum Bisnis Universitas Pelita Harapan. Berpengalaman menangani perselisihan ketenagakerjaan, hukum bisnis komersial, dan hukum perbankan.",
     "Bachelor of Law from Parahyangan Catholic University and Master of Business Law from Pelita Harapan University. Experienced in employment disputes, commercial business law, and banking law."),
    ("Henrietta Sarah Mega, S.H.", "sarah.webp",
     "Corporate Partner", "Corporate Partner",
     "Lulusan Sarjana Hukum Universitas Indonesia dengan kekhususan hukum korporasi. Berpengalaman di hukum ketenagakerjaan dan penanaman modal, termasuk transaksi merger dan akuisisi, pembiayaan kembali, dan hak tanggungan.",
     "Bachelor of Law from the University of Indonesia, specialising in corporate law. Experienced in employment and investment law, including mergers and acquisitions, refinancing, and mortgages."),
    ("Denny Rizky Setiawan, S.H.", None,
     "Advokat", "Lawyer",
     "Lulusan Sarjana Hukum Universitas Katolik Parahyangan. Berpengalaman mendampingi dan mewakili klien dalam berbagai sengketa di pengadilan Indonesia, serta menjadi bagian tim pengurus dan kurator dalam perkara kepailitan dan PKPU.",
     "Bachelor of Law from Parahyangan Catholic University. Experienced in representing clients in disputes before Indonesian courts, and in serving on administrator and curator teams in bankruptcy and PKPU cases."),
]


def team(lang, heading_level="h3"):
    cards = []
    for name, photo, role_id, role_en, bio_id, bio_en in TEAM:
        if photo:
            pic = f'<div class="photo has-img"><img src="{asset(lang, photo)}" alt="{name.split(",")[0]}" width="600" height="800" loading="lazy"></div>'
        else:
            pic = '<div class="photo" aria-hidden="true"></div>'
        cards.append(f"""<article class="member reveal">
        {pic}
        <{heading_level}>{name}</{heading_level}>
        <p class="role">{T(lang, role_id, role_en)}</p>
        <p>{T(lang, bio_id, bio_en)}</p>
      </article>""")
    return '<div class="team">\n      ' + "\n      ".join(cards) + "\n    </div>"


def closing(lang):
    return f"""<section class="closing">
  <div class="wrap">
    <div>
      <h2>{T(lang, 'Ingin membicarakan persoalan Anda?', 'Would you like to discuss your matter?')}</h2>
      <p>{T(lang, 'Kirim pesan singkat lewat WhatsApp, kami akan menghubungi Anda kembali.', 'Send us a short WhatsApp message and we will get back to you.')}</p>
    </div>
    <a class="btn btn-dark" href="{wa(lang)}">{WA_ICON} WhatsApp {WA_DISPLAY}</a>
  </div>
</section>"""


def home(lang):
    return f"""
<section class="hero">
  <div class="wrap">
    <div class="copy">
      <hr class="gold-rule">
      <h1 class="hero-title"><span class="ln"><span>{T(lang, 'Menjaga Kepentingan.', 'Protecting Interests.')}</span></span> <span class="ln"><em>{T(lang, 'Memperjuangkan Hak.', 'Fighting for Rights.')}</em></span></h1>
      <p class="intro fade-in">{T(lang, 'Kantor hukum di Jakarta untuk pengusaha, perusahaan, dan keluarga. Kami menyusun dan memeriksa perjanjian, menangani urusan ketenagakerjaan, dan mendampingi Anda di pengadilan bila sengketa tidak terhindarkan.', 'A Jakarta law office for business owners, companies, and families. We draft and review agreements, handle employment matters, and represent you in court when a dispute cannot be avoided.')}</p>
      <div class="buttons fade-in">
        <a class="btn btn-gold" href="{wa(lang)}">{WA_ICON} {T(lang, 'Konsultasi lewat WhatsApp', 'Consult via WhatsApp')}</a>
        <a class="btn btn-line-light" href="layanan.html">{T(lang, 'Lihat layanan', 'View services')}</a>
      </div>
    </div>
    <img class="statue" src="{asset(lang, 'dewi.webp')}" width="900" height="998" alt="" fetchpriority="high">
  </div>
</section>

<section class="facts" aria-label="{T(lang, 'Informasi kantor', 'Office information')}">
  <dl class="wrap">
    <div><dt>{T(lang, 'Kantor', 'Office')}</dt><dd><a href="{MAPS}" rel="noopener">Plaza Indonesia Lt. 5, Jakarta</a></dd></div>
    <div><dt>WhatsApp</dt><dd><a href="{wa(lang)}">{WA_DISPLAY}</a></dd></div>
    <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
    {f"<div><dt>{T(lang, 'Jam kerja', 'Hours')}</dt><dd>{hours(lang)}</dd></div>" if HOURS else ""}
  </dl>
</section>

{marquee(lang)}

<section class="block">
  <div class="wrap">
    <header class="section-head section-head-lg reveal">
      <h2>{T(lang, 'Bidang praktik', 'Practice areas')}</h2>
      <span class="line" aria-hidden="true"></span>
      <p>{T(lang, 'Sebagian besar pekerjaan kami bersifat pencegahan: memastikan dokumen benar sebelum ditandatangani.', 'Most of our work is preventive: getting documents right before they are signed.')}</p>
    </header>
    {practice_list(lang)}
    <p class="outcomes-ask reveal">{T(lang, 'Belum yakin persoalan Anda termasuk bidang mana?', 'Not sure where your matter fits?')} <a class="link-arrow" href="{wa(lang)}">{T(lang, 'Tanyakan lewat WhatsApp', 'Ask us on WhatsApp')} &rarr;</a></p>
  </div>
</section>

<section class="quote-band">
  <div class="wrap">
    <img src="{asset(lang, 'mark-gold.png')}" width="600" height="434" alt="">
    <div>
      <p class="quote reveal">{T(lang, '&ldquo;Cegah selagi bisa dicegah, perbaiki segera setelah disadari.&rdquo;', '&ldquo;Prevent when you are able to prevent; fix it as soon as you notice it.&rdquo;')}</p>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <header class="section-head">
      <h2>{T(lang, 'Tim kami', 'Our team')}</h2>
      <span class="line" aria-hidden="true"></span>
    </header>
    {team(lang)}
  </div>
</section>

{closing(lang)}
"""


SERVICE_DETAIL = {
    "usaha": (
        "Seperti dokter keluarga untuk urusan hukum usaha Anda. Layanan ini cocok untuk usaha kecil dan menengah yang belum memiliki bagian hukum, dan ingin persoalan dengan karyawan, pemasok, atau pelanggan ditangani sebelum menjadi sengketa.",
        "Like a family doctor for your business's legal matters. Suited to small and medium businesses without a legal department that want issues with employees, suppliers, or customers handled before they become disputes.",
        ["Menyusun dan memeriksa perjanjian dengan pemasok, vendor, dan mitra", "Perjanjian kerja dan persoalan karyawan", "Pendampingan penagihan piutang", "Konsultasi saat ada keputusan penting"],
        ["Drafting and reviewing agreements with suppliers, vendors, and partners", "Employment agreements and employee matters", "Support with collections", "Consultation on important decisions"]),
    "pribadi": (
        "Untuk perorangan yang mengurus banyak perjanjian dan dokumen, dan ingin memastikan semuanya aman sebelum ditandatangani.",
        "For individuals who handle many agreements and documents and want to be sure they are sound before signing.",
        ["Pemeriksaan dokumen dan perjanjian", "Pendapat hukum atas persoalan pribadi", "Pendampingan saat menghadapi persoalan hukum"],
        ["Document and agreement review", "Legal opinions on personal matters", "Support when facing a legal problem"]),
    "litigasi": (
        "Bila persoalan tidak dapat diselesaikan dengan musyawarah, kami mendampingi Anda di setiap tahap perkara.",
        "When a matter cannot be settled by agreement, we represent you at every stage.",
        ["Wanprestasi dan perbuatan melawan hukum", "Pendampingan pidana sejak pemeriksaan hingga persidangan", "Penyusunan dan penanganan somasi"],
        ["Breach of contract and unlawful acts", "Criminal representation from investigation to trial", "Drafting and responding to demand letters"]),
    "ketenagakerjaan": (
        "Kepatuhan hukum ketenagakerjaan bagi perusahaan, dan pendampingan bila terjadi perselisihan.",
        "Employment law compliance for companies, and representation when disputes arise.",
        ["Perjanjian kerja dan peraturan perusahaan", "Prosedur pemutusan hubungan kerja", "Perselisihan di Pengadilan Hubungan Industrial"],
        ["Employment agreements and company regulations", "Termination procedures", "Disputes before the Industrial Relations Court"]),
    "pkpu": (
        "Pendampingan kreditur maupun debitur dalam proses penundaan kewajiban pembayaran utang dan kepailitan.",
        "Acting for creditors and debtors in suspension of payments and bankruptcy proceedings.",
        [], []),
    "hki": (
        "Pendaftaran serta penegakan hak cipta dan merek, termasuk penanganan pelanggaran.",
        "Registration and enforcement of copyright and trademarks, including infringement matters.",
        [], []),
    "sdm": (
        "Pelatihan dan konsultasi untuk mengembangkan orang di dalam organisasi Anda, sejalan dengan kepatuhan ketenagakerjaan.",
        "Training and consulting to develop the people in your organisation, aligned with employment compliance.",
        ["Pelatihan HRD: kepemimpinan, perencanaan karier, budaya kerja", "Pelatihan HRM: rekrutmen, penilaian kinerja, pengelolaan konflik, kompensasi", "Psikologi dan konseling karyawan", "Keterampilan lunak: komunikasi, manajemen waktu, kecerdasan emosional", "Program khusus: persiapan pensiun, team building, kewirausahaan, pelayanan publik"],
        ["HRD training: leadership, career planning, workplace culture", "HRM training: recruitment, appraisal, conflict management, compensation", "Employee psychology and counselling", "Soft skills: communication, time management, emotional intelligence", "Custom programmes: pre-retirement, team building, entrepreneurship, public service"]),
}


def services(lang):
    blocks = []
    for a, ti, te, *_ in PRACTICE:
        di, de, li, le = SERVICE_DETAIL[a]
        items = li if lang == "id" else le
        ul = ("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>") if items else ""
        blocks.append(f"""<article class="detail" id="{a}">
        <h2>{T(lang, ti, te)}</h2>
        <p style="margin-top:12px">{T(lang, di, de)}</p>
        {ul}
        <a class="link-arrow" href="{wa(lang)}">{T(lang, 'Minta informasi dan penawaran', 'Request information and a quotation')} &rarr;</a>
      </article>""")
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">{T(lang, 'Beranda', 'Home')}</a> / {T(lang, 'Layanan', 'Services')}</p>
    <h1>{T(lang, 'Layanan', 'Services')}</h1>
    <p class="intro">{T(lang, 'Setiap pekerjaan dimulai dengan percakapan singkat untuk memahami persoalan Anda. Setelah itu kami memberikan penawaran tertulis sebelum pekerjaan dimulai.', 'Every engagement begins with a short conversation to understand your matter, followed by a written proposal before work begins.')}</p>
  </div>
</section>
<section class="block">
  <div class="wrap split">
    <header><h2>{T(lang, 'Daftar layanan', 'All services')}</h2>
      <ul class="tags">{''.join(f'<li><a href="#{a}" style="text-decoration:none">{T(lang, ti, te)}</a></li>' for a, ti, te, *_ in PRACTICE)}</ul>
    </header>
    <div>
      {''.join(blocks)}
    </div>
  </div>
</section>
{closing(lang)}
"""


def about(lang):
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">{T(lang, 'Beranda', 'Home')}</a> / {T(lang, 'Tentang Kami', 'About')}</p>
    <h1>{T(lang, 'Tentang Kami', 'About us')}</h1>
    <p class="intro">{T(lang, f'{FIRM} berkantor di Plaza Indonesia, Jakarta. Kami membawa cara pandang yang segar dan pendekatan yang luwes dalam menyelesaikan persoalan hukum klien, dengan biaya yang dijelaskan sejak awal.', f'{FIRM} is based at Plaza Indonesia, Jakarta. We bring a fresh perspective and a flexible approach to our clients&rsquo; legal matters, with fees explained from the start.')}</p>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <header class="section-head">
      <h2>{T(lang, 'Tim kami', 'Our team')}</h2>
      <span class="line" aria-hidden="true"></span>
    </header>
    {team(lang)}
  </div>
</section>
<section class="block block-soft">
  <div class="wrap split">
    <header><h2>{T(lang, 'Cara kami bekerja', 'How we work')}</h2></header>
    <div>
      <p><strong>{T(lang, 'Mencegah lebih dulu.', 'Prevention first.')}</strong> {T(lang, 'Perjanjian yang disusun dengan benar sejak awal menghindarkan banyak sengketa di kemudian hari.', 'An agreement drafted correctly from the start avoids many disputes later.')}</p>
      <p><strong>{T(lang, 'Biaya yang jelas.', 'Clear fees.')}</strong> {T(lang, 'Penawaran tertulis diberikan sebelum pekerjaan dimulai.', 'A written proposal is provided before work begins.')}</p>
      <p><strong>{T(lang, 'Mudah dihubungi.', 'Easy to reach.')}</strong> {T(lang, 'Lewat WhatsApp atau email, dengan kabar perkembangan secara berkala.', 'By WhatsApp or email, with regular updates on progress.')}</p>
    </div>
  </div>
</section>
{closing(lang)}
"""


def insights(lang):
    chapters = [("1", "Tanda Tangan", "Signature"), ("2", "Syarat dan Ketentuan", "Terms and Conditions"),
                ("3", "Ketenagakerjaan I", "Employment I")]
    ch = "".join(
        f'<li><span class="meta">{T(lang, "Bab", "Chapter")} {n}</span><div><h3>{T(lang, i, e)}</h3><p>{todo(T(lang, "tanggal terbit dan berkas PDF", "publication date and PDF"))}</p></div></li>'
        for n, i, e in chapters)
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">{T(lang, 'Beranda', 'Home')}</a> / {T(lang, 'Wawasan', 'Insights')}</p>
    <h1>{T(lang, 'Wawasan', 'Insights')}</h1>
    <p class="intro">{T(lang, 'Tulisan singkat untuk membantu Anda mengenali persoalan hukum sebelum menjadi besar.', 'Short pieces to help you recognise legal problems before they grow.')}</p>
  </div>
</section>
<section class="block">
  <div class="wrap split">
    <header><h2>{T(lang, 'Artikel', 'Articles')}</h2></header>
    <ul class="posts">
      <li id="irony-of-law"><span class="meta">{todo(T(lang, 'tanggal', 'date'))}</span><div><h3>The Irony of Law</h3><p>{T(lang, 'Cegah selagi bisa dicegah, perbaiki segera setelah disadari.', 'Prevent when you are able to prevent; fix it as soon as you notice it.')} {todo(T(lang, 'isi artikel dipindahkan dari situs lama setelah ditinjau', 'article text moved from the old site after review'))}</p></div></li>
    </ul>
  </div>
</section>
<section class="block" id="legal-reminder">
  <div class="wrap split">
    <header><h2>Legal Reminder Series</h2><p>{T(lang, 'Seri pengingat hukum yang dapat diunduh.', 'A downloadable series of legal reminders.')}</p></header>
    <ul class="posts">{ch}</ul>
  </div>
</section>
{closing(lang)}
"""


def contact(lang):
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">{T(lang, 'Beranda', 'Home')}</a> / {T(lang, 'Kontak', 'Contact')}</p>
    <h1>{T(lang, 'Kontak', 'Contact')}</h1>
    <p class="intro">{T(lang, 'Cara tercepat menghubungi kami adalah lewat WhatsApp. Ceritakan persoalan Anda secara singkat, dan kami akan menghubungi Anda kembali.', 'The fastest way to reach us is WhatsApp. Tell us briefly about your matter and we will get back to you.')}</p>
  </div>
</section>
<section class="block">
  <div class="wrap contact">
    <div>
      <dl>
        <dt>WhatsApp</dt><dd><a href="{wa(lang)}">{WA_DISPLAY}</a></dd>
        <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>{T(lang, 'Alamat', 'Address')}</dt><dd>{address(lang)}</dd>
        {f"<dt>{T(lang, 'Jam kerja', 'Office hours')}</dt><dd>{hours(lang)}</dd>" if HOURS else ""}
      </dl>
      <p style="margin-top:32px"><a class="btn btn-gold" href="{wa(lang)}">{WA_ICON} {T(lang, 'Kirim pesan WhatsApp', 'Send a WhatsApp message')}</a></p>
    </div>
    <iframe class="map" src="{MAP_EMBED}" loading="lazy" title="{T(lang, 'Peta lokasi Plaza Indonesia', 'Map of Plaza Indonesia')}" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</section>
"""


WEDDING_PDF = "/wedding/order-of-service.pdf"


def wedding(lang):
    # Halaman pernikahan Adriel & Anasthasia, dibuka lewat QR (arshlaw.id/order-of-service). Tidak ada di menu.
    up = "../"
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="{up}index.html">{T(lang, 'Beranda', 'Home')}</a> / {T(lang, 'Pernikahan', 'Wedding')}</p>
    <h1>Hi there. Our Managing Partner is <em class="wedding-amp">getting married.</em></h1>
    <p class="intro">Adriel Hutagalung and Anasthasia Sabatini will be joined in holy matrimony on Sunday, 18 October 2026, at 08.30 in the Alumni Chapel, Universitas Advent Indonesia. For once, he is signing an agreement with no clauses to negotiate. Thank you for being with them, and for your prayers.</p>
  </div>
</section>
<section class="block">
  <div class="wrap wedding">
    <img class="wedding-photo reveal" src="/wedding/adriel-anasthasia-cover.webp" width="1000" height="1420" alt="Adriel {T(lang, 'dan', 'and')} Anasthasia">
    <div class="wedding-copy reveal">
      <h2>{T(lang, 'Susunan acara', 'Order of service')}</h2>
      <p>{T(lang, 'Seluruh susunan acara pemberkatan, dari prelude sampai ucapan terima kasih, beserta nama para petugas dan lagu yang dinyanyikan.', 'The full programme of the ceremony, from the prelude to the words of thanks, with everyone taking part and the songs that will be sung.')}</p>
      <p class="wedding-file">PDF &middot; 16 {T(lang, 'halaman', 'pages')} A5 &middot; {T(lang, '6,6', '6.6')} MB</p>
      <p><a class="btn btn-gold" href="{WEDDING_PDF}" download="Order of Service - Adriel &amp; Anasthasia.pdf">{T(lang, 'Unduh susunan acara', 'Download the order of service')}</a></p>
    </div>
  </div>
</section>
<section class="block block-soft" id="story-frames">
  <div class="wrap">
    <div class="frames-head reveal">
      <h2>{T(lang, 'Bingkai Instagram Story', 'Instagram Story frames')}</h2>
      <p>{T(lang, 'Adriel dan Anasthasia membuat dua bingkai Instagram Story untuk hari ini, dan mereka ingin sekali melihat foto Anda di dalamnya. Pilih salah satu, simpan ke ponsel, lalu pasang di atas foto Anda.', 'Adriel and Anasthasia made two Instagram Story frames for the day, and they would love to see your photos in them. Pick one, save it to your phone, and lay it over your own photo.')}</p>
    </div>
    <div class="frames">
      {''.join(f"""<figure class="frame reveal">
        <img src="/wedding/story-frame-{n}.png?v=3" width="1080" height="1920" alt="{T(lang, f'Bingkai {n}', f'Frame {n}')}" loading="lazy">
        <figcaption>{T(lang, f'Bingkai {n}, untuk foto {pi}', f'Frame {n}, for {pe} photos')}</figcaption>
        <a class="btn btn-gold btn-small" href="/wedding/story-frame-{n}.png?v=3" download="Adriel &amp; Anasthasia - Story frame {n}.png">{T(lang, f'Unduh bingkai {n}', f'Download frame {n}')}</a>
      </figure>""" for n, pi, pe in ((1, 'tegak', 'portrait'), (2, 'mendatar', 'landscape')))}
    </div>
    <div class="howto">
      <div class="reveal">
        <h3>iPhone</h3>
        <ol>
          <li>{T(lang, 'Buka bingkai yang sudah diunduh, ketuk Share, lalu Copy.', 'Open the frame you downloaded, tap Share, then Copy.')}</li>
          <li>{T(lang, 'Buka Instagram dan buat Story baru dengan foto Anda.', 'In Instagram, start a new Story with your photo.')}</li>
          <li>{T(lang, 'Ketuk di mana saja pada layar, lalu pilih Paste.', 'Tap anywhere on the screen and choose Paste.')}</li>
          <li>{T(lang, 'Cubit dan lebarkan bingkai sampai memenuhi layar.', 'Pinch the frame until it fills the screen.')}</li>
          <li>{T(lang, 'Bagikan ke Story Anda.', 'Share it to your Story.')}</li>
        </ol>
      </div>
      <div class="reveal">
        <h3>Android</h3>
        <ol>
          <li>{T(lang, 'Buka bingkai di Galeri, ketuk Share, lalu Copy.', 'Open the frame in your Gallery, tap Share, then Copy.')}</li>
          <li>{T(lang, 'Buka Instagram dan buat Story baru dengan foto Anda.', 'In Instagram, start a new Story with your photo.')}</li>
          <li>{T(lang, 'Ketuk layar sampai keyboard muncul, lalu ketuk bingkai di saran clipboard.', 'Tap the screen to bring up the keyboard, then tap the frame in the clipboard suggestion.')}</li>
          <li>{T(lang, 'Cubit dan lebarkan bingkai sampai memenuhi layar.', 'Pinch the frame until it fills the screen.')}</li>
          <li>{T(lang, 'Bagikan ke Story Anda.', 'Share it to your Story.')}</li>
        </ol>
      </div>
    </div>
    <div class="frames-notes reveal">
      <p>{T(lang, 'Tidak ada pilihan Copy? Di Story Anda, ketuk ikon stiker, pilih Cutouts, lalu pilih file bingkainya.', 'No Copy option? In your Story, tap the sticker icon, choose Cutouts, and pick the frame file instead.')}</p>
      <p>{T(lang, 'Kalau ada stiker &ldquo;Add Yours&rdquo; di Story mereka, ketuk stiker itu supaya semua foto terkumpul di satu tempat.', 'If you see an &ldquo;Add Yours&rdquo; sticker on their Story, tap it so every photo ends up in one place.')}</p>
    </div>
  </div>
</section>
"""


MOREMENTS_URL = "https://morements.cloud/e/xk97vqiv73"


def wedding_photos(lang):
    # Kamera bersama Morements untuk tamu. Link dibagikan diam-diam lewat pesan (bukan QR), tidak ada di menu.
    up = "../../"
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="{up}index.html">{T(lang, 'Beranda', 'Home')}</a> / <a href="../">{T(lang, 'Pernikahan', 'Wedding')}</a> / Special project</p>
    <h1>{T(lang, 'Apabila berkenan, bolehkah kami <em class="wedding-amp">minta tolong?</em>', 'If you don&rsquo;t mind, may we <em class="wedding-amp">ask a favour?</em>')}</h1>
    <p class="intro">{T(lang, 'Di hari pernikahan kami, Minggu, 18 Oktober 2026, kami ingin kamu menjadi salah satu fotografernya. Kamu tidak perlu membawa kamera apa pun. Kami menyiapkan kamera sekali pakai virtual yang terbuka langsung di ponselmu, dengan jumlah jepretan terbatas seperti kamera film zaman dulu. Dari pemberkatan di chapel pagi hari sampai resepsi siang harinya, setiap foto yang kamu ambil akan masuk ke satu album bersama: <em>The One on the Eighteenth of October 2026.</em>', 'On our wedding day, Sunday, 18 October 2026, we would love for you to be one of our photographers. There is nothing to bring. We have set up a virtual disposable camera that opens right on your phone, with a limited number of shots, just like the film cameras of old. From the chapel in the morning to the reception in the afternoon, every photo you take goes into one shared album: <em>The One on the Eighteenth of October 2026.</em>')}</p>
  </div>
</section>
<section class="block">
  <div class="wrap wedding">
    <img class="wedding-photo reveal" src="/wedding/adriel-anasthasia-cover-sp.webp" width="1000" height="1420" alt="Adriel {T(lang, 'dan', 'and')} Anasthasia">
    <div class="wedding-copy photos-story reveal">
    <h2>{T(lang, 'Hanya ada 200 kamera', 'There are only 200 cameras')}</h2>
    <p>{T(lang, 'Untuk hari itu, kami hanya punya 200 kamera sekali pakai virtual, masing-masing berisi 25 foto. Setiap foto hanya bisa diambil sekali dan tidak bisa diulang atau diganti kalau ada yang salah. Karena jumlah kameranya terbatas, proyek ini sengaja tidak kami umumkan ke semua orang. Kalau link ini sampai kepadamu, berarti kamu termasuk orang yang kami harapkan ikut berkontribusi.', 'We only have 200 virtual disposable cameras for the day, each holding 25 shots. Every shot can be taken only once, and it cannot be retaken or replaced if something goes wrong. Because the cameras are limited, we are keeping this project a little quiet. If this link has reached you, you are one of the people we hoped would take part.')}</p>
    <p>{T(lang, 'Link ini tidak akan dipasang di QR dan tidak akan diumumkan di mana pun. <em class="photos-em">Link ini beredar diam-diam, dari pesan ke pesan. Kalau ada orang yang kamu percaya bisa ikut membantu,</em> <em class="photos-em photos-underline">silakan teruskan kepada mereka.</em> Kami sangat menghargai kalau link ini tetap beredar dengan cara itu.', 'This link will not appear on any QR code, and it will not be announced. <em class="photos-em">It travels quietly, from one message to the next. If there is someone you trust to help,</em> <em class="photos-em photos-underline">feel free to pass it on to them.</em> We would be grateful if it keeps travelling that way.')}</p>
    <p class="photos-em photos-underline">{T(lang, 'Kalau link ini sampai kepadamu dan kamu berkenan ikut terlibat, tolong simpan link ini baik-baik dan ingat untuk membukanya lagi di hari pernikahan kami, Minggu, 18 Oktober 2026.', 'If this link has reached you and you would like to take part, please save it and remember to open it again on our wedding day, Sunday, 18 October 2026.')}</p>
    <p>{T(lang, 'Sekali lagi, kami berdua berterima kasih banyak atas bantuanmu di proyek spesial ini.', 'Once again, thank you so much from both of us for your help with this special project.')}</p>
    <p class="photos-sign">Adriel &amp; Anasthasia</p>
    </div>
  </div>
</section>
<section class="block block-soft">
  <div class="wrap photos">
    <div class="photos-copy reveal">
      <h2>{T(lang, 'Buka kameranya', 'Open the camera')}</h2>
      <p>{T(lang, 'Di hari pernikahan, buka kameranya dari ponselmu. Pilih momennya baik-baik dan pastikan setiap foto adalah yang terbaik menurutmu. Kalau kamu membuka halaman ini di ponsel, cukup ketuk tombolnya. Kalau dari komputer, pindai kode ini dengan kamera ponselmu.', 'On the day, open the camera on your phone. Choose your moments well and make every photo one you are proud of. If you are reading this on your phone, just tap the button. If you are on a computer, scan the code with your phone camera.')}</p>
      <p><a class="btn btn-gold" href="{MOREMENTS_URL}" rel="noopener">{T(lang, 'Buka kamera', 'Open the camera')}</a></p>
    </div>
    <img class="photos-qr reveal" src="/wedding/morements-qr.svg" width="330" height="330" alt="{T(lang, 'Kode QR kamera Morements', 'QR code for the Morements camera')}">
  </div>
</section>
"""


# ---------- Tulisan (14 Okt 2026): esai Adriel, hanya berbahasa Indonesia, di /id/tulisan/ ----------
# Naskah ada di tulisan/<slug>.md: paragraf dipisah baris kosong, "## " = subjudul, "> " = kutipan, _miring_.
# Situs adalah sumber utama (canonical); versi Medium diimpor lewat "Import a story" agar canonical menunjuk ke sini.
POSTS = [
    {"slug": "kembali-sebentar-ke-1945",
     "title": "Kembali Sebentar ke <em>1945</em>",
     "title_text": "Kembali Sebentar ke 1945",
     "description": "Mengapa Republik yang baru merdeka tetap memakai hukum peninggalan kolonial, dan apakah pilihan itu ikut membentuk cara kita memandang pemerintah hari ini.",
     # Kalimat pembuka (hook) di atas tulisan, dikutip dari isi tulisan
     "hook": "Bisa jadi pemerintah Republik dipandang sebagai pihak yang patut dan selalu dihormati karena sejak awal kehadirannya dianggap sebagai penolong (atau apabila saya boleh menggunakan istilah yang sedikit lebih ekstrem, sebagai seorang &lsquo;pahlawan&rsquo;) dalam menyelesaikan berbagai permasalahan penduduk Republik; sehingga semakin menjauhkan cara pandang terhadap pemerintah sebagai &lsquo;pelayan&rsquo; masyarakat.",
     "date": "2026-10-14",
     "image": "/assets/tulisan/kembali-sebentar-ke-1945.jpg",
     "medium": "https://aderiyel.medium.com/kembali-sebentar-ke-1945-698834e853f7"},
]
POSTS_BY_SLUG = {f"tulisan/{p['slug']}/index.html": p for p in POSTS}
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
AUTHOR_BIO = ("Adriel Hutagalung adalah Managing Partner ARSH &amp; Partners Law Office. "
              "Ia menulis tentang sejarah dan hukum Indonesia untuk memahami keadaan hari ini.")


def tanggal(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {BULAN[int(m) - 1]} {y}"


def post_source(post):
    return (Path(__file__).parent / "tulisan" / f"{post['slug']}.md").read_text(encoding="utf-8")


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r'"([^"]+)"', r"&ldquo;\1&rdquo;", text)
    return re.sub(r"\b_([^_]+)_\b", r"<em>\1</em>", text)


def render_post(src):
    out = []
    for block in src.strip().split("\n\n"):
        block = block.strip()
        if block.startswith("## "):
            out.append(f"<h2>{inline(block[3:])}</h2>")
        elif block.startswith("> "):
            out.append(f"<blockquote><p>{inline(block[2:])}</p></blockquote>")
        else:
            out.append(f"<p>{inline(block)}</p>")
    return "\n      ".join(out)


def reading_minutes(src):
    return max(1, round(len(src.split()) / 200))


def article_ld(post):
    url = f"{SITE}/id/tulisan/{post['slug']}/"
    return ('<script type="application/ld+json">\n'
            f'{{"@context":"https://schema.org","@type":"Article","headline":"{post["title_text"]}","description":"{post["description"]}",'
            f'"image":"{SITE}{post["image"]}","datePublished":"{post["date"]}","inLanguage":"id","mainEntityOfPage":"{url}",'
            f'"author":{{"@type":"Person","name":"Adriel Hutagalung","url":"{SITE}/id/tentang.html"}},'
            f'"publisher":{{"@type":"Organization","name":"ARSH & Partners Law Office","logo":{{"@type":"ImageObject","url":"{SITE}/assets/logo-arsh.png"}}}}}}\n'
            '</script>\n')


def post_page(post):
    def build(lang):
        src = post_source(post)
        url = f"{SITE}/id/tulisan/{post['slug']}/"
        share_text = quote(f"{post['title_text']} — {url}")
        medium = (f'<p class="essay-medium">Tulisan ini juga terbit di <a href="{post["medium"]}" rel="noopener">Medium</a>.</p>'
                  if post["medium"] else "")
        return f"""
<section class="page-hero essay-hero">
  <div class="wrap">
    <p class="crumbs"><a href="../../index.html">Beranda</a> / <a href="../">Tulisan</a></p>
    <h1>{post['title']}</h1>
    <p class="essay-meta">Adriel Hutagalung <i aria-hidden="true"></i> <time datetime="{post['date']}">{tanggal(post['date'])}</time> <i aria-hidden="true"></i> {reading_minutes(src)} menit baca</p>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <article class="essay">
      {f'<p class="essay-hook">&ldquo;{post["hook"]}&rdquo;</p>' if post.get("hook") else ""}
      {render_post(src)}
    </article>
    <aside class="essay-end">
      <p class="essay-author">{AUTHOR_BIO} <a class="link-arrow" href="../../tentang.html">Tentang kami &rarr;</a></p>
      {medium}
      <p class="essay-share">Bagikan:
        <a href="https://wa.me/?text={share_text}" rel="noopener">WhatsApp</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(url, safe='')}" rel="noopener">LinkedIn</a>
        <button type="button" class="copy-link" data-url="{url}">Salin tautan</button>
      </p>
    </aside>
  </div>
</section>
<script>
document.querySelector('.copy-link').addEventListener('click', function () {{
  var b = this;
  navigator.clipboard.writeText(b.dataset.url).then(function () {{ b.textContent = 'Tautan tersalin'; }});
}});
</script>
"""
    return build


def posts_index(lang):
    items = "".join(f"""<li class="reveal">
        <a href="{p['slug']}/">
          <span class="meta"><time datetime="{p['date']}">{tanggal(p['date'])}</time></span>
          <h2>{p['title']}</h2>
          <p>{p['description']}</p>
          <span class="link-arrow">Baca tulisan &rarr;</span>
        </a>
      </li>""" for p in sorted(POSTS, key=lambda p: p["date"], reverse=True))
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="../index.html">Beranda</a> / Tulisan</p>
    <h1>Tulisan</h1>
    <p class="intro">Menengok kembali masa lalu, untuk memahami hari ini.</p>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <ul class="essay-list">
      {items}
    </ul>
  </div>
</section>
"""


PAGES = {
    "index.html": (home,
                   ("ARSH &amp; Partners Law Office | Menjaga Kepentingan. Memperjuangkan Hak.",
                    "Kantor hukum di Plaza Indonesia, Jakarta, untuk pengusaha, perusahaan, dan keluarga: perjanjian, ketenagakerjaan, litigasi, dan kepailitan."),
                   ("ARSH &amp; Partners Law Office | Protecting Interests. Fighting for Rights.",
                    "A law office at Plaza Indonesia, Jakarta, for business owners, companies, and families: agreements, employment, litigation, and insolvency.")),
    "layanan.html": (services,
                     ("Layanan", "Pendampingan hukum usaha, pengacara pribadi, litigasi, ketenagakerjaan, PKPU dan kepailitan, hak cipta dan merek, serta konsultasi SDM."),
                     ("Services", "Business legal retainer, personal lawyer, litigation, employment, insolvency, copyright and trademarks, and HR consulting.")),
    "tentang.html": (about,
                     ("Tentang Kami", "Tentang ARSH &amp; Partners Law Office dan advokatnya."),
                     ("About", "About ARSH &amp; Partners Law Office and its lawyers.")),
    "kontak.html": (contact,
                    ("Kontak", "Hubungi ARSH &amp; Partners Law Office lewat WhatsApp atau email, atau kunjungi kantor kami di Plaza Indonesia, Jakarta."),
                    ("Contact", "Contact ARSH &amp; Partners Law Office by WhatsApp or email, or visit our office at Plaza Indonesia, Jakarta.")),
    "wedding/index.html": (wedding,
                           ("Adriel &amp; Anasthasia", "Susunan acara pemberkatan nikah Adriel dan Anasthasia, 18 Oktober 2026."),
                           ("Adriel &amp; Anasthasia", "Order of service for the holy matrimony of Adriel and Anasthasia, 18 October 2026.")),
    "wedding/special-project/index.html": (wedding_photos,
                                  ("Special project | Adriel &amp; Anasthasia", "Kamera bersama untuk tamu pernikahan Adriel dan Anasthasia, 18 Oktober 2026."),
                                  ("Special project | Adriel &amp; Anasthasia", "A shared camera for the guests of Adriel and Anasthasia, 18 October 2026.")),
    "tulisan/index.html": (posts_index,
                           ("Tulisan", "Menengok kembali masa lalu, untuk memahami hari ini."), None),
}
for _p in POSTS:
    PAGES[f"tulisan/{_p['slug']}/index.html"] = (post_page(_p), (_p["title_text"], _p["description"]), None)


def sitemap():
    # Halaman yang boleh diindeks; halaman pernikahan (noindex) tidak dimasukkan
    urls = []
    for slug, (_, _, meta_en) in PAGES.items():
        if slug.startswith("wedding/"):
            continue
        path = slug[:-len("index.html")] if slug.endswith("index.html") else slug
        if meta_en:
            urls.append(f"{SITE}/{path}")
        urls.append(f"{SITE}/id/{path}")
    body = "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n",
                                      encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


def main():
    (ROOT / "id").mkdir(exist_ok=True)
    for slug, (fn, meta_id, meta_en) in PAGES.items():
        for lang, (title, desc) in (("id", meta_id), ("en", meta_en)) if meta_en else (("id", meta_id),):
            out = ROOT / ("id" if lang == "id" else "") / slug
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page(lang, slug, title, desc, fn(lang)), encoding="utf-8")
            print("ditulis", out.relative_to(ROOT))
    sitemap()


if __name__ == "__main__":
    main()
