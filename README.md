# Hub Tecnología · IES Jiménez de Quesada

**Departamento de Tecnología · Curso 2026-27**
Profesor: Manuel Alonso Herrera · Santa Fe (Granada)

Página índice única que centraliza el acceso a las 5 webs de
asignaturas del departamento. Sitio estático servido por Cloudflare
Workers Static Assets en
[tecnologia-ies-jdq.malonso72.workers.dev](https://tecnologia-ies-jdq.malonso72.workers.dev).

## Webs enlazadas

| Curso         | Asignatura                       | URL                                            |
|---------------|----------------------------------|------------------------------------------------|
| 1º ESO        | Computación y Robótica (CyR)     | cyr1-ies-jdq.malonso72.workers.dev             |
| 2º ESO        | Tecnología y Digitalización (TyD)| tyd2-ies-jdq.malonso72.workers.dev             |
| 3º ESO        | Tecnología y Digitalización (TyD)| tyd3-ies-jdq.malonso72.workers.dev             |
| 4º ESO        | Tecnología (Tec)                 | tec4-ies-jdq.malonso72.workers.dev             |
| 1º + 2º Bach. | Tecnología e Ingeniería (TECI)   | teci2-ies-jdq.malonso72.workers.dev            |

## Estructura

```
tecnologia-ies-jdq/
├── index.html                  Hub con las 5 tarjetas
├── img/                        fachada + logo
├── assets/css/                 common, hub
├── documentacion/              Privado: pendientes y decisiones
└── scripts/                    Auditoría y mantenimiento
```

## Despliegue

```bash
# Test local
python3 -m http.server 8000

# Validación pre-push
python3 scripts/comprobar_enlaces.py
python3 scripts/auditar_imagenes_huerfanas.py
python3 scripts/auditar_archivos_pesados.py --umbral 300

# Deploy automático: push a main → Cloudflare deploya en 1-2 min
```

## Convenciones

- HTML + CSS + JS vanilla. Sin frameworks.
- Tipografía: Barlow + Barlow Condensed.
- Paleta principal: azul institucional (`#1B4F8A`) sobre fondo neutro.
- Cada tarjeta de curso conserva el color de su asignatura para que
  el alumno reconozca a primera vista cuál es la suya.
- Accesibilidad: skip-link, focus-visible, alt en imágenes, contraste AA.
