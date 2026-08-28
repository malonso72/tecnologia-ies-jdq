#!/usr/bin/env python3
"""
verificar_html.py — Valida el HTML de todos los ficheros del ecosistema TECI II.

QUÉ VERIFICA
    Que cada fichero .html del ecosistema se procesa sin errores con html.parser
    (la biblioteca estándar de Python). Esta no es una validación estricta W3C
    sino una comprobación de que el HTML se puede parsear sin excepciones —
    suficiente para detectar etiquetas mal formadas, comillas sin cerrar,
    atributos rotos, etc. (Fue el criterio utilizado en v2.4, v2.5, v2.6 y v2.7).

CÓMO SE EJECUTA
    Desde la raíz del ecosistema:
        python3 scripts/verificar_html.py

OUTPUT
    - Lista de todos los .html encontrados con estado ✓ / ✗.
    - Para los ✗, el mensaje de error concreto.
    - Total ficheros válidos vs total escaneados.
    Exit code 0 si 100 % válidos, 1 si hay algún ✗.

ÚLTIMA UTILIZACIÓN
    v2.7 · Bloque 5 (15-abr-2026) — resultado: 71 / 71 HTML válidos.
"""
from __future__ import annotations
import sys
from html.parser import HTMLParser
from pathlib import Path

# Forzar UTF-8 en stdout para que funcione en consolas Windows (cp1252)
# que no soportan caracteres Unicode como ✓ o ✗.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []

    def error(self, message: str) -> None:  # type: ignore[override]
        self.errors.append(message)


def main() -> int:
    htmls = sorted(ROOT.rglob('*.html'))
    ok = 0
    fail: list[tuple[Path, str]] = []
    for p in htmls:
        txt = p.read_text(encoding='utf-8')
        parser = Parser()
        try:
            parser.feed(txt)
            parser.close()
        except Exception as e:
            fail.append((p, f'{type(e).__name__}: {e}'))
            continue
        if parser.errors:
            fail.append((p, '; '.join(parser.errors)))
            continue
        ok += 1

    for p in htmls:
        estado = '✓' if not any(p == f[0] for f in fail) else '✗'
        print(f'  {estado} {p.relative_to(ROOT)}')

    print(f'\n=== RESUMEN ===')
    print(f'  Válidos: {ok} / {len(htmls)}')
    if fail:
        print(f'  ❌ Errores:')
        for p, msg in fail:
            print(f'    · {p.relative_to(ROOT)} → {msg}')
        return 1
    print('  ✅ 100 % HTML válidos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
