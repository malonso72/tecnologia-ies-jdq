#!/usr/bin/env python3
"""
Actualizar sitemap.xml — Hub Tecnología
═══════════════════════════════════════════════════════════════════
Sitio con un solo index.html, así que sitemap.xml es trivial.
Este script lo regenera con la fecha de hoy.

Uso:
    python3 scripts/actualizar_seo.py

Se ancla automáticamente a la raíz del sitio.
"""
import os, sys
from pathlib import Path
from datetime import date

DOMAIN = "https://tecnologia-ies-jdq.malonso72.workers.dev"

os.chdir(Path(__file__).resolve().parent.parent)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

TODAY = date.today().isoformat()

sitemap = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url>\n'
    f'    <loc>{DOMAIN}/</loc>\n'
    f'    <lastmod>{TODAY}</lastmod>\n'
    '    <changefreq>monthly</changefreq>\n'
    '    <priority>1.0</priority>\n'
    '  </url>\n'
    '</urlset>\n'
)
Path("sitemap.xml").write_text(sitemap, encoding="utf-8")
print(f"sitemap.xml regenerado ({DOMAIN}/)")
