# Modelo financiero: BTS frente a BTR en Lima Moderna

Este modelo calcula las cifras del artículo [Vivienda en renta en Lima: qué tiene que ser cierto para que compita por el suelo](../articulo/financiamiento-vivienda-en-renta-peru.md). Las fórmulas y los supuestos están en la [memoria de cálculo](../articulo/memoria-de-calculo.md).

## Archivos

| Archivo | Qué es |
|---|---|
| `modelo_multifamily.py` | Modelo trimestral: BTS, BTR, regímenes de IGV, mini-perm, escenarios, mapa de viabilidad, distritos y prueba después de impuestos. Los supuestos están en el diccionario `BASE` |
| `resultados.json` | Salida completa del modelo (supuestos, resultados, escenarios y flujos) |
| `salida_consola.txt` | Resumen impreso por el modelo |
| `construir_excel.py` | Genera `memoria-de-calculo.xlsx` con fórmulas que referencian la hoja Supuestos |
| `memoria-de-calculo.xlsx` | El modelo en Excel. Cambie los valores en azul de la hoja Supuestos y el resto se recalcula; la hoja Resumen compara Excel con Python |

## Cómo reproducir

```bash
python3 modelo/modelo_multifamily.py      # escribe resultados.json
python3 modelo/construir_excel.py         # escribe memoria-de-calculo.xlsx
```

Requiere Python 3 y `openpyxl`. Abra el Excel en Excel o LibreOffice para que se calculen las fórmulas.

## Límites

Antes de impuestos salvo la hoja DespuesIR; un solo producto típico (5,500 m² vendibles); tasas del BCRP y la SBS tomadas como supuestos con fecha. Ver la sección de limitaciones de la memoria de cálculo.
