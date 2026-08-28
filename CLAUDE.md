# CLAUDE.md — Hub Tecnología (portal) · IES Jiménez de Quesada
## Lee esto al inicio de cada sesión antes de tocar ningún archivo.

---

## PROYECTO

Sitio web estático de **Departamento de Tecnología · portal de acceso a las 5 webs**. Profesor: Manuel Alonso Herrera. Centro: IES Jiménez de Quesada, Santa Fe (Granada). Curso activo: **2026-27**.

Despliegue: Cloudflare Workers Static Assets vía GitHub (`git push` → producción automática en tecnologia-ies-jdq.malonso72.workers.dev).

Para el mapa de carpetas y comandos de despliegue, ver `README.md` en la raíz de este repo — ya está bien documentado y no se duplica aquí.

---

## ESTADO DE ESTE FICHERO

Este CLAUDE.md se creó en agosto de 2026 al portar la infraestructura técnica de verificación desde el sitio hermano **teci2-ies-jdq** (Bachillerato), que lleva dos meses de trabajo iterativo y tiene una filosofía editorial mucho más desarrollada. Este fichero es un punto de partida deliberadamente ligero: documenta la herramienta nueva y deja que la filosofía editorial (qué se amplía, qué no, criterios de auditoría) se vaya fijando en próximas sesiones con Manuel, igual que ocurrió en teci2. No asumas que las convenciones de teci2 aplican aquí sin preguntar — este sitio puede seguir en fase de crecimiento de contenido, a diferencia de teci2.

---

## HERRAMIENTAS DE VERIFICACIÓN (nuevo, ago-2026)

Antes de este cambio, este repo solo tenía scripts de higiene de assets (imágenes huérfanas, archivos pesados) y `comprobar_enlaces.py` (href/src rotos). Se han añadido dos verificadores más, calcados de los usados en teci2:

- `scripts/verificar_html.py` — comprueba que todos los `.html` del sitio parsean sin errores (etiquetas mal formadas, comillas sin cerrar, etc.). Ejecutar: `python3 scripts/verificar_html.py`.
- `scripts/verificar_enlaces.py` — comprueba enlaces internos rotos y anchors `#id` que no existen en el fichero destino. Ejecutar: `python3 scripts/verificar_enlaces.py`.

**Hook de pre-push instalado.** `scripts/hooks/pre-push` ejecuta automáticamente `verificar_html.py`, `verificar_enlaces.py` y `comprobar_enlaces.py` antes de cada `git push`, y bloquea el push si algo falla. Ya está instalado en `.git/hooks/` de este repo (lo hizo esta sesión ejecutando `python3 scripts/instalar_hooks.py`). Si algún día hace falta reinstalarlo (p. ej. tras clonar el repo en otro equipo), basta con volver a ejecutar ese comando. Para saltárselo puntualmente: `git push --no-verify`.

**Resultado de la primera pasada (ago-2026):** ver el informe que te dio Claude en el chat — puede haber incidencias preexistentes (anchors rotos, etc.) que no se han corregido en esta sesión porque el objetivo era solo instalar la herramienta, no auditar contenido. Cuando le toque el turno de trabajo profundo a este sitio, esa lista es un buen punto de partida.

---

## CONVENCIONES CONOCIDAS

- HTML + CSS + JS vanilla, sin frameworks (ver README.md → sección Convenciones si existe).
- `_soluciones/` es privada y no debe enlazarse desde páginas visibles al alumnado (lo comprueba `verificar_enlaces.py`).
- `documentacion/` es privada (PROGRAMACION, DECISIONES, PENDIENTES) — no se despliega públicamente salvo que el `.assetsignore` diga lo contrario; revisa `.assetsignore` antes de asumirlo.
