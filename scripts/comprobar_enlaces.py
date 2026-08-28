#!/usr/bin/env python3
"""
Comprobador de enlaces internos
═══════════════════════════════════════════
Verifica que todos los enlaces (href, src) de los HTMLs apuntan a archivos
que existen en el repo. Detecta enlaces rotos antes de hacer push.

Uso:
    python3 scripts/comprobar_enlaces.py

El script se ancla automáticamente a la raíz de su propio sitio
(la carpeta padre de scripts/), así que se puede invocar desde
cualquier directorio.
"""
import os, re, glob, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

os.chdir(Path(__file__).resolve().parent.parent)

EXCLUDE = ["documentacion/", "_soluciones/", ".git/", "node_modules/", ".wrangler/", "assets/templates/"]

def main():
    htmls = [f for f in glob.glob("**/*.html", recursive=True)
             if not any(e in f.replace("\\", "/") for e in EXCLUDE)]

    broken = []
    total_links = 0
    for f in htmls:
        with open(f, encoding="utf-8", errors="ignore") as fh:
            content = fh.read()
        links = re.findall(r'(?:href|src)="([^"]+)"', content)
        for link in links:
            if link.startswith(("http", "https", "mailto:", "#", "data:", "javascript:", "//")):
                continue
            # Saltar template literals de JavaScript (${...}) que aparecen dentro
            # de bloques <script> de los libros digitales y se interpolan en runtime.
            if "${" in link:
                continue
            total_links += 1
            target = link.split("?")[0].split("#")[0]
            if not target: continue
            base_dir = os.path.dirname(f)
            full_target = os.path.normpath(os.path.join(base_dir, target))
            if not os.path.exists(full_target):
                broken.append((f, link, full_target))

    print(f"HTMLs analizados:    {len(htmls)}")
    print(f"Enlaces internos:    {total_links}")
    print(f"Enlaces rotos:       {len(broken)}")
    print()

    if broken:
        for src, link, target in broken[:50]:
            print(f"  [X] {src}")
            print(f"    enlace: {link}")
            print(f"    busca:  {target}")
            print()
        return 1
    else:
        print("[OK] Todos los enlaces internos validos.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
