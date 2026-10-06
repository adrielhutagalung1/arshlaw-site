#!/usr/bin/env python3
"""Membangun halaman statis situs ARSH & Partners Law Office (ID dan EN).

Jalankan: python3 build.py
Halaman Indonesia ditulis di root, halaman Inggris di en/.
Teks bertanda .todo masih menunggu isi dari advokat.
"""
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
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
    ("wawasan.html", "Wawasan", "Insights"),
    ("kontak.html", "Kontak", "Contact"),
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


def page(lang, slug, title, description, body):
    depth = "../" if lang == "en" else ""
    prefix = "en/" if lang == "en" else ""
    path = "" if slug == "index.html" else slug
    other_href = ("en/" + slug) if lang == "id" else ("../" + slug)
    nav = "\n      ".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == slug else ""}>{T(lang, i, e)}</a>' for h, i, e in NAV)
    lang_top = (f'<span class="on">ID</span> / <a href="{other_href}" hreflang="en">EN</a>' if lang == "id"
                else f'<a href="{other_href}" hreflang="id">ID</a> / <span class="on">EN</span>')
    lang_nav = (f'<a class="nav-lang" href="{other_href}" hreflang="en">English</a>' if lang == "id"
                else f'<a class="nav-lang" href="{other_href}" hreflang="id">Bahasa Indonesia</a>')
    full_title = title if slug == "index.html" else f"{title} | ARSH &amp; Partners Law Office"
    foot_nav = "".join(f'<li><a href="{h}">{T(lang, i, e)}</a></li>' for h, i, e in NAV)
    foot_practice = "".join(
        f'<li><a href="layanan.html#{a}">{T(lang, ti, te)}</a></li>' for a, ti, te, *_ in PRACTICE[:5])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE}/{prefix}{path}">
<link rel="alternate" hreflang="id" href="{SITE}/{path}">
<link rel="alternate" hreflang="en" href="{SITE}/en/{path}">
<link rel="alternate" hreflang="x-default" href="{SITE}/{path}">
<meta property="og:site_name" content="ARSH &amp; Partners Law Office">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE}/{prefix}{path}">
<meta property="og:locale" content="{T(lang, 'id_ID', 'en_US')}">
<meta name="theme-color" content="#121212">
<link rel="icon" href="{depth}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital@0;1&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{depth}assets/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LegalService","name":"ARSH & Partners Law Office","url":"{SITE}/","email":"{EMAIL}","telephone":"+{WA_NUMBER}","address":{{"@type":"PostalAddress","streetAddress":"Plaza Indonesia L5 Unit E021AB, Jl. M.H. Thamrin Kav. 28-30","addressLocality":"Jakarta","postalCode":"10350","addressCountry":"ID"}}}}
</script>
</head>
<body>
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
    <a class="logo" href="index.html">ARSH &amp; Partners<small>LAW OFFICE</small></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="{T(lang, 'Navigasi utama', 'Main navigation')}">
      {nav}
      {lang_nav}
    </nav>
    <a class="btn btn-accent btn-small header-cta" href="{wa(lang)}">{T(lang, 'Hubungi kami', 'Contact us')}</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="index.html">ARSH &amp; Partners<small>LAW OFFICE</small></a>
        <p style="margin-top:16px">{address(lang)}</p>
        <p><a href="{MAPS}" rel="noopener">{T(lang, 'Petunjuk arah', 'Get directions')} &rarr;</a></p>
      </div>
      <div><h2>{T(lang, 'Halaman', 'Pages')}</h2><ul>{foot_nav}</ul></div>
      <div><h2>{T(lang, 'Layanan', 'Services')}</h2><ul>{foot_practice}</ul></div>
      <div><h2>{T(lang, 'Kontak', 'Contact')}</h2><ul>
        <li>WhatsApp <a href="{wa(lang)}">{WA_DISPLAY}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{T(lang, 'Jam kerja', 'Office hours')}: {todo(T(lang, 'hari dan jam', 'days and hours'))}</li>
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
</script>
</body>
</html>
"""


def practice_list(lang, linked=True):
    rows = []
    for a, ti, te, di, de in PRACTICE:
        inner = f'<h3>{T(lang, ti, te)}</h3><p>{T(lang, di, de)}</p><span class="arrow" aria-hidden="true">&rarr;</span>'
        rows.append(f'<li><a href="layanan.html#{a}">{inner}</a></li>')
    return '<ul class="practice">' + "".join(rows) + "</ul>"


def person(lang, heading_level="h2"):
    return f"""<div class="person">
      <div class="photo">{T(lang, 'Foto advokat', 'Photo')}</div>
      <div>
        <{heading_level}>{todo(T(lang, 'Nama lengkap, S.H., M.H.', 'Full name, S.H., M.H.'))}</{heading_level}>
        <p class="role">{T(lang, 'Advokat Pengelola', 'Managing Partner')}</p>
        <p>{todo(T(lang, 'latar belakang pendidikan, pengalaman, dan bidang yang paling sering ditangani', 'education, experience, and main practice areas'))}</p>
      </div>
    </div>"""


def closing(lang):
    return f"""<section class="closing">
  <div class="wrap">
    <div>
      <h2>{T(lang, 'Ingin membicarakan persoalan Anda?', 'Would you like to discuss your matter?')}</h2>
      <p>{T(lang, 'Kirim pesan singkat lewat WhatsApp, kami akan menghubungi Anda kembali.', 'Send us a short WhatsApp message and we will get back to you.')}</p>
    </div>
    <a class="btn btn-accent" href="{wa(lang)}">{WA_ICON} WhatsApp {WA_DISPLAY}</a>
  </div>
</section>"""


def home(lang):
    return f"""
<section class="hero">
  <div class="wrap">
    <div>
      <h1>{T(lang, 'Kantor hukum untuk pengusaha, perusahaan, dan keluarga di Jakarta.', 'A law office for business owners, companies, and families in Jakarta.')}</h1>
      <p class="intro">{T(lang, 'Kami menyusun dan memeriksa perjanjian, menangani urusan ketenagakerjaan, dan mendampingi Anda di pengadilan bila sengketa tidak terhindarkan.', 'We draft and review agreements, handle employment matters, and represent you in court when a dispute cannot be avoided.')}</p>
      <div class="buttons">
        <a class="btn btn-accent" href="{wa(lang)}">{WA_ICON} {T(lang, 'Konsultasi lewat WhatsApp', 'Consult via WhatsApp')}</a>
        <a class="btn btn-line" href="layanan.html">{T(lang, 'Lihat layanan', 'View services')}</a>
      </div>
    </div>
    <aside class="office-card">
      <h2>{T(lang, 'Kantor kami', 'Our office')}</h2>
      <dl>
        <dt>{T(lang, 'Alamat', 'Address')}</dt><dd>{address(lang)}</dd>
        <dt>WhatsApp</dt><dd><a href="{wa(lang)}">{WA_DISPLAY}</a></dd>
        <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>{T(lang, 'Jam kerja', 'Hours')}</dt><dd>{todo(T(lang, 'hari dan jam', 'days and hours'))}</dd>
      </dl>
      <a class="btn btn-line btn-small" href="{MAPS}" rel="noopener">{T(lang, 'Petunjuk arah', 'Get directions')}</a>
    </aside>
  </div>
</section>

<section class="block">
  <div class="wrap split">
    <header>
      <h2>{T(lang, 'Bidang praktik', 'Practice areas')}</h2>
      <p>{T(lang, 'Sebagian besar pekerjaan kami bersifat pencegahan: memastikan dokumen benar sebelum ditandatangani.', 'Most of our work is preventive: getting documents right before they are signed.')}</p>
    </header>
    {practice_list(lang)}
  </div>
</section>

<section class="block block-soft">
  <div class="wrap">
    <p class="quote">{T(lang, '&ldquo;Cegah selagi bisa dicegah, perbaiki segera setelah disadari.&rdquo;', '&ldquo;Prevent when you are able to prevent; fix it as soon as you notice it.&rdquo;')}</p>
    <p class="quote-by">{T(lang, 'Dari tulisan kami,', 'From our article,')} <a href="wawasan.html#irony-of-law"><em>The Irony of Law</em></a></p>
  </div>
</section>

<section class="block">
  <div class="wrap split">
    <header><h2>{T(lang, 'Advokat', 'Our lawyers')}</h2></header>
    <div>
      {person(lang, 'h3')}
      <p style="margin-top:24px"><a class="link-arrow" href="tentang.html">{T(lang, 'Tentang kantor kami', 'About the firm')} &rarr;</a></p>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap split">
    <header>
      <h2>{T(lang, 'Wawasan', 'Insights')}</h2>
      <p><a class="link-arrow" href="wawasan.html">{T(lang, 'Semua tulisan', 'All articles')} &rarr;</a></p>
    </header>
    <ul class="posts">
      <li><span class="meta">{T(lang, 'Artikel', 'Article')}</span><div><h3><a href="wawasan.html#irony-of-law">The Irony of Law</a></h3><p>{T(lang, 'Mengapa pencegahan hampir selalu lebih ringan daripada penyelesaian perkara.', 'Why prevention is almost always lighter than resolving a case.')}</p></div></li>
      <li><span class="meta">Legal Reminder Series</span><div><h3><a href="wawasan.html#legal-reminder">{T(lang, 'Bab 1: Tanda Tangan', 'Chapter 1: Signature')}</a></h3><p>{T(lang, 'Seri pengingat hukum singkat yang dapat diunduh.', 'A short, downloadable series of legal reminders.')}</p></div></li>
    </ul>
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
  <div class="wrap split">
    <header><h2>{T(lang, 'Advokat', 'Our lawyers')}</h2></header>
    {person(lang, 'h3')}
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
        <dt>{T(lang, 'Jam kerja', 'Office hours')}</dt><dd>{todo(T(lang, 'hari dan jam', 'days and hours'))}</dd>
      </dl>
      <p style="margin-top:32px"><a class="btn btn-accent" href="{wa(lang)}">{WA_ICON} {T(lang, 'Kirim pesan WhatsApp', 'Send a WhatsApp message')}</a></p>
    </div>
    <iframe class="map" src="{MAP_EMBED}" loading="lazy" title="{T(lang, 'Peta lokasi Plaza Indonesia', 'Map of Plaza Indonesia')}" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</section>
"""


PAGES = {
    "index.html": (home,
                   ("ARSH &amp; Partners Law Office | Kantor Hukum di Jakarta",
                    "Kantor hukum di Plaza Indonesia, Jakarta, untuk pengusaha, perusahaan, dan keluarga: perjanjian, ketenagakerjaan, litigasi, dan kepailitan."),
                   ("ARSH &amp; Partners Law Office | Law Office in Jakarta",
                    "A law office at Plaza Indonesia, Jakarta, for business owners, companies, and families: agreements, employment, litigation, and insolvency.")),
    "layanan.html": (services,
                     ("Layanan", "Pendampingan hukum usaha, pengacara pribadi, litigasi, ketenagakerjaan, PKPU dan kepailitan, hak cipta dan merek, serta konsultasi SDM."),
                     ("Services", "Business legal retainer, personal lawyer, litigation, employment, insolvency, copyright and trademarks, and HR consulting.")),
    "tentang.html": (about,
                     ("Tentang Kami", "Tentang ARSH &amp; Partners Law Office dan advokatnya."),
                     ("About", "About ARSH &amp; Partners Law Office and its lawyers.")),
    "wawasan.html": (insights,
                     ("Wawasan", "Artikel dan Legal Reminder Series dari ARSH &amp; Partners Law Office."),
                     ("Insights", "Articles and the Legal Reminder Series from ARSH &amp; Partners Law Office.")),
    "kontak.html": (contact,
                    ("Kontak", "Hubungi ARSH &amp; Partners Law Office lewat WhatsApp atau email, atau kunjungi kantor kami di Plaza Indonesia, Jakarta."),
                    ("Contact", "Contact ARSH &amp; Partners Law Office by WhatsApp or email, or visit our office at Plaza Indonesia, Jakarta.")),
}


def main():
    (ROOT / "en").mkdir(exist_ok=True)
    for slug, (fn, meta_id, meta_en) in PAGES.items():
        for lang, (title, desc) in (("id", meta_id), ("en", meta_en)):
            out = ROOT / ("en" if lang == "en" else "") / slug
            out.write_text(page(lang, slug, title, desc, fn(lang)), encoding="utf-8")
            print("ditulis", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
