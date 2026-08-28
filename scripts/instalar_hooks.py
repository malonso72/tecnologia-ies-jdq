#!/usr/bin/env python3
"""
TECI II · Instalador de hooks de Git
═════════════════════════════════════
Copia los hooks versionados de scripts/hooks/ a .git/hooks/
para que se ejecuten automáticamente con git push, git commit, etc.

Es seguro ejecutarlo varias veces: sobrescribe los hooks existentes.

Uso:
    python3 scripts/instalar_hooks.py

Para desinstalar (borrar los hooks de .git/hooks/):
    python3 scripts/instalar_hooks.py --desinstalar
"""
import os, sys, shutil

HOOKS_SRC = "scripts/hooks"
HOOKS_DST = ".git/hooks"

def main():
    desinstalar = "--desinstalar" in sys.argv

    if not os.path.isdir(".git"):
        print("✗ Error: este script debe ejecutarse desde la raíz del repo (la carpeta que contiene .git/).")
        sys.exit(1)

    if not os.path.isdir(HOOKS_SRC):
        print(f"✗ Error: no encuentro {HOOKS_SRC}/")
        sys.exit(1)

    os.makedirs(HOOKS_DST, exist_ok=True)
    hooks = [f for f in os.listdir(HOOKS_SRC) if not f.startswith(".")]

    if desinstalar:
        for h in hooks:
            target = os.path.join(HOOKS_DST, h)
            if os.path.exists(target):
                os.remove(target)
                print(f"  ✗ Desinstalado: {target}")
        print("\n✓ Hooks desinstalados. Tu git ya no los ejecutará.")
        return

    for h in hooks:
        src = os.path.join(HOOKS_SRC, h)
        dst = os.path.join(HOOKS_DST, h)
        shutil.copy(src, dst)
        # Hacer ejecutable (sólo aplica en Linux/Mac, en Windows da igual)
        try:
            os.chmod(dst, 0o755)
        except Exception:
            pass
        print(f"  ✓ Instalado: {dst}")

    print(f"""
✓ Hooks instalados correctamente.

A partir de ahora, cada vez que hagas git push (o desde GitHub Desktop),
se ejecutarán las comprobaciones automáticas:

  - pre-push: comprueba que no hay enlaces internos rotos antes de subir.

Si alguna comprobación falla, el push se BLOQUEA y verás un mensaje
explicando qué arreglar. Para saltarte una comprobación de emergencia:

    git push --no-verify

(no recomendado, pero está ahí por si algún día lo necesitas)
""")

if __name__ == "__main__":
    main()
