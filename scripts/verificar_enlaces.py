#!/usr/bin/env python3
"""
verificar_enlaces.py — Verifica la integridad de los enlaces internos del sitio.

QUÉ VERIFICA
    1. Todos los href="..." relativos a ficheros del propio sitio resuelven a
       ficheros existentes (se omiten enlaces http/https, mailto, tel, data, #ancla-local).
    2. Todos los anchors #id referenciados por enlaces existen en su fichero destino.

CÓMO SE EJECUTA
    Desde la raíz del sitio:
        python3 scripts/verificar_enlaces.py

OUTPUT
    - Resumen de la categoría.
    - Lista de enlaces rotos con fichero origen y URL destino.
    Exit code 0 si 0 rotos, 1 si hay rotos.

ORIGEN
    Adaptado del verificador usado en teci2-ies-jdq (verano 2026), simplificado
    para este sitio (sin carpeta _soluciones/ ni convenciones de exámenes PAU).
"""
from __future__ import annotations
import os, re, sys
from pathlib import Path
from urllib.parse import urlparse, unquote

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {'templates', 'node_modules'}


def listar_htmls() -> list[Path]:
    out = []
    for p in ROOT.rglob('*.html'):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def extraer_hrefs(html: str) -> list[str]:
    hrefs = re.findall(r'(?:^|[\s<])href=["\']([^"\']+)["\']', html, re.MULTILINE)
    # Descarta hrefs con interpolacion JS (p.ej. href="${v.url}" dentro de una
    # plantilla de JavaScript) -- no son atributos HTML estaticos reales.
    return [h for h in hrefs if '${' not in h]


DYNAMIC_ID_RE = re.compile(
    r"""\.id\s*=\s*(?:`([a-zA-Z][\w-]*?)\$\{|['"]([a-zA-Z][\w-]*)['"]\s*\+)"""
)


def extraer_prefijos_dinamicos(html: str) -> set[str]:
    """Prefijos de id asignados en tiempo de ejecucion via JavaScript
    (p.ej. sec.id = `bloque-${num}` o sec.id = 'b' + k). El HTML estatico
    nunca contiene el id final, asi que un anchor que coincide con uno de
    estos prefijos + sufijo numerico no se considera roto."""
    prefijos = set()
    for m in DYNAMIC_ID_RE.finditer(html):
        p = m.group(1) or m.group(2)
        if p:
            prefijos.add(p)
    return prefijos


def es_externo(href: str) -> bool:
    u = urlparse(href)
    return u.scheme in ('http', 'https', 'mailto', 'tel', 'data')


def resolver(origen: Path, href: str) -> tuple[Path | None, str | None]:
    if es_externo(href):
        return None, None
    if href.startswith('#'):
        return origen.resolve(), href[1:]
    if '#' in href:
        ruta, anchor = href.split('#', 1)
    else:
        ruta, anchor = href, None
    if not ruta:
        return origen.resolve(), anchor
    if '?' in ruta:
        ruta = ruta.split('?', 1)[0]
    if not ruta:
        return origen.resolve(), anchor
    ruta = unquote(ruta)
    try:
        destino = (origen.parent / ruta).resolve()
    except Exception:
        return None, anchor
    return destino, anchor


def main() -> int:
    htmls = listar_htmls()
    print(f'[info] HTML escaneados: {len(htmls)}')

    rotos = []
    anchors_por_fichero: dict[Path, set[str]] = {}
    prefijos_por_fichero: dict[Path, set[str]] = {}
    for p in htmls:
        txt = p.read_text(encoding='utf-8', errors='ignore')
        anchors_por_fichero[p.resolve()] = set(re.findall(r'id="([^"]+)"', txt))
        prefijos_por_fichero[p.resolve()] = extraer_prefijos_dinamicos(txt)

    for p in htmls:
        txt = p.read_text(encoding='utf-8', errors='ignore')
        for href in extraer_hrefs(txt):
            if es_externo(href):
                continue
            destino, anchor = resolver(p, href)
            if destino is None:
                continue
            if not destino.exists():
                rotos.append((p.relative_to(ROOT), href, 'fichero no existe'))
                continue
            if anchor and destino.suffix == '.html':
                if anchor in anchors_por_fichero.get(destino, set()):
                    continue
                prefijos = prefijos_por_fichero.get(destino, set())
                if any(anchor.startswith(pre) and anchor[len(pre):].isdigit() for pre in prefijos):
                    continue  # id generado en tiempo de ejecucion (ver extraer_prefijos_dinamicos)
                rotos.append((p.relative_to(ROOT), href, f'anchor #{anchor} no existe'))

    print('\n=== 1 · Enlaces internos (href + anchors) ===')
    if rotos:
        print(f'  ❌ {len(rotos)} enlaces rotos:')
        for p, href, motivo in rotos[:50]:
            print(f'     · {p}:  href="{href}"  [{motivo}]')
        if len(rotos) > 50:
            print(f'     · ... y {len(rotos)-50} más')
    else:
        print('  ✅ 0 enlaces rotos')

    errores = len(rotos)
    print('\n=== RESUMEN ===')
    if errores == 0:
        print('✅ Integridad OK')
        return 0
    print(f'❌ {errores} problemas detectados')
    return 1


if __name__ == '__main__':
    sys.exit(main())
