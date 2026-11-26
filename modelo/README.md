# Modelos financieros

- **Artículo 1**, [Vivienda en renta en Lima: dónde y bajo qué condiciones es viable hoy](../articulo/financiamiento-vivienda-en-renta-peru.md): BTS frente a BTR en Lima Moderna. Fórmulas en la [memoria de cálculo](../articulo/memoria-de-calculo.md).
- **Artículo 2**, [¿Puede la vivienda en renta ayudar a cerrar la brecha de vivienda en Lima y Callao?](../articulo/btr-y-brecha-de-vivienda-lima-callao.md): BTR sobre suelo público en derecho de superficie. Fórmulas en la [memoria de cálculo del suelo público](../articulo/memoria-de-calculo-suelo-publico.md).

## Archivos

| Archivo | Qué es |
|---|---|
| `modelo_multifamily.py` | Modelo trimestral: BTS, BTR, regímenes de IGV, mini-perm, escenarios, mapa de viabilidad, distritos y prueba después de impuestos. Los supuestos están en el diccionario `BASE` |
| `resultados.json` | Salida completa del modelo (supuestos, resultados, escenarios y flujos) |
| `salida_consola.txt` | Resumen impreso por el modelo |
| `construir_excel.py` | Genera `memoria-de-calculo.xlsx` con fórmulas que referencian la hoja Supuestos |
| `memoria-de-calculo.xlsx` | El modelo en Excel. Cambie los valores en azul de la hoja Supuestos y el resto se recalcula; la hoja Resumen compara Excel con Python |
| `modelo_suelo_publico.py` | Modelo anual del artículo 2: cascada inversionistas → Estado → excedente, relicitación, escenarios, sensibilidad, plazo mínimo y asequibilidad con bono. Usa los supuestos de `BASE` del modelo 1 |
| `resultados_suelo_publico.json` | Salida del modelo del artículo 2 |
| `construir_excel_suelo_publico.py` | Genera `memoria-suelo-publico.xlsx` |
| `memoria-suelo-publico.xlsx` | Modelo del artículo 2 con fórmulas (régimen B, T1 + T2 ≤ 90 años); la hoja Resumen compara con Python |

## Cómo reproducir

```bash
python3 modelo/modelo_multifamily.py      # escribe resultados.json
python3 modelo/construir_excel.py         # escribe memoria-de-calculo.xlsx
cd modelo && python3 modelo_suelo_publico.py && python3 construir_excel_suelo_publico.py   # artículo 2
```

Requiere Python 3 y `openpyxl`. Abra el Excel en Excel o LibreOffice para que se calculen las fórmulas.

## Límites

Antes de impuestos salvo la hoja DespuesIR; un solo producto típico (5,500 m² vendibles); tasas del BCRP y la SBS tomadas como supuestos con fecha. Ver la sección de limitaciones de la memoria de cálculo.
