# arshlaw-site

Situs ARSH & Partners Law Office (www.arshlaw.id). Halaman statis, tanpa proses build di hosting.

- Ubah isi di `build.py`, lalu jalankan `python3 build.py` untuk menulis ulang halaman HTML di `public/` (EN di root, ID di `public/id/`).
- Gaya ada di `public/assets/style.css`.
- Teks bertanda `[ISI DARI ADVOKAT: ...]` masih menunggu isi dari advokat.
- Hosting: Cloudflare (Workers static assets lewat `wrangler.jsonc`, atau Pages dengan output directory `public`), tanpa build command.
