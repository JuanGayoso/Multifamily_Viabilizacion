# Revisión de pares del artículo v2.0

**Vivienda en renta en Lima: qué tiene que ser cierto para que compita por el suelo**

Fecha: 25 de noviembre de 2026 · Alcance: artículo, memoria de cálculo, modelo en Python, hoja Excel y contratos 01, 02, 07 y 11

## Para qué sirve este documento

Este documento registra la revisión crítica del artículo y del modelo. La revisión se hizo en rondas: en cada una se buscaron errores de matemática, supuestos sesgados hacia la conclusión y afirmaciones sin fuente; se corrigió lo encontrado y se volvió a revisar. El proceso terminó cuando ninguna observación abierta cambiaba la conclusión.

**Criterio de cierre.** El artículo se considera cerrado cuando:

1. toda cifra del texto sale del modelo y coincide con la hoja Excel;
2. todo supuesto tiene una fuente o figura como estimación, con su rango;
3. la conclusión se mantiene en las pruebas de robustez (después de impuestos, por distrito, con salida por unidades); y
4. los contratos estándar usan valores referenciales coherentes con el modelo.

**Escala de gravedad.**
- **Crítica:** cambia la conclusión.
- **Alta:** cambia una cifra relevante o el umbral de viabilidad.
- **Media:** afecta la trazabilidad o la presentación honesta del resultado.
- **Baja:** forma.

## Punto de partida: problemas del artículo v1.0

El artículo v1.0 sostenía que el BTR es viable con ingeniería financiera y sin subsidios. La revisión inicial encontró que esa conclusión no estaba demostrada:

| # | Hallazgo | Gravedad |
|---|---|---|
| 0.1 | No había un modelo de flujo de caja reproducible; las cifras no se podían auditar | Crítica |
| 0.2 | No se comparaba el BTR contra el uso alternativo del suelo (BTS); la viabilidad se juzgaba sin costo de oportunidad del terreno | Crítica |
| 0.3 | El cap rate, el yield y el costo de la deuda no eran coherentes entre sí: el rendimiento sobre costo quedaba por debajo de la tasa de la deuda, y aun así se presentaba el apalancamiento como fuente de valor | Crítica |
| 0.4 | El tratamiento del IGV del alquiler (gravado, con crédito fiscal recuperable solo contra la renta) no estaba cuantificado | Alta |
| 0.5 | Los valores referenciales de los contratos (LTV 65%, DSCR 1.20x, amortización a 25-30 años) no eran compatibles con el NOI del activo | Alta |

Por eso el artículo se rehízo desde cero, con un modelo publicado (`modelo/`), en vez de corregirlo por partes.

## Ronda 1: modelo financiero

| # | Hallazgo | Gravedad | Corrección | Efecto |
|---|---|---|---|---|
| 1.1 | El NOI de la salida usaba solo tres trimestres: el horizonte del BTR terminaba un trimestre antes | Alta | Horizonte de 27 trimestres, que crece con la fecha de salida | Corrige el valor de salida |
| 1.2 | El crédito de construcción del BTR (LTC 65%) no podía ser repagado por el mini-perm, y el modelo escondía un aporte grande de capital al refinanciar | Alta | LTC del BTR de 55%; la brecha se reporta (S/ 619 por m², S/ 3.4 millones) | La brecha queda explícita en el artículo y en el contrato 01 |
| 1.3 | La tasa de descuento de la vara laxa no estaba ligada al cap rate | Alta | *r*<sub>u</sub> = cap + *g* (Gordon), así que la vara se mueve con el cap | Consistencia interna |
| 1.4 | Solo se modelaba la salida en bloque; el BTS se beneficia del precio por unidad | Alta | Salida por venta de unidades a personas naturales (descuento por usado, absorción, comisión) | El BTR sube a 6.4% en el régimen A; sigue bajo el umbral |
| 1.5 | El análisis era solo antes de impuestos | Media | Prueba después del IR (29.5%) | BTS 12.3%; BTR −0.4% a 4.0%; la conclusión no cambia |
| 1.6 | Un solo distrito | Media | Sensibilidad por distrito con rendimientos de Urbania | La conclusión se mantiene en todo el rango de Lima Moderna |
| 1.7 | La exoneración del IGV se modelaba como beneficio puro, ignorando que se pierde el crédito del IGV de obra | Crítica | Regímenes A, B y C separados; B (exonerado) iguala al BTR con la persona natural, no le da ventaja | El régimen B sube la TIR a 2.6%, no al nivel que sugería una lectura ingenua |
| 1.8 | La prima de renta del producto institucional no tiene fuente pública | Media | Se trata como variable de sensibilidad (0% a 30%) y no como supuesto base | **Abierta**: brecha de datos declarada en el artículo |

## Ronda 2: artículo frente al modelo

| # | Hallazgo | Gravedad | Corrección |
|---|---|---|---|
| 2.1 | El texto decía que el crédito fiscal se recupera "en pocos años" | Alta | Se reemplazó por la cifra del modelo: 22% en tres años y ~11 años en total |
| 2.2 | El umbral de viabilidad de la conclusión no coincidía con el mapa | Alta | Se unificó: prima ≥ 20% y cap ≤ 6.0% con régimen B |
| 2.3 | El balloon del mini-perm figuraba como un solo valor | Media | Rango de 89% a 96% según el plazo de amortización |
| 2.4 | Los rendimientos de alquiler por distrito no tenían fuente | Media | Se añadieron los rendimientos de Urbania (5.1% a 5.9%) como fuente 17 |
| 2.5 | Una cifra de ACAFI se citaba como si fuera primaria | Media | Se marcó como fuente secundaria |
| 2.6 | Juicios de valor mezclados con resultados del modelo | Media | Etiqueta "Opinión profesional" donde corresponde |
| 2.7 | Solo se reportaban los umbrales con la vara laxa | Media | Se añadieron los umbrales con la vara estricta |
| 2.8 | El rango de tasas VAC no tenía atribución | Baja | Se atribuyó al reporte del MEF |

## Ronda 3: verificación numérica y contratos

| # | Hallazgo | Gravedad | Corrección |
|---|---|---|---|
| 3.1 | Verificación automática de todas las cifras del artículo y de la memoria contra `resultados.json` | — | Sin diferencias. La hoja Excel reproduce el Python en los siete escenarios de prueba (1,634 fórmulas, 0 errores) |
| 3.2 | La memoria no incluía el escenario "caso favorable" citado en el artículo | Baja | Añadido |
| 3.3 | Ingreso neto del arrendador persona natural mal transcrito en la memoria | Baja | Corregido a S/ 309.1 por m² |
| 3.4 | Contrato 01: LTV máximo de 65%, cuando el DSCR de 1.25x limita el préstamo a un LTV de ~49%; periodo de colocación de 24 meses y amortización a 25-30 años no coherentes con el modelo | Alta | LTV 55%, DSCR 1.25x/1.35x, debt yield mínimo de 9.5% (definición, covenant y condición de desembolso), colocación de 12-18 meses, amortización de 15-20 años, balloon referencial, nota de calibración |
| 3.5 | Contrato 02: faltaban el plazo de tenencia de la FIBRA para el diferimiento, la evidencia de capital comprometido y el riesgo de perder el crédito de IGV si se exonera el alquiler | Alta | Cláusulas 62.4, 62.5 y 63.3; cap pactado de 6.5% con su derivación; base legal actualizada |
| 3.6 | Contrato 07: presentaba el puente como fuente de viabilidad | Media | Nota: solo agrega valor si la TIR del proyecto supera su costo; en el caso base es apalancamiento negativo |
| 3.7 | Contrato 11: rango de gastos (25-35%) por encima de lo que usa el modelo (23.6%) y sin tratamiento del IGV de los gastos | Media | Rango de 22% a 35%, tratamiento del IGV según régimen, cap de 6.5% con su derivación |

## Estado final

**La conclusión es robusta.** En ninguna de las pruebas el BTR alcanza el valor de mercado del suelo en Lima Moderna con el régimen tributario actual. El resultado que se probó y se mantuvo es este:

- **Caso base:** TIR no apalancada de 0.5% frente a un umbral de 9%. El rendimiento sobre costo (5.69%) es menor que el cap de salida (6.50%).
- **Toda la ingeniería financiera junta:** 1.2%.
- **Variables que sí cambian el resultado:** régimen de IGV, cap de salida, prima de renta demostrada y costo del suelo. Con régimen B, prima de 20% y cap de 6.0%, la TIR llega a 10.7%. Con terreno aportado, llega a 15.6%.

**La viabilidad del planteamiento** (lo que el usuario pidió que se alcanzara en el loop) no se logró forzando supuestos. Se logró reformulando la pregunta: el artículo ya no afirma que el BTR es viable en general, sino que delimita con números en qué condiciones lo es. Esa delimitación sí es defendible.

**Observaciones abiertas que no cambian la conclusión:**

| # | Tema | Por qué sigue abierto | Cómo cerrarlo |
|---|---|---|---|
| A1 | Prima de renta del producto institucional | No hay serie pública de rentas de cierre por tipo de arrendador | Rent rolls de operadores; registros del D.Leg. 1177 |
| A2 | Texto final del PL 58-2026 | Proyecto no aprobado | Seguimiento en el Congreso; opinión de tributarista |
| A3 | Requisitos vigentes del D.Leg. 973 | No contrastados con el texto oficial | MEF, ProInversión |
| A4 | Artículo exacto del plazo de tenencia de la FIBRA | No contrastado | Ley 30532 y DS 336-2018-EF en el SPIJ |
| A5 | Tasas del BCRP | BCRPData bloqueó la descarga automática; se usaron como supuestos con fecha | Descarga manual de BCRPData |

**Limitaciones del método.** La revisión la hizo el mismo autor del modelo, en rondas sucesivas. Eso detecta errores de consistencia, pero no reemplaza una revisión independiente. Antes de usar el modelo para una decisión de inversión, un tercero debe revisar la memoria de cálculo y la hoja Excel, y un tributarista debe validar los regímenes de IGV.
