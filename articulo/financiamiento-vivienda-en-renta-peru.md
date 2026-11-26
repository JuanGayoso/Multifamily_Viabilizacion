# Vivienda en renta en Lima: qué tiene que ser cierto para que compita por el suelo

**Neutralidad tributaria, costo de capital e ingeniería financiera, medidos con datos de mercado**

Por: Juan Germán Gayoso Arnillas · Versión 2.0 · 25 de noviembre de 2026

Modelo reproducible: [`modelo/modelo_multifamily.py`](../modelo/modelo_multifamily.py) · Hoja de cálculo con fórmulas: [`modelo/memoria-de-calculo.xlsx`](../modelo/memoria-de-calculo.xlsx) · Memoria de cálculo: [`memoria-de-calculo.md`](memoria-de-calculo.md) · Revisión de pares: [`revision-de-pares.md`](revision-de-pares.md)

---

## Conclusión

Con precios, alquileres, tasas y normas vigentes a noviembre de 2026, un edificio de vivienda para renta (*build-to-rent*, BTR) en Lima Moderna **no puede pagar el precio de mercado del terreno**, que fija el proyecto de vivienda para venta (*build-to-sell*, BTS). Hay que distinguir dos cosas:

- **La ingeniería financiera es necesaria para que un proyecto sea financiable, pero no basta para hacerlo viable.** Nota puente de terreno, mini-perm, financiamiento verde y recuperación anticipada del IGV, todas juntas, suben la TIR no apalancada del caso base de 0.5% a 1.2%. El umbral exigible es 9%.
- **Cuatro variables deciden la viabilidad:**
  1. el régimen de IGV del alquiler;
  2. el cap rate al que compra el inversionista institucional;
  3. la prima de renta que el producto logra demostrar;
  4. el costo del suelo.

  El BTR compite por suelo de mercado solo cuando se combinan neutralidad del IGV (alquiler exonerado, como el de la persona natural), una prima de renta de al menos 20% bien sustentada y un cap de salida de 6.0% o menos. Fuera de eso, es viable en nichos donde el suelo no se paga a precio BTS: aporte de terreno por un propietario patrimonial, joint ventures o tierra que ya está en balance.

En el caso base el edificio vale menos de lo que cuesta. Su rendimiento sobre costo (5.69%) está por debajo del cap rate de salida (6.50%). Ninguna estructura de deuda corrige un margen de desarrollo negativo: con deuda más cara que el rendimiento del activo, el apalancamiento empeora la TIR del capital.

La tesis de la neutralidad competitiva sigue en pie: el Estado no debe darle al multifamily ventajas que el arrendador persona natural no tiene. El modelo muestra que hoy la cancha está inclinada *en contra* del multifamily, sobre todo por el IGV, y que nivelarla es condición necesaria pero no suficiente.

---

## 1. La pregunta correcta: quién puede pagar el terreno

Un proyecto de vivienda en renta no compite contra "nada", sino contra el mejor uso alternativo del mismo terreno. En Lima Moderna ese uso es el edificio para venta, cuyos departamentos compran familias y pequeños inversionistas que luego los alquilan. El terreno se lo lleva quien puede pagar más por él. Por eso el criterio de viabilidad de este artículo es el **valor residual del suelo**: cuánto puede pagar cada modelo por el terreno y aun así darle a su capital la rentabilidad que exige.

- **BTS:** el residual se calcula con la TIR que exige el promotor (20% en soles, rango de mercado de 18% a 25%). Ese residual es el **precio de mercado del terreno**.
- **BTR:** se calcula con dos varas.
  - **Vara laxa:** TIR no apalancada igual al cap rate más el crecimiento de la renta (9.0%). Es el retorno de un activo ya estabilizado; no premia el riesgo de construcción ni de colocación, así que es un **límite superior**.
  - **Vara estricta:** TIR del capital de 14% (rango de 12% a 16%).

Si el BTR no alcanza el residual del BTS ni siquiera con la vara laxa, no puede comprar terreno de mercado.

## 2. Los datos de partida

**Tabla 1. Datos de mercado** (hechos verificables, salvo donde se indica).

| Variable | Valor | Fecha | Fuente |
|---|---|---|---|
| Precio de oferta de departamentos, Lima Moderna (6 distritos) | US$ 1,868 por m² | IV trim. 2025 | BCRP, Nota de Estudios 16-2026 (medianas Urbania) |
| Alquiler de oferta, Lima Moderna (promedio simple de los 6 distritos) | US$ 119.3 por m² al año | IV trim. 2025 | BCRP, Nota de Estudios 16-2026 |
| Relación precio/alquiler (PER) | 15.6 en Lima Moderna; 16.3 en 12 distritos; 16.1 al II trim. 2026 | 2025-2026 | BCRP |
| Rentabilidad bruta del alquiler, Lima | 5.27% (oct-2025); 5.44% (2026) | 2025-2026 | Urbania Index; Gestión |
| Tasa de referencia BCRP | 4.50% (subió desde 4.25%) | 12-nov-2026 | BCRP; Andina |
| Inflación de Lima, 12 meses | 5.3% | oct-2026 | BCRP; Panamericana |
| Expectativa de inflación a 12 meses | 3.1% | nov-2026 | BBVA Research |
| Bono soberano SB12AGO34 (≈8 años) | 6.35% | 30-set-2026 | MEF, reporte diario |
| Bono soberano SB12AGO37 | ≈7.0% | 30-set-2026 | MEF, reporte diario |
| Tasa hipotecaria promedio en soles | 7.5%-7.8% | ene-ago 2026 | BCRP vía Andina; SBS |
| Tipo de cambio | S/ 3.40-3.41 por US$ | nov-2026 | BCRP |
| FIBRA Prime: ocupación y activos | 95.3%; US$ 274.6 millones; 40 inmuebles (sin vivienda) | II trim. 2026 | Revista Economía; Infomercado |
| Renta residencial directa en Chile | 3.5%-4.5% neto en UF (real) | jul-2026 | ACAFI, citada por Mercado Libre Chile (fuente secundaria) |

Dos precisiones sobre estos datos:

- **Precio y alquiler son de oferta, no de cierre.** El modelo les aplica el mismo descuento de 4% para no sesgar la comparación.
- **El 6.4% de rentabilidad bruta que sale del BCRP para Lima Moderna es más alto que lo que reporta Urbania.** Urbania da 5.3%-5.4% para Lima, y por distrito de Lima Moderna, entre 5.1% (Magdalena) y 5.9% (Pueblo Libre, San Miguel) a mayo de 2026. Usar el dato del BCRP *favorece* al modelo de renta. Es una elección deliberada: si el BTR no cierra con el dato favorable, tampoco cierra con el otro.

## 3. El modelo

Se modela un mismo edificio de 5,500 m² vendibles (unos 100 departamentos de 55 m²) desarrollado de dos maneras. Los flujos son trimestrales, en soles nominales; el IGV se trata como flujo de caja, con débito, crédito y saldo a favor. El análisis principal es antes de Impuesto a la Renta, y en la sección 9 se contrasta después de IR.

**Tabla 2. Supuestos principales** (H = hecho con fuente; E = estimación; O = opinión profesional).

| Supuesto | Base | Tipo | Sustento |
|---|---|---|---|
| Precio de cierre BTS | S/ 6,115 por m² (con IGV) | H+E | US$ 1,868 × 3.41 × (1 − 4%) |
| Renta de cierre BTR | S/ 391 por m² al año | H+E | US$ 119.3 × 3.41 × (1 − 4%) |
| Crecimiento de precios y rentas | 2.5% anual | E | Inflación de largo plazo, sin crecimiento real |
| Costo directo | S/ 2,665 por m² vendible (sin IGV) | E | S/ 2,050 por m² techado × 1.30 |
| Indirectos / contingencia | 12% / 5% del costo directo | E | Práctica de mercado |
| Gastos de venta BTS | 4% de la venta neta | E | Práctica de mercado |
| Amoblado y amenities BTR | S/ 150 por m² | E | |
| Calendario | Licencias t1-t3; obra t4-t10; entrega t11 | E | 21 meses de obra |
| Ventas BTS | t3-t14; 20% de inicial y saldo a la entrega | E | |
| Ocupación BTR | 25%, 50%, 75% y 90% en t11-t14; 95% estabilizada | E | Vacancia estructural de 5% |
| Opex del propietario | S/ 72 por m² al año (≈21% del ingreso neto) + reserva de 2% | E | Desglose en la memoria |
| Crédito de obra | 10.0% TEA; 65% LTC en BTS y 55% en BTR | E | Soberano + ≈370 pb |
| Mini-perm | 9.0% TEA; amortización a 20 años; DSCR 1.25x; LTV 60%; debt yield 9.5% | E | |
| Cap rate de salida | 6.50% sobre NOI | E/O | Soberano ≈6.3% + prima ≈2.7% − crecimiento 2.5% |
| Venta BTR | t22 (dos años después de estabilizar) | E | |
| TIR exigida al capital | BTS 20%; BTR 14% | O | |

**Cómo se llega al cap de 6.5%.** Por el modelo de Gordon, el cap es el retorno exigido menos el crecimiento: (6.3% + 2.7%) − 2.5% = 6.5%. En términos reales equivale a cerca de 4%, similar a la renta residencial neta de Chile (3.5%-4.5% en UF) pese a que la tasa real soberana del Perú es más alta (los bonos VAC de 2035-2040 rendían entre 3.8% y 4.3% reales en septiembre de 2026, según el reporte diario del MEF). Pedir un cap menor en Lima supone un mercado institucional más profundo que el chileno, y ese mercado no existe todavía.

## 4. Resultado base

**Tabla 3. Resultado base, terreno a precio de mercado** (soles; valores por m² vendible).

| Indicador | BTS | BTR |
|---|---|---|
| Terreno residual a la TIR exigida | **S/ 1,015 por m²** (15.7% de las ventas) | −S/ 452 por m² (capital al 14%); −S/ 195 por m² (no apalancado al 9%) |
| Costo de desarrollo sin terreno | S/ 3,280 por m² + S/ 237 de ventas | S/ 3,463 por m² + S/ 611 de IGV (crédito) |
| NOI estabilizado | — | S/ 256 por m² al año |
| Rendimiento sobre costo (YoC) | — | 5.69% |
| Valor a la salida (NOI/cap) | — | S/ 4,132 por m² frente a S/ 4,508 de costo con terreno |
| TIR no apalancada | 17.2% | **0.5%** |
| TIR del capital | 20.0% | **−5.4%** |
| Mini-perm | — | S/ 1,935 por m²; LTV 49%; DSCR mínimo 1.24x; restricción: DSCR |

**Calibración.** El residual del BTS (S/ 1,015 por m² vendible, unos US$ 300) equivale al 15.7% de las ventas, con un margen de 22% sobre ventas. Ambas cifras caen dentro de los rangos que se ven en la práctica de Lima Moderna: 12%-20% de incidencia y 15%-25% de margen. La incidencia es opinión profesional y debe contrastarse con transacciones (ver "Datos a verificar").

### 4.1 De la renta al NOI: dónde se va el ingreso

**Tabla 4. Cascada del ingreso BTR, régimen tributario vigente** (S/ por m² al año, estabilizado, t15-t18).

| Concepto | S/ por m² | % de la renta potencial |
|---|---|---|
| Renta potencial a precio de mercado | 432 | 100% |
| (−) Vacancia (5%) e incobrables (1%) | −26 | −6% |
| Renta cobrada al inquilino | 407 | 94% |
| (−) IGV absorbido (18% dentro del precio de mercado) | −62 | −14% |
| Ingreso neto del propietario | 345 | 80% |
| (−) Opex del propietario | −81 | −19% |
| (−) Reserva de reposición | −7 | −2% |
| **NOI** | **256** | **59%** |

La partida más grande después del opex es el IGV. El inquilino compara el precio del multifamily con el de un departamento que alquila una persona natural, que no cobra IGV. Para competir, el operador tiene que absorber el impuesto dentro del precio de mercado. Trasladarlo (cobrar 18% más) equivale a lo mismo, con más vacancia.

## 5. Por qué la persona natural paga más que el institucional

El precio del departamento lo fija un comprador que exige poco. Una persona natural que compra en Lima Moderna para alquilar obtiene:

**Tabla 5. Rendimiento del arrendador persona natural** (por m², supuestos en la hoja "Individual").

| Indicador | Valor |
|---|---|
| Rendimiento bruto (renta / precio con IGV) | 6.39% |
| Rendimiento neto de vacancia (8%), corretaje, predial, mantenimiento vacío e IR (5% del bruto) | **4.98%** |
| TIR a 10 años con apreciación de 2.5% anual | **7.1%** |

El institucional exige 9.0% sin deuda (cap de 6.5% + 2.5%). La distancia, de unos 190 pb de retorno exigido, es el problema de fondo: **la vivienda se valoriza en el mercado como depósito de valor familiar, no como activo de renta institucional**. El BTS vende a ese comprador y traslada al terreno el bajo retorno que este exige. El BTR, que vende a un institucional, no puede hacerlo.

En nuestra opinión profesional, esa brecha no es una "falla de mercado" que se cierre con un subsidio. Refleja preferencias (el valor de ser propietario, la falta de alternativas de ahorro) y diferencias tributarias (sección 6). La política pública puede corregir lo segundo; lo primero, no le corresponde.

## 6. La cancha tributaria: dónde está inclinada y cuánto cuesta nivelarla

La comparación relevante es entre la empresa que alquila y la persona natural que alquila.

**Tabla 6. Tratamiento tributario comparado** (normas vigentes; ver [validación normativa](validacion-normativa.md)).

| Concepto | Persona natural | Empresa (multifamily) |
|---|---|---|
| IGV sobre el alquiler | No gravado (renta de primera categoría) | Gravado con 18% (TUO Ley del IGV) |
| IGV de la construcción | Pagado una vez, dentro del precio (primera venta: base sin terreno, ≈9% efectivo) | Crédito fiscal que se recupera solo contra el IGV de los alquileres: en el caso base se recupera 22% en los primeros tres años de operación y tomaría unos 11 años recuperarlo todo |
| Impuesto a la Renta | 6.25% sobre el 80% de la renta = 5% del bruto (art. 52-A LIR) | 29.5% sobre la utilidad, más 5% al distribuir; depreciación de 5% anual |
| Impuesto predial | Tramos bajos (0.2% hasta 15 UIT de autoavalúo) | Edificio completo en el tramo de 1.0% |
| Vehículo de salida (FIBRA, Ley 30532) | — | Retención de 5% para personas naturales con menos de 20% de los certificados: neutral frente a la persona natural |

Tres regímenes de IGV para el alquiler de vivienda por empresas, medidos en el modelo:

**Tabla 7. Efecto del régimen de IGV en el BTR** (terreno a precio de mercado).

| Régimen | YoC | TIR no apalancada | ¿Neutral frente a la persona natural? |
|---|---|---|---|
| A. Vigente: alquiler gravado, IGV absorbido | 5.69% | 0.5% | No: castiga al multifamily |
| A + recuperación anticipada del IGV de obra (D.Leg. 973) | 5.69% | 1.2% | Corrige el calendario, no la carga |
| B. Alquiler exonerado, sin crédito fiscal (la lógica del PL 58-2026) | 6.00% | 2.6% | **Sí**: el IGV de la obra queda como costo, igual que para la persona natural |
| C. Tasa 0% con devolución del IGV de obra (hipotético) | 7.04% | 6.6% | No: le da al multifamily una ventaja que la persona natural no tiene |

El hallazgo menos intuitivo es que **la exoneración no es gratuita para el operador**. Al exonerar el alquiler se pierde el crédito fiscal de la obra, que pasa a ser costo. Aun así, el régimen B mejora el resultado frente al A (YoC de 6.00% contra 5.69%), porque el IGV que se deja de absorber sobre las rentas pesa más que el crédito que se pierde. Por eso el régimen B es el que replica la situación de la persona natural, y el que este artículo defiende: **nivela sin inclinar**. El régimen C (tasa cero) inclinaría la cancha a favor del multifamily y tendría costo fiscal. No se recomienda.

Estado normativo, a verificar al decidir:

- El Proyecto de Ley 58-2026 propone exonerar del IGV el arrendamiento de vivienda con vigencia de seis meses o más a personas naturales, en proyectos destinados exclusivamente a vivienda, y amplía el Bono de Arrendamiento (Ley 30952).
- Es un proyecto, no una ley. Su texto final puede variar, y el tratamiento del crédito fiscal debe verificarse con un tributarista.
- El D.Leg. 973 exige un contrato de inversión con el Estado, una inversión mínima de US$ 5 millones y una etapa preproductiva de al menos dos años. Un edificio de 100 unidades está en el límite.

## 7. Lo que la ingeniería financiera sí hace, y lo que no

**Tabla 8. Efecto de cada palanca financiera** (régimen A, terreno a precio de mercado).

| Palanca | TIR no apalancada | TIR del capital | Lectura |
|---|---|---|---|
| Caso base (crédito de obra + mini-perm) | 0.5% | −5.4% | |
| + Nota puente de terreno (45% al 12%) | 0.5% | −6.0% | Con TIR baja, deuda al 12% resta |
| Sin mini-perm (el capital cancela la obra en t14) | 0.5% | −2.0% | **La deuda destruye valor** cuando el activo rinde menos que ella |
| Mini-perm solo intereses | 0.5% | −6.7% | Más deuda, peor resultado |
| + Financiamiento verde (−75 pb; +1% de costo) | 0.4% | −5.4% | Neutro |
| + Construcción industrializada (−5% de costo directo) | 0.7% | −4.9% | Marginal |
| + Recuperación anticipada del IGV | 1.2% | −5.0% | La palanca individual más útil |
| Todas las palancas juntas | 1.2% | −5.0% | Insuficiente: el umbral es 9% / 14% |

Tres lecciones:

1. **Apalancamiento negativo real.** Con un YoC de 5.7%-6.4% y deuda a 9%-10%, cada sol prestado reduce la TIR del capital. La deuda sirve para un activo que ya crea valor; no lo crea.
2. **El mini-perm lo limita el DSCR, no el LTV.** Con NOI de S/ 256 por m², tasa de 9% y amortización a 20 años (constante anual de 10.6%), un DSCR de 1.25x permite prestar solo 49% del valor. Un crédito de obra dimensionado a 55% del costo deja un **hueco de refinanciamiento de S/ 619 por m²** (S/ 3.4 millones en el proyecto), que debe cubrir el capital. Con amortización a 25-30 años y plazo de 5-7 años, el saldo final sería de 89% a 96%: un riesgo de refinanciamiento que el contrato debe reconocer, no esconder.
3. **La nota puente de terreno solo conviene si el proyecto rinde más que ella.** Es una herramienta de liquidez, no de valor.

La ingeniería financiera importa por otra razón: **hace financiable un proyecto que ya es viable**. Los contratos estándar del repositorio (mini-perm, compraventa futura, fideicomiso, acuerdo directo, tasación) bajan costos de transacción, ordenan riesgos y permiten que bancos, aseguradoras y FIBRA participen. Ese valor no aparece en una TIR, pero es real.

## 8. Qué tiene que ser cierto: el mapa de viabilidad

**Tabla 9. Ratio entre el terreno que puede pagar el BTR (vara laxa) y el precio de mercado** (≥ 1.00: el BTR compite por el suelo).

| Prima de renta | Régimen | Cap 5.50% | Cap 6.00% | Cap 6.50% | Cap 7.00% | Cap 7.50% |
|---|---|---|---|---|---|---|
| 0% | A (vigente) | 0.38 | 0.07 | −0.19 | −0.41 | −0.60 |
| 0% | B (exonerado) | 0.74 | 0.38 | 0.07 | −0.19 | −0.41 |
| 10% | A | 0.84 | 0.49 | 0.19 | −0.06 | −0.27 |
| 10% | B | **1.29** | 0.87 | 0.52 | 0.22 | −0.03 |
| 20% | A | **1.30** | 0.91 | 0.57 | 0.29 | 0.05 |
| 20% | B | **1.83** | **1.36** | 0.97 | 0.63 | 0.35 |
| 30% | A | **1.77** | **1.32** | 0.96 | 0.64 | 0.38 |
| 30% | B | **2.37** | **1.85** | **1.41** | **1.04** | 0.73 |

Cómo leer el mapa:

- **Sin prima de renta, ninguna combinación alcanza el precio de mercado del terreno,** ni siquiera con el alquiler exonerado y un cap de 5.5%.
- **Con el IGV neutral (régimen B), hacen falta una prima de 20% y un cap de 6.0%,** o una prima de 10% con un cap de 5.5%. Con la vara estricta (capital al 14%) se necesita aún más: una prima de 20% con un cap de 5.5%, o una prima de 30% con un cap de 6.0%.
- **¿Qué significa "prima de renta"?** Es lo que el edificio institucional cobra por m² por encima del promedio distrital: producto nuevo, unidades pequeñas, amoblado, servicios y gestión profesional, neto del sobreprecio que ese mismo producto tendría en venta. El comprador BTS también puede construir unidades pequeñas y venderlas más caras.
- **Lo que se puede afirmar.** No hay una serie pública que mida esa prima en Lima. Es el dato más importante por levantar (sección 11). Los avisos de renta son mayormente de unidades usadas y los de venta, de proyectos nuevos, lo que sugiere una prima por producto nuevo de algunos puntos. Una prima de 20% o más debe demostrarse con contratos firmados, no suponerse.

**Tabla 10. Casos de nicho y alternativas de salida.**

| Caso | YoC | TIR no apalancada | TIR del capital | Lectura |
|---|---|---|---|---|
| B + prima 10% + cap 6.0% + terreno al 50% del mercado (aporte, joint venture) | 7.55% | 11.1% | 11.8% | Viable con la vara laxa, no con la estricta |
| Ídem sin mini-perm | 7.55% | 11.1% | 11.2% | Con un activo que crea valor, la deuda suma poco |
| A + prima 10% + cap 6.0% + terreno al 50% | 7.28% | 8.4% | 7.1% | No alcanza con el IGV vigente |
| B + prima 10% + cap 6.0% + terreno aportado sin costo | 8.51% | 15.6% | 21.2% | El propietario del suelo que quiere renta es el socio natural |
| B + prima 20% + cap 6.0% + terreno a mercado | 7.55% | 10.7% | 11.0% | Viable con la vara laxa |
| A con salida por venta de unidades a personas naturales | 5.69% | 6.4% | 4.4% | Captura la brecha de la sección 5, pero es un BTS diferido |
| A con tenencia de 10 años | 5.69% | 5.1% | 2.9% | El tiempo diluye el arrastre del crédito fiscal, no la brecha |
| B con tenencia de 10 años | 6.00% | 6.2% | 4.4% | |

**Tabla 11. Por distrito** (precio y alquiler del BCRP para cada distrito; mismos costos).

| Distrito | PER | TIR no apalancada A / B | Ratio de terreno A / B |
|---|---|---|---|
| Surquillo | 14.4 | 2.9% / 5.2% | 0.09 / 0.41 |
| Lince | 14.9 | 2.6% / 4.9% | 0.18 / 0.46 |
| Pueblo Libre | 14.9 | 1.0% / 3.0% | −0.47 / −0.13 |
| Jesús María | 16.7 | −0.1% / 2.0% | −0.01 / 0.20 |
| Magdalena | 16.2 | −0.5% / 1.5% | −0.29 / −0.05 |
| San Miguel | 17.0 | −3.3% / −1.7% | −1.21 / −0.97 |

Los distritos con PER más bajo (Surquillo, Lince) son los menos desfavorables, pero ninguno cierra sin prima ni cap institucional. Los distritos de Lima Top tienen PER más alto (Surco 19.8, San Borja 18.1), lo que agrava el problema.

## 9. Robustez del resultado

- **Después de IR (29.5%).** Con terreno de mercado, la TIR no apalancada después de impuestos es 12.3% en BTS frente a −0.4% en BTR (régimen A), 1.8% (régimen B) y 4.0% (A con venta por unidades). La depreciación y el diferimiento ayudan al BTR, pero no cambian la conclusión.
- **Supuestos adversos al BTS.** Si el precio de venta baja 5%, el terreno de mercado cae a S/ 833 por m². Si las ventas tardan 16 trimestres, a S/ 847. Si el costo directo sube 10%, a S/ 752. Aun con S/ 750 por m², el BTR del caso base tiene una TIR no apalancada cercana a 2%.
- **Supuestos favorables al BTR ya incluidos.** Rentabilidad bruta del BCRP (6.4%) en lugar de la de Urbania (5.3%-5.4%); el IGV no recuperado del BTS se trata como pérdida; el crédito fiscal del BTR se transfiere al comprador con solo 25% de descuento.
- **Sensibilidad operativa.** Una vacancia de 8% resta 1.0 punto de TIR no apalancada y un opex 20% más alto, 1.5 puntos. Un cap de 7.0% la lleva a −1.0%.

## 10. Recomendaciones

**Para promotores e inversionistas**

1. **No compren terreno a precio BTS para hacer BTR genérico.** Busquen suelo que no compita con el BTS: aporte de propietarios patrimoniales a cambio de renta (contrato de asociación o fideicomiso con participación en el NOI), tierra en balance de retailers, universidades, clínicas o instituciones, y lotes con baja absorción para venta.
2. **Diseñen el producto para la prima, y pruébenla.** Unidades pequeñas, amobladas, con servicios. Antes de comprometer capital, levanten comparables de renta firmada (no de oferta) por tipología.
3. **Usen deuda solo cuando el YoC supere su costo.** Dimensionen el crédito de obra a la toma del mini-perm (LTV de 45%-50% por DSCR) y planifiquen el capital del hueco de refinanciamiento.

**Para FIBRA, AFP y aseguradoras**

4. Un cap institucional de 6.0% en vivienda requiere historia de desempeño. Pidan rent rolls estandarizados (contrato 04) y financien plataformas, no edificios sueltos. La restricción de cuatro años para transferir inmuebles adquiridos o construidos por una FIBRA debe reflejarse en la compraventa futura (contrato 02).

**Para el Estado**

5. **Neutralidad del IGV, no ventaja.** Exonerar el alquiler de vivienda por empresas, con el crédito fiscal de obra como costo (régimen B), replica la situación de la persona natural. Una tasa cero con devolución no se justifica.
6. **Información.** Una serie pública de rentas de cierre, vacancia y morosidad (BCRP/SBS a partir de los registros del RAV y del FUA del D.Leg. 1177) reduciría la prima de riesgo más que cualquier incentivo.
7. **Predial y licencias.** Revisen si la progresividad del predial por propietario debe aplicarse por unidad de vivienda en edificios de renta. Cumplir los plazos de la Ley 29090 baja el costo de capital de la fase de licencias.
8. **Vivienda social en arrendamiento.** La Ley 32379 (VIS) y su reglamento en consulta (RM 269-2026-VIVIENDA) son el lugar para un subsidio *explícito* a la demanda (Bono de Arrendamiento). No corresponde un subsidio al vehículo.

## 11. Riesgos y límites del análisis

- **Los datos de precio y renta son de oferta.** Una base de transacciones podría mover el PER en cualquier dirección.
- **El costo de construcción viene de fuentes débiles.** La calibración del BTS lo valida de forma indirecta, pero hay que contrastarlo con presupuestos reales.
- **La prima de renta no tiene serie pública.** Es la variable más sensible y la menos medida.
- **Dos simplificaciones tributarias.**
  - En el régimen B con venta por unidades no se modela la prorrata del crédito fiscal.
  - Las pérdidas tributarias se arrastran sin límite.
- **El cap de salida es una estimación sin transacciones residenciales institucionales comparables en Perú.**
- **El modelo es de un proyecto tipo.** Cada terreno requiere su propio análisis; el modelo está publicado para eso.

## Datos a verificar

| Dato | Valor usado | Fuente sugerida |
|---|---|---|
| Precio y alquiler de cierre por tipología | Oferta − 4% | Tasaciones; registros SUNARP; RAV (D.Leg. 1177) |
| Prima de renta del producto institucional | 0% base; mapa de 0%-30% | Rent rolls de edificios en operación (contrato 04) |
| Incidencia del terreno en Lima Moderna | 15.7% de las ventas | Transacciones de terrenos; tasadores |
| Costo directo por m² techado | S/ 2,050 sin IGV | Presupuestos de constructoras; CAPECO; índices INEI |
| Tasa del crédito de obra y del mini-perm en soles | 10.0% y 9.0% TEA | SBS, tasas activas de medianas y grandes empresas; cotizaciones bancarias |
| Cap rate institucional residencial | 6.50% | Transacciones de FIBRA/fondos; clasificadoras |
| Texto final del PL 58-2026 y tratamiento del crédito fiscal | Régimen B | Congreso; SUNAT; tributarista |
| Requisitos y plazos del D.Leg. 973 | Devolución con 2 trimestres de rezago | MEF, ProInversión |
| Predial de un edificio de renta | S/ 22 por m² al año | Municipalidad distrital; autoavalúo |

## Fuentes

1. BCRP, *Nota de Estudios 16-2026: Indicadores del mercado inmobiliario, IV trimestre 2025*: https://www.bcrp.gob.pe/docs/Publicaciones/Notas-Estudios/2026/nota-de-estudios-16-2026.pdf
2. BCRP, BCRPData, series de precios por m² (PD38028PQ, PD37944PQ) e indicador PER: https://estadisticas.bcrp.gob.pe/estadisticas/series/trimestrales/mercado-inmobiliario
3. Andina, "BCR eleva tasa de interés de referencia a 4.50% por inflación" (12-nov-2026): https://andina.pe/agencia/noticia-bcr-eleva-tasa-interes-referencia-a-450-inflacion-1099738.aspx
4. BBVA Research, "Perú | BCRP eleva la tasa a 4,50 % y no descartamos algún ajuste adicional" (13-nov-2026): https://www.bbvaresearch.com/publicaciones/peru-bcrp-eleva-la-tasa-a-450-y-no-descartamos-algun-ajuste-adicional/
5. Panamericana, inflación de 5.3% a octubre de 2026: https://panamericana.pe/politica/477390-bcr-eleva-tasa-interes-4-50-contener-avance-inflacion
6. MEF, Reporte diario de bonos soberanos (30-set-2026): https://www.mef.gob.pe/contenidos/english/report/2026/Daily_09_30_26.pdf
7. Andina, tasa hipotecaria promedio en soles 2026 (BCRP): https://andina.pe/agencia/noticia-mercado-inmobiliario-credito-hipotecario-crece-76-a-julio-1092400.aspx
8. BCRP, Nota Informativa del 16-mar-2026, tasas activas por segmento: https://www.bcrp.gob.pe/docs/Transparencia/Notas-Informativas/2026/nota-informativa-2026-03-16.pdf
9. Urbania, *Index Lima*, octubre 2025 (rentabilidad bruta de 5.27%): https://urbania.pe/blog/wp-content/uploads/2025/11/INDEX_LIMA_REPORTE_2025-10.pdf
10. Gestión, rentabilidad bruta de 5.44% en Lima (Urbania, 2026): https://gestion.pe/economia/empresas/compra-de-viviendas-la-mayor-demanda-es-por-departamentos-de-entre-45-m2-a-80-m2-noticia/
11. Revista Economía, FIBRA Prime al II trim. 2026: https://www.revistaeconomia.com/fibra-prime-avanza-en-la-adquisicion-del-parque-logistico-lima-sur-por-us145-millones/
12. Infomercado, FIBRA Prime: 40 inmuebles y 95.3% de ocupación: https://infomercado.pe/parque-logistico-lima-sur/
13. Mercado Libre Chile, datos de ACAFI sobre renta residencial (jul-2026): https://www.mercadolibre.cl/blog/re-fondos-inversion-inmobiliaria-chile
14. Gestión, Proyecto de Ley 58-2026 (Bono de Arrendamiento y exoneración del IGV): https://gestion.pe/tu-dinero/inmobiliarias/jovenes-que-vivan-solos-tambien-podrian-acceder-al-bono-para-alquiler-noticia/
15. CMS Grau, "Aprueban nueva Ley de la Vivienda de Interés Social (VIS)", Ley 32379: https://cms.law/en/per/publication/aprueban-nueva-ley-de-la-vivienda-de-interes-social-vis
16. CMS Grau, proyecto de reglamento de la Ley 32379 (RM 269-2026-VIVIENDA): https://cms.law/en/per/publication/publican-el-proyecto-de-reglamento-de-la-ley-de-vivienda-de-interes-social-vis
17. Urbania, rentabilidad bruta por distrito (actualizado al 27-may-2026): https://urbania.pe/blog/se-amplio-el-plazo-de-retornos-para-las-inversiones-en-inmuebles-de-lima/
18. Gestión, ASEI y ADI sobre por qué no despega el multifamily: https://gestion.pe/tu-dinero/inmobiliarias/vivienda-alquiler-de-vivienda-venta-de-vivienda-multifamily-mvcs-viviendas-para-alquiler-no-despegan-lo-que-hace-falta-para-impulsarlas-noticia/
19. TUO de la Ley del IGV (DS 055-99-EF); TUO de la Ley del Impuesto a la Renta (DS 179-2004-EF), arts. 39 y 52-A; Ley 30532 (FIBRA); D.Leg. 973 y DS 084-2007-EF; D.Leg. 776 (Tributación Municipal); D.Leg. 1177; Ley 29090; Ley 31313; Ley 32379. Texto oficial en el Sistema Peruano de Información Jurídica (SPIJ) y El Peruano.

*Este artículo es un análisis financiero y no constituye asesoría legal, tributaria ni de inversión. Las afirmaciones normativas deben validarse con abogados y tributaristas antes de estructurar una operación.*
