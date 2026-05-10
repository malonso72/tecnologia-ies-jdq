#!/usr/bin/env python3
"""
Auditor de archivos pesados
══════════════════════════════════════
Lista los archivos del sitio que superan un umbral de tamaño.

Uso:
    python3 scripts/auditar_archivos_pesados.py
    python3 scripts/auditar_archivos_pesados.py --umbral 200

Se ancla a la raíz del sitio.
"""
import os, sys, glob
from pathlib import Path

os.chdir(Path(__file__).resolve().parent.parent)

EXCLUDE = ["documentacion/", "_soluciones/", ".git/", "node_modules/", ".wrangler/"]

def main():
    umbral_kb = 100
    if "--umbral" in sys.argv:
        try:
            umbral_kb = int(sys.argv[sys.argv.index("--umbral") + 1])
        except (ValueError, IndexError):
            print("⚠ Argumento --umbral inválido, usando 100 KB")

    files = []
    for f in glob.glob("**/*", recursive=True):
        if not os.path.isfile(f): continue
        if any(e in f for e in EXCLUDE): continue
        s = os.path.getsize(f)
        if s > umbral_kb * 1024:
            files.append((f, s))

    files.sort(key=lambda x: -x[1])

    print(f"Archivos > {umbral_kb} KB: {len(files)}")
    print()
    for f, s in files[:40]:
        print(f"  {s/1024:7.0f} KB  {f}")

if __name__ == "__main__":
    main()
