#!/usr/bin/env python3
"""Membangun halaman statis situs ARSH & Partners Law Office (ID dan EN).

Jalankan: python3 build.py
Hasilnya ditulis langsung ke folder repositori (index.html, layanan.html, en/...).
Teks bertanda [ISI DARI ADVOKAT] masih menunggu isi dari advokat.
"""
from pathlib import Path

ROOT = Path(__file__).parent

FIRM = "ARSH &amp; Partners Law Office"
EMAIL = "info@arshlaw.id"
# Nomor resmi belum dikonfirmasi advokat; sementara memakai nomor tombol WhatsApp di situs lama.
WA_NUMBER = "6282129652342"
WA_DISPLAY = "+62 821 2965 2342"
ADDRESS = "Plaza Indonesia Lt. 5 Unit #E021AB<br>Jl. M.H. Thamrin Kav. 28–30<br>Jakarta 10350"
ADDRESS_EN = "Plaza Indonesia Level 5 Unit #E021AB<br>Jl. M.H. Thamrin Kav. 28–30<br>Jakarta 10350, Indonesia"
SITE = "https://www.arshlaw.id"


def ph(text):
    return f'<span class="placeholder">[ISI DARI ADVOKAT: {text}]</span>'


L = {
    "id": {
        "lang": "id",
        "prefix": "",
        "nav": [("index.html", "Beranda"), ("layanan.html", "Layanan"), ("tentang.html", "Tentang Kami"),
                ("wawasan.html", "Wawasan"), ("kontak.html", "Kontak")],
        "menu": "Menu",
        "skip": "Lewati ke isi",
        "wa_text": "Halo ARSH & Partners Law Office, saya ingin berkonsultasi.",
        "wa_cta": "Konsultasi via WhatsApp",
        "wa_float": "WhatsApp",
        "footer_tag": "Kantor hukum di Jakarta untuk pengusaha, perusahaan, dan perorangan.",
        "footer_pages": "Halaman",
        "footer_contact": "Kontak",
        "fine": "Informasi di situs ini bersifat umum dan bukan nasihat hukum untuk perkara tertentu.",
        "address": ADDRESS,
    },
    "en": {
        "lang": "en",
        "prefix": "en/",
        "nav": [("index.html", "Home"), ("layanan.html", "Services"), ("tentang.html", "About"),
                ("wawasan.html", "Insights"), ("kontak.html", "Contact")],
        "menu": "Menu",
        "skip": "Skip to content",
        "wa_text": "Hello ARSH & Partners Law Office, I would like a consultation.",
        "wa_cta": "Consult via WhatsApp",
        "wa_float": "WhatsApp",
        "footer_tag": "A Jakarta law office for business owners, companies, and individuals.",
        "footer_pages": "Pages",
        "footer_contact": "Contact",
        "fine": "Information on this site is general and is not legal advice for any specific matter.",
        "address": ADDRESS_EN,
    },
}


def wa_link(lang):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUMBER}?text={quote(L[lang]['wa_text'])}"


def page(lang, slug, title, description, body):
    c = L[lang]
    other = "en" if lang == "id" else "id"
    depth = "../" if lang == "en" else ""
    other_href = ("en/" + slug) if lang == "id" else ("../" + slug)
    nav = "\n".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == slug else ""}>{label}</a>'
        for href, label in c["nav"]
    )
    lang_switch = (
        f'<span class="lang"><strong>ID</strong> · <a href="{other_href}" hreflang="en" lang="en">EN</a></span>'
        if lang == "id" else
        f'<span class="lang"><a href="{other_href}" hreflang="id" lang="id">ID</a> · <strong>EN</strong></span>'
    )
    canonical = f"{SITE}/{c['prefix']}{'' if slug == 'index.html' else slug}"
    alt_id = f"{SITE}/{'' if slug == 'index.html' else slug}"
    alt_en = f"{SITE}/en/{'' if slug == 'index.html' else slug}"
    footer_links = "\n".join(f'<li><a href="{h}">{t}</a></li>' for h, t in c["nav"])
    full_title = title if slug == "index.html" else f"{title} · ARSH &amp; Partners Law Office"
    return f"""<!doctype html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="id" href="{alt_id}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="{depth}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Public+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{depth}assets/style.css">
</head>
<body>
<a class="skip" href="#isi">{c['skip']}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><span class="brand-name">ARSH &amp; Partners</span><span class="brand-sub">Law Office</span></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav">{c['menu']}</button>
    <nav class="nav" id="nav" aria-label="Menu">
      {nav}
      {lang_switch}
    </nav>
  </div>
</header>
<main id="isi">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <p class="brand-name">{FIRM}</p>
      <p>{c['footer_tag']}</p>
    </div>
    <div>
      <p><strong>{c['footer_pages']}</strong></p>
      <ul>{footer_links}</ul>
    </div>
    <div>
      <p><strong>{c['footer_contact']}</strong></p>
      <p><a href="{wa_link(lang)}">{WA_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>{c['address']}</p>
    </div>
    <p class="fine">© 2026 {FIRM}. {c['fine']}</p>
  </div>
</footer>
<a class="wa-float" href="{wa_link(lang)}" aria-label="{c['wa_cta']}">{c['wa_float']}</a>
<script>
  const t = document.querySelector('.menu-toggle'), n = document.getElementById('nav');
  t.addEventListener('click', () => {{ const o = n.classList.toggle('open'); t.setAttribute('aria-expanded', o); }});
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- Isi halaman

def home(lang):
    wa = wa_link(lang)
    if lang == "id":
        return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">ARSH &amp; Partners Law Office · Jakarta</p>
    <h1>Urusan hukum usaha Anda,<br>ditata sejak awal.</h1>
    <p class="lead">Kami membantu pengusaha dan perusahaan menyusun perjanjian, mengelola hubungan kerja, dan menyelesaikan sengketa dengan tenang dan terukur.</p>
    <div class="actions">
      <a class="btn btn-primary" href="{wa}">Konsultasi via WhatsApp</a>
      <a class="btn btn-ghost" href="layanan.html">Lihat layanan</a>
    </div>
    <div class="rule"></div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>Untuk siapa kami bekerja</h2>
      <p>Sebagian besar persoalan hukum bisa dicegah bila ditangani sejak dokumen pertama ditandatangani. Di situlah kami paling banyak membantu.</p>
    </div>
    <div class="for-whom">
      <div><h3>Pemilik usaha</h3><p>Usaha kecil dan menengah yang membutuhkan pendampingan hukum rutin tanpa harus memiliki bagian hukum sendiri.</p></div>
      <div><h3>Perusahaan</h3><p>Perjanjian dengan mitra, pemasok, dan karyawan; kepatuhan ketenagakerjaan; serta penyelesaian sengketa.</p></div>
      <div><h3>Perorangan</h3><p>Pemeriksaan dokumen, perjanjian pribadi, dan pendampingan saat menghadapi persoalan hukum.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <h2>Layanan utama</h2>
      <p>Pilih sesuai kebutuhan Anda. Setiap layanan dimulai dengan percakapan singkat untuk memahami persoalannya.</p>
    </div>
    <div class="grid-3">
      <article class="card"><span class="num">01</span><h3>Pendampingan Hukum Usaha</h3><p>Pengacara langganan untuk usaha Anda: menyusun dan memeriksa perjanjian, menangani persoalan karyawan, dan membantu penagihan.</p><a class="more" href="layanan.html#usaha">Selengkapnya</a></article>
      <article class="card"><span class="num">02</span><h3>Litigasi &amp; Sengketa</h3><p>Pendampingan perkara perdata, pidana, hubungan industrial, PKPU, dan kepailitan, termasuk somasi sebelum ke pengadilan.</p><a class="more" href="layanan.html#litigasi">Selengkapnya</a></article>
      <article class="card"><span class="num">03</span><h3>Ketenagakerjaan &amp; SDM</h3><p>Perjanjian kerja, prosedur pemutusan hubungan kerja, serta pelatihan dan konsultasi SDM untuk tim Anda.</p><a class="more" href="layanan.html#ketenagakerjaan">Selengkapnya</a></article>
    </div>
  </div>
</section>

<section class="band-ink">
  <div class="wrap">
    <div class="section-head">
      <h2>Cara kami bekerja</h2>
      <p style="color:#CFC9BC">Sederhana dan jelas sejak awal.</p>
    </div>
    <ol class="steps">
      <li><h3>Ceritakan persoalan Anda</h3><p>Hubungi kami lewat WhatsApp atau email. Kami mendengarkan dan menanyakan hal yang perlu.</p></li>
      <li><h3>Terima penawaran</h3><p>Kami menjelaskan langkah yang kami sarankan dan biayanya secara tertulis sebelum pekerjaan dimulai.</p></li>
      <li><h3>Kami tangani</h3><p>Anda mendapat kabar perkembangan secara berkala sampai urusan selesai.</p></li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap profile">
    <div class="photo">{ph('foto advokat pengelola')}</div>
    <div>
      <p class="eyebrow">Advokat pengelola</p>
      <h2>{ph('Nama, S.H., M.H.')}</h2>
      <p>{ph('dua sampai tiga kalimat tentang latar belakang, bidang keahlian, dan cara bekerja advokat pengelola')}</p>
      <a class="more" href="tentang.html">Tentang kantor kami</a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>Wawasan</h2>
      <p>Tulisan singkat tentang hukum sehari-hari untuk pengusaha dan pekerja.</p>
    </div>
    <ul class="article-list">
      <li><span class="meta">Artikel</span><div><h3><a href="wawasan.html#ironi-hukum">The Irony of Law</a></h3><p class="muted">Mengapa pencegahan hampir selalu lebih murah daripada penyelesaian perkara.</p></div></li>
      <li><span class="meta">Legal Reminder Series</span><div><h3><a href="wawasan.html#legal-reminder">Tanda tangan, syarat dan ketentuan, dan ketenagakerjaan</a></h3><p class="muted">Seri pengingat hukum yang bisa diunduh.</p></div></li>
    </ul>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Ada persoalan hukum yang ingin dibicarakan?</h2>
    <a class="btn btn-primary" href="{wa}">Konsultasi via WhatsApp</a>
  </div>
</section>
"""
    return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">ARSH &amp; Partners Law Office · Jakarta</p>
    <h1>Your business's legal matters,<br>in order from the start.</h1>
    <p class="lead">We help business owners and companies draft agreements, manage employment relationships, and resolve disputes calmly and carefully.</p>
    <div class="actions">
      <a class="btn btn-primary" href="{wa}">Consult via WhatsApp</a>
      <a class="btn btn-ghost" href="layanan.html">Our services</a>
    </div>
    <div class="rule"></div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head">
      <h2>Who we work with</h2>
      <p>Most legal problems can be prevented when they are handled from the first signed document. That is where we help most.</p>
    </div>
    <div class="for-whom">
      <div><h3>Business owners</h3><p>Small and medium businesses that need regular legal support without an in-house legal team.</p></div>
      <div><h3>Companies</h3><p>Agreements with partners, suppliers, and employees; employment compliance; and dispute resolution.</p></div>
      <div><h3>Individuals</h3><p>Document review, personal agreements, and support when facing a legal problem.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <h2>Core services</h2>
      <p>Every engagement begins with a short conversation to understand the matter.</p>
    </div>
    <div class="grid-3">
      <article class="card"><span class="num">01</span><h3>Business Legal Retainer</h3><p>A retained lawyer for your business: drafting and reviewing agreements, handling employee matters, and supporting collections.</p><a class="more" href="layanan.html#usaha">Read more</a></article>
      <article class="card"><span class="num">02</span><h3>Litigation &amp; Disputes</h3><p>Civil, criminal, industrial relations, suspension of payments (PKPU), and bankruptcy matters, including demand letters before court.</p><a class="more" href="layanan.html#litigasi">Read more</a></article>
      <article class="card"><span class="num">03</span><h3>Employment &amp; HR</h3><p>Employment agreements, termination procedures, and HR training and consulting for your team.</p><a class="more" href="layanan.html#ketenagakerjaan">Read more</a></article>
    </div>
  </div>
</section>

<section class="band-ink">
  <div class="wrap">
    <div class="section-head">
      <h2>How we work</h2>
      <p style="color:#CFC9BC">Simple and clear from the start.</p>
    </div>
    <ol class="steps">
      <li><h3>Tell us the matter</h3><p>Reach us by WhatsApp or email. We listen and ask what we need to know.</p></li>
      <li><h3>Receive a proposal</h3><p>We explain the steps we recommend and the fees in writing before any work begins.</p></li>
      <li><h3>We handle it</h3><p>You receive regular updates until the matter is resolved.</p></li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap profile">
    <div class="photo">{ph('managing partner photo')}</div>
    <div>
      <p class="eyebrow">Managing partner</p>
      <h2>{ph('Name, S.H., M.H.')}</h2>
      <p>{ph('two or three sentences on background, practice areas, and way of working')}</p>
      <a class="more" href="tentang.html">About the firm</a>
    </div>
  </div>
</section>

<section class="cta-band band">
  <div class="wrap">
    <h2>Have a legal matter you would like to discuss?</h2>
    <a class="btn btn-primary" href="{wa}">Consult via WhatsApp</a>
  </div>
</section>
"""


def services(lang):
    wa = wa_link(lang)
    if lang == "id":
        return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Layanan</p>
    <h1>Layanan hukum yang dimulai dari pencegahan.</h1>
    <p class="lead">Kami lebih suka membantu Anda menghindari sengketa daripada menyelesaikannya. Bila sengketa sudah terjadi, kami mendampingi sampai tuntas.</p>
  </div>
</section>
<section class="band" id="usaha">
  <div class="wrap">
    <div class="grid-2">
      <article class="card"><span class="num">01</span><h3>Pendampingan Hukum Usaha</h3>
        <p>Seperti memiliki dokter keluarga untuk urusan hukum usaha Anda. Cocok untuk usaha kecil dan menengah yang belum memiliki bagian hukum.</p>
        <ul><li>Menyusun dan memeriksa perjanjian dengan pemasok, vendor, dan mitra</li><li>Perjanjian kerja dan persoalan karyawan</li><li>Pendampingan penagihan piutang</li><li>Konsultasi rutin saat ada keputusan penting</li></ul>
        <a class="more" href="{wa}">Minta informasi &amp; penawaran</a></article>
      <article class="card"><span class="num">02</span><h3>Pengacara Pribadi</h3>
        <p>Untuk perorangan yang mengurus banyak perjanjian dan dokumen, dan ingin memastikan semuanya aman sebelum ditandatangani.</p>
        <ul><li>Pemeriksaan dokumen dan perjanjian</li><li>Pendapat hukum atas persoalan pribadi</li><li>Pendampingan saat menghadapi persoalan hukum</li></ul>
        <a class="more" href="{wa}">Minta informasi &amp; penawaran</a></article>
    </div>
  </div>
</section>
<section id="litigasi">
  <div class="wrap">
    <div class="section-head"><h2>Litigasi &amp; Sengketa</h2><p>Bila persoalan tidak dapat diselesaikan dengan musyawarah, kami mendampingi Anda di setiap tahap.</p></div>
    <div class="grid-3">
      <article class="card"><h3>Perdata</h3><p>Wanprestasi, perbuatan melawan hukum, dan sengketa perjanjian.</p></article>
      <article class="card"><h3>Pidana</h3><p>Pendampingan sejak pemeriksaan hingga persidangan.</p></article>
      <article class="card"><h3>Hubungan Industrial</h3><p>Perselisihan ketenagakerjaan di Pengadilan Hubungan Industrial.</p></article>
      <article class="card"><h3>PKPU &amp; Kepailitan</h3><p>Pendampingan kreditur maupun debitur.</p></article>
      <article class="card"><h3>Somasi</h3><p>Penyusunan dan penanganan somasi sebelum perkara ke pengadilan.</p></article>
      <article class="card"><h3>Hak Kekayaan Intelektual</h3><p>Pendaftaran dan penegakan hak cipta serta merek.</p></article>
    </div>
  </div>
</section>
<section class="band" id="ketenagakerjaan">
  <div class="wrap">
    <div class="section-head"><h2>Ketenagakerjaan &amp; SDM</h2><p>Menggabungkan kepatuhan hukum ketenagakerjaan dengan pengembangan orang di dalam organisasi Anda.</p></div>
    <div class="grid-3">
      <article class="card"><h3>Hukum ketenagakerjaan</h3><p>Perjanjian kerja, peraturan perusahaan, dan prosedur pemutusan hubungan kerja.</p></article>
      <article class="card"><h3>Pelatihan HRD &amp; HRM</h3><p>Kepemimpinan, rekrutmen, penilaian kinerja, pengelolaan konflik, dan kepatuhan ketenagakerjaan.</p></article>
      <article class="card"><h3>Psikologi &amp; konseling karyawan</h3><p>Dukungan bagi kesejahteraan karyawan dan keharmonisan tempat kerja.</p></article>
      <article class="card"><h3>Keterampilan lunak</h3><p>Komunikasi, manajemen waktu, dan kecerdasan emosional.</p></article>
      <article class="card"><h3>Program khusus</h3><p>Persiapan pensiun, team building, kewirausahaan, dan pelayanan publik.</p></article>
      <article class="card"><h3>Bidang lain</h3><p>Perlindungan konsumen, perdagangan dan ekspor-impor, serta hukum pendidikan.</p></article>
    </div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap"><h2>Belum yakin layanan mana yang tepat?</h2><a class="btn btn-primary" href="{wa}">Tanyakan via WhatsApp</a></div>
</section>
"""
    return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h1>Legal services that begin with prevention.</h1>
    <p class="lead">We would rather help you avoid a dispute than resolve one. When a dispute has already arisen, we stay with you until it is settled.</p>
  </div>
</section>
<section class="band" id="usaha">
  <div class="wrap">
    <div class="grid-2">
      <article class="card"><span class="num">01</span><h3>Business Legal Retainer</h3>
        <p>Like having a family doctor for your business's legal matters. Suited to small and medium businesses without an in-house legal team.</p>
        <ul><li>Drafting and reviewing agreements with suppliers, vendors, and partners</li><li>Employment agreements and employee matters</li><li>Support with collections</li><li>Regular consultation on important decisions</li></ul>
        <a class="more" href="{wa}">Request information &amp; a quotation</a></article>
      <article class="card"><span class="num">02</span><h3>Personal Lawyer</h3>
        <p>For individuals who handle many agreements and documents and want them checked before signing.</p>
        <ul><li>Document and agreement review</li><li>Legal opinions on personal matters</li><li>Support when facing a legal problem</li></ul>
        <a class="more" href="{wa}">Request information &amp; a quotation</a></article>
    </div>
  </div>
</section>
<section id="litigasi">
  <div class="wrap">
    <div class="section-head"><h2>Litigation &amp; Disputes</h2><p>When a matter cannot be settled by agreement, we represent you at every stage.</p></div>
    <div class="grid-3">
      <article class="card"><h3>Civil</h3><p>Breach of contract, unlawful acts, and contract disputes.</p></article>
      <article class="card"><h3>Criminal</h3><p>Representation from investigation through trial.</p></article>
      <article class="card"><h3>Industrial Relations</h3><p>Employment disputes before the Industrial Relations Court.</p></article>
      <article class="card"><h3>PKPU &amp; Bankruptcy</h3><p>Acting for creditors and debtors.</p></article>
      <article class="card"><h3>Demand letters</h3><p>Drafting and responding to demand letters (somasi) before court.</p></article>
      <article class="card"><h3>Intellectual Property</h3><p>Copyright and trademark registration and enforcement.</p></article>
    </div>
  </div>
</section>
<section class="band" id="ketenagakerjaan">
  <div class="wrap">
    <div class="section-head"><h2>Employment &amp; HR</h2><p>Employment law compliance combined with developing the people in your organisation.</p></div>
    <div class="grid-3">
      <article class="card"><h3>Employment law</h3><p>Employment agreements, company regulations, and termination procedures.</p></article>
      <article class="card"><h3>HRD &amp; HRM training</h3><p>Leadership, recruitment, performance appraisal, conflict management, and labour compliance.</p></article>
      <article class="card"><h3>Employee psychology &amp; counselling</h3><p>Support for employee well-being and workplace harmony.</p></article>
      <article class="card"><h3>Soft skills</h3><p>Communication, time management, and emotional intelligence.</p></article>
      <article class="card"><h3>Custom programmes</h3><p>Pre-retirement, team building, entrepreneurship, and public service.</p></article>
      <article class="card"><h3>Other areas</h3><p>Consumer protection, trade and import-export, and education law.</p></article>
    </div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap"><h2>Not sure which service fits?</h2><a class="btn btn-primary" href="{wa}">Ask via WhatsApp</a></div>
</section>
"""


def about(lang):
    if lang == "id":
        return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Tentang Kami</p>
    <h1>Kantor hukum yang menjelaskan, bukan menakut-nakuti.</h1>
    <p class="lead">{FIRM} berkantor di Plaza Indonesia, Jakarta. Kami membawa cara pandang yang segar dan pendekatan yang luwes dalam menyelesaikan persoalan hukum klien.</p>
  </div>
</section>
<section class="band">
  <div class="wrap profile">
    <div class="photo">{ph('foto advokat pengelola')}</div>
    <div>
      <p class="eyebrow">Advokat pengelola</p>
      <h2>{ph('Nama, S.H., M.H.')}</h2>
      <p>{ph('latar belakang pendidikan, pengalaman, dan bidang keahlian')}</p>
      <p>{ph('keanggotaan organisasi advokat dan nomor induk, bila ingin ditampilkan')}</p>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><h2>Cara kami memandang pekerjaan ini</h2><p></p></div>
    <div class="for-whom">
      <div><h3>Mencegah lebih dulu</h3><p>Perjanjian yang disusun dengan benar sejak awal menghindarkan banyak sengketa di kemudian hari.</p></div>
      <div><h3>Jelas soal biaya</h3><p>Penawaran tertulis diberikan sebelum pekerjaan dimulai, sehingga Anda tahu apa yang akan dibayar.</p></div>
      <div><h3>Mudah dihubungi</h3><p>Anda bisa menghubungi kami lewat WhatsApp atau email, dan kami memberi kabar perkembangan secara berkala.</p></div>
    </div>
  </div>
</section>
"""
    return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>A law office that explains, rather than alarms.</h1>
    <p class="lead">{FIRM} is based at Plaza Indonesia, Jakarta. We bring a fresh perspective and a flexible approach to resolving our clients' legal matters.</p>
  </div>
</section>
<section class="band">
  <div class="wrap profile">
    <div class="photo">{ph('managing partner photo')}</div>
    <div>
      <p class="eyebrow">Managing partner</p>
      <h2>{ph('Name, S.H., M.H.')}</h2>
      <p>{ph('education, experience, and practice areas')}</p>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="for-whom">
      <div><h3>Prevention first</h3><p>An agreement drafted correctly from the start avoids many disputes later.</p></div>
      <div><h3>Clear on fees</h3><p>A written proposal is provided before work begins, so you know what you will pay.</p></div>
      <div><h3>Easy to reach</h3><p>Reach us by WhatsApp or email, and expect regular updates on progress.</p></div>
    </div>
  </div>
</section>
"""


def insights(lang):
    if lang == "id":
        return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Wawasan</p>
    <h1>Tulisan dan pengingat hukum.</h1>
    <p class="lead">Bacaan singkat untuk membantu Anda mengenali persoalan hukum sebelum menjadi besar.</p>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <ul class="article-list">
      <li id="ironi-hukum"><span class="meta">Artikel · {ph('tanggal')}</span><div><h3>The Irony of Law</h3><p class="muted">Cegah selagi bisa dicegah, perbaiki segera setelah disadari. {ph('isi artikel dipindahkan dari situs lama setelah ditinjau advokat')}</p></div></li>
    </ul>
  </div>
</section>
<section id="legal-reminder">
  <div class="wrap">
    <div class="section-head"><h2>Legal Reminder Series</h2><p>Seri pengingat hukum yang bisa diunduh.</p></div>
    <ul class="article-list">
      <li><span class="meta">Bab 1</span><div><h3>Tanda Tangan</h3><p class="muted">{ph('tanggal dan berkas PDF')}</p></div></li>
      <li><span class="meta">Bab 2</span><div><h3>Syarat dan Ketentuan</h3><p class="muted">{ph('tanggal dan berkas PDF')}</p></div></li>
      <li><span class="meta">Bab 3</span><div><h3>Ketenagakerjaan I</h3><p class="muted">{ph('tanggal dan berkas PDF')}</p></div></li>
    </ul>
  </div>
</section>
"""
    return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Insights</p>
    <h1>Articles and legal reminders.</h1>
    <p class="lead">Short reads to help you spot legal problems before they grow.</p>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <ul class="article-list">
      <li id="ironi-hukum"><span class="meta">Article · {ph('date')}</span><div><h3>The Irony of Law</h3><p class="muted">Prevent when you are able to prevent; fix it as soon as you notice it. {ph('article text moved from the old site after review')}</p></div></li>
    </ul>
  </div>
</section>
<section id="legal-reminder">
  <div class="wrap">
    <div class="section-head"><h2>Legal Reminder Series</h2><p>Downloadable legal reminders.</p></div>
    <ul class="article-list">
      <li><span class="meta">Chapter 1</span><div><h3>Signature</h3><p class="muted">{ph('date and PDF')}</p></div></li>
      <li><span class="meta">Chapter 2</span><div><h3>Terms and Conditions</h3><p class="muted">{ph('date and PDF')}</p></div></li>
      <li><span class="meta">Chapter 3</span><div><h3>Employment I</h3><p class="muted">{ph('date and PDF')}</p></div></li>
    </ul>
  </div>
</section>
"""


def contact(lang):
    wa = wa_link(lang)
    map_src = "https://www.google.com/maps?q=Plaza+Indonesia+Jakarta&output=embed"
    if lang == "id":
        return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Kontak</p>
    <h1>Mari bicarakan persoalan Anda.</h1>
    <p class="lead">Cara tercepat adalah lewat WhatsApp. Ceritakan secara singkat persoalannya, dan kami akan menghubungi Anda kembali.</p>
    <div class="actions"><a class="btn btn-primary" href="{wa}">Konsultasi via WhatsApp</a><a class="btn btn-ghost" href="mailto:{EMAIL}">Kirim email</a></div>
  </div>
</section>
<section class="band">
  <div class="wrap contact-grid">
    <dl>
      <dt>WhatsApp</dt><dd><a href="{wa}">{WA_DISPLAY}</a></dd>
      <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt>Alamat</dt><dd>{ADDRESS}</dd>
      <dt>Jam kerja</dt><dd>{ph('hari dan jam kerja')}</dd>
    </dl>
    <iframe class="map" src="{map_src}" loading="lazy" title="Peta Plaza Indonesia" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</section>
"""
    return f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Let's talk about your matter.</h1>
    <p class="lead">WhatsApp is the fastest way to reach us. Tell us briefly about the matter and we will get back to you.</p>
    <div class="actions"><a class="btn btn-primary" href="{wa}">Consult via WhatsApp</a><a class="btn btn-ghost" href="mailto:{EMAIL}">Send an email</a></div>
  </div>
</section>
<section class="band">
  <div class="wrap contact-grid">
    <dl>
      <dt>WhatsApp</dt><dd><a href="{wa}">{WA_DISPLAY}</a></dd>
      <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt>Address</dt><dd>{ADDRESS_EN}</dd>
      <dt>Office hours</dt><dd>{ph('days and hours')}</dd>
    </dl>
    <iframe class="map" src="{map_src}" loading="lazy" title="Map of Plaza Indonesia" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</section>
"""


PAGES = {
    "index.html": (home, {
        "id": ("ARSH &amp; Partners Law Office · Kantor Hukum di Jakarta",
               "Kantor hukum di Jakarta yang membantu pengusaha, perusahaan, dan perorangan menyusun perjanjian, mengelola hubungan kerja, dan menyelesaikan sengketa."),
        "en": ("ARSH &amp; Partners Law Office · Jakarta Law Office",
               "A Jakarta law office helping business owners, companies, and individuals with agreements, employment matters, and disputes."),
    }),
    "layanan.html": (services, {
        "id": ("Layanan", "Pendampingan hukum usaha, pengacara pribadi, litigasi dan sengketa, serta ketenagakerjaan dan SDM."),
        "en": ("Services", "Business legal retainer, personal lawyer, litigation and disputes, and employment and HR."),
    }),
    "tentang.html": (about, {
        "id": ("Tentang Kami", "Tentang ARSH & Partners Law Office dan advokat pengelolanya."),
        "en": ("About", "About ARSH & Partners Law Office and its managing partner."),
    }),
    "wawasan.html": (insights, {
        "id": ("Wawasan", "Artikel dan Legal Reminder Series dari ARSH & Partners Law Office."),
        "en": ("Insights", "Articles and the Legal Reminder Series from ARSH & Partners Law Office."),
    }),
    "kontak.html": (contact, {
        "id": ("Kontak", "Hubungi ARSH & Partners Law Office lewat WhatsApp, email, atau kunjungi kantor kami di Plaza Indonesia, Jakarta."),
        "en": ("Contact", "Contact ARSH & Partners Law Office by WhatsApp or email, or visit us at Plaza Indonesia, Jakarta."),
    }),
}


def main():
    (ROOT / "en").mkdir(exist_ok=True)
    for slug, (fn, meta) in PAGES.items():
        for lang in ("id", "en"):
            title, desc = meta[lang]
            out = ROOT / L[lang]["prefix"] / slug
            out.write_text(page(lang, slug, title, desc, fn(lang)), encoding="utf-8")
            print("ditulis", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
