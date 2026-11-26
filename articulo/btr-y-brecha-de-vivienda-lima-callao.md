# ¿Puede la vivienda en renta ayudar a cerrar la brecha de vivienda en Lima y Callao?

**Una propuesta de suelo público en derecho de superficie, sin subsidio al modelo de negocio, medida con números**

Por: Juan Germán Gayoso Arnillas · Versión 1.0 · 26 de noviembre de 2026

Segundo de dos artículos. El primero, [*Vivienda en renta en Lima: dónde y bajo qué condiciones es viable hoy*](financiamiento-vivienda-en-renta-peru.md), mide la viabilidad del multifamily en el mercado.

Modelo: [`modelo/modelo_suelo_publico.py`](../modelo/modelo_suelo_publico.py) · Hoja con fórmulas: [`modelo/memoria-suelo-publico.xlsx`](../modelo/memoria-suelo-publico.xlsx) · Memoria de cálculo: [`memoria-de-calculo-suelo-publico.md`](memoria-de-calculo-suelo-publico.md) · Contrato modelo: [`contratos/12-derecho-de-superficie-suelo-publico.md`](../contratos/12-derecho-de-superficie-suelo-publico.md)

---

## Conclusión

**Tal como funciona hoy, el multifamily no cierra la brecha de vivienda, y subsidiarlo empeoraría el problema.** El edificio de renta institucional solo es viable en Lima Top y en la parte más cara de Lima Moderna, con alquileres que superan los S/ 2,400 al mes. Esa no es la demanda que está en el déficit. Un subsidio a la oferta (crédito fiscal, tasa preferente o suelo regalado) no cambia ese hecho: la ventaja se capitaliza en el precio del terreno y la pagan después todos los compradores, incluidos los de vivienda para venta.

**Sí puede contribuir, en una escala acotada, si se cambia el modelo de negocio y no solo la ingeniería financiera.** Lo que cambia es que el terreno sale del negocio inmobiliario. Bajo cuatro condiciones, el Estado no regala nada y el modelo cierra:

1. **Suelo público bien ubicado.** El Estado aporta terreno en derecho de superficie por un primer periodo de **45 años**. Lo valora a precio de mercado y lo cobra en segundo lugar en la cascada de retornos, después de los inversionistas y antes del excedente.
2. **Paridad del IGV.** El alquiler de vivienda de una empresa tributa igual que el de una persona natural (exonerado), como en Colombia y Chile.
3. **Capital por etapas, con un costo combinado cercano a 7.5% en soles.** Cada tramo entra y sale según su horizonte: desarrollo, deuda de obra, mini-perm, y luego bonos, FIBRA o AFP.
4. **Al vencimiento, reversión y relicitación, no venta de unidades.** El edificio revierte al Estado, que licita un segundo periodo y cobra por él.

Con esas condiciones, los inversionistas obtienen 7.5%. El Estado recupera el terreno con una TIR de 6.66%, por encima de su costo de deuda de 6.3%, y un VPN positivo de S/ 160 por m² (unos S/ 0.9 millones por edificio).

El margen es estrecho, y hay que decirlo: un alquiler 10% menor, un costo de obra 10% mayor o un capital al 8% lo vuelven negativo. **En ubicaciones periféricas, con alquileres 20% menores, no hay plazo legal que lo haga funcionar.**

La asequibilidad no sale del terreno; sale de un **bono visible a la familia**. Es el diseño de la Ley 30952: S/ 500 al mes por hasta cinco años, 70% para el alquiler y 30% para ahorro. Ese bono permite que hogares con ingresos de S/ 3,200 a S/ 4,500 paguen el alquiler de mercado y ahorren S/ 9,000 para dar el salto a Techo Propio o al Nuevo Crédito Mivivienda.

En nuestra opinión, la contribución es real pero modesta:

- Un programa de diez edificios al año agregaría unas 1,370 viviendas en renta por año. Es menos del 1% anual del déficit cuantitativo de Lima y Callao.
- Lo que el esquema sí aporta es rotación: cada departamento atiende a una familia distinta cada cinco años.

El esquema también deja una regla de política pública: **todo apoyo estatal tiene que verse en el presupuesto** (el bono) **o cobrarse** (el terreno).

---

## 1. La afirmación que se pone a prueba

Promotores, gremios y algunos funcionarios sostienen que el multifamily contribuiría a cerrar la brecha de vivienda si el Estado lo promoviera. El argumento tiene dos partes:

- más oferta de alquiler formal da una alternativa a quien no puede comprar;
- la competencia ordena un mercado de alquiler mayormente informal.

Este artículo pone a prueba esa afirmación en tres pasos:

1. ¿El multifamily de mercado llega a la demanda que está en el déficit?
2. Si no llega, ¿un subsidio al modelo lo resolvería?
3. Si tampoco, ¿qué cambio en el modelo de negocio permitiría contribuir sin subsidiarlo?

## 2. La brecha: tamaño y quién queda fuera

**Tabla 1. Déficit y producción de vivienda** (hechos con fuente; las cifras de déficit se basan en el Censo 2017 y deben actualizarse con el Censo 2025).

| Indicador | Valor | Fuente |
|---|---|---|
| Déficit habitacional nacional | 1.56 millones de hogares: 64% cualitativo (mejoras) y 36% cuantitativo (viviendas nuevas) | MVCS, presentación a la Comisión de Vivienda del Congreso (mar-2025); La República (ago-2026) |
| Déficit cuantitativo, provincia de Lima | 198,377 viviendas (35% del nacional) | MVCS sobre INEI 2017 |
| Déficit cuantitativo, Callao | 21,803 viviendas | MVCS sobre INEI 2017 |
| Déficit de Lima según el PLANMET 2040 | ~225,000 viviendas | Entrevista en La República (oct-2024) |
| Edificaciones urbanas producidas en Lima y Callao | 48,540 unidades en 2024 | Infobae (feb-2026), columna de opinión; verificar con CAPECO |
| Venta de vivienda nueva en Lima Metropolitana | >26,000 en 2025; ~32,000 proyectadas en 2026 | Credicorp Capital, vía Gestión |
| Ingreso para calificar al crédito de la vivienda nueva más barata | Subió de ~S/ 4,000 a ~S/ 5,000 al mes; el ticket mínimo pasó de S/ 210,000 a S/ 250,000 | Proper, vía Infobae (may-2026) |
| Nivel socioeconómico C en Lima | 45% de los hogares; ingreso promedio de S/ 4,325 al mes | Proper, vía Infobae (may-2026) |
| Tope de ingreso de Techo Propio | S/ 3,715 al mes para comprar (AVN); S/ 2,706 para construir o mejorar | El Peruano; MVCS (2026) |

De esos datos salen dos hechos:

- **El déficit cuantitativo de Lima y Callao (~220,000 viviendas) equivale a casi siete años de ventas formales al ritmo de 2026.** Además, las ventas crecen en su mayor parte en el tramo que ya accede al crédito.
- **Hay un tramo de hogares que el mercado de venta no atiende.** Ganan entre S/ 3,000 y S/ 5,000: demasiado para los programas más focalizados y muy poco para el crédito hipotecario de la vivienda nueva más barata. En ese grupo pesan los ingresos informales o recientes, que el sistema financiero no puede acreditar.

Este artículo trata sobre ese tramo. No pretende resolver todo el déficit: el déficit cualitativo y los hogares de menores ingresos necesitan otros instrumentos (§9).

## 3. Por qué el multifamily de mercado no llega ahí

El [primer artículo](financiamiento-vivienda-en-renta-peru.md) mide cuánto puede pagar por el terreno un edificio de renta frente a uno de venta en Lima Moderna. Su resultado, en corto:

- **Con el alquiler promedio de Lima Moderna (US$ 119 por m² al año) el BTR no paga el terreno de mercado.** Ni con el IGV neutral ni con toda la ingeniería financiera disponible.
- **Con el IGV neutral (exonerado) necesita una prima de renta de 21% a 34%** sobre ese promedio, es decir, US$ 144 a 159 por m² al año, según la vara de retorno y un cap de 6.5%. **Con el IGV vigente, la prima sube a 31%-46%.**
- **Los edificios lanzados en Lima confirman esa lectura: están donde la prima existe.**
  - El edificio de Av. Ricardo Palma 251, en Miraflores, ofrece 280 unidades de 53 a 60 m² desde S/ 2,909 al mes. Eso equivale a unos US$ 170 a 190 por m² al año.
  - LiveSpace La Mar, de Parque Arauco, ofrece departamentos de un dormitorio desde S/ 2,385.
  - Gestión reportó que los alquileres multifamily en Lima superan los S/ 2,400 al mes. Lima tenía 160 unidades en operación y unas 900 en construcción a fines de 2024.

Un alquiler de S/ 2,400 a S/ 2,900 exige un ingreso de S/ 8,000 a S/ 9,700 si no supera el 30% del ingreso. Es un producto legítimo y útil para ese segmento. **Pero no es vivienda para la brecha.** Podría aliviarla de forma indirecta: la evidencia de EE. UU. muestra que los edificios nuevos de mercado bajan entre 5% y 7% los alquileres cercanos, porque absorben demanda que de otro modo competiría por el stock existente (Asquith, Mast y Reed, 2023). Ese efecto, llamado filtrado, requiere volumen. Con unas mil unidades en Lima, es imperceptible.

## 4. Por qué subsidiar el modelo empeora el problema

### 4.1 Asimetrías entre vender y rentar: cuáles se pueden corregir

El BTR pierde el terreno frente al BTS por varias razones. Unas son corregibles con reglas parejas; otras son estructurales.

**Tabla 2. Asimetrías BTS-BTR.**

| Asimetría | Efecto | ¿Temporal o permanente? | Corrección que nivela sin inclinar la cancha |
|---|---|---|---|
| IGV: la empresa que alquila cobra 18%; la persona natural no | ~2 puntos de TIR en contra del BTR (artículo 1, tabla 7) | Corregible por norma | Exonerar el alquiler de vivienda de empresas, con el IGV de obra como costo (régimen B). Es el estándar de Colombia (Estatuto Tributario, art. 476, num. 15) y de Chile (el arriendo de inmuebles sin amoblar no está gravado con IVA, según el SII) |
| IR: el arrendador persona natural paga 5% del bruto (6.25% sobre el 80%), pero una parte no declara | La informalidad abarata el alquiler con el que compite el BTR | Corregible por fiscalización | Cruce de información (RAV del D.Leg. 1177, recibos, SUNARP) y fiscalización por SUNAT. No hay cifra pública de evasión; es un dato por levantar |
| Prima de riesgo: sin historia de rentas, morosidad ni desalojos, el institucional pide más | Encarece el capital del BTR | Se reduce con información y reglas | Serie pública de rentas de cierre y morosidad (BCRP/SBS), desalojo notarial predecible, rent rolls estandarizados (contrato 04) |
| Financiamiento de largo plazo en soles | Mini-perm de 5-7 años con saldo final de 89%-96% | Se reduce con mercado de capitales | Bonos de titulización, FIBRA y AFP como tenedores de largo plazo |
| El BTS recupera el capital en 3-4 años; el BTR en 10 o más | El promotor que vende recicla capital y exige 20% | **Permanente** | No se corrige: es la naturaleza del negocio. Se resuelve con capital por etapas (§5.4) |
| El comprador que invierte acepta un rendimiento bruto de ~5.3% y fija el precio del terreno | El terreno vale lo que paga el que compra para alquilar | **Permanente** | No se corrige con política tributaria. Refleja preferencias (la vivienda como depósito de valor familiar) |

La conclusión de la tabla es la razón de ser de este artículo. **Aun con todas las asimetrías corregibles corregidas, las dos permanentes mantienen al BTR fuera del suelo de mercado** fuera de los nichos de alta renta. Por eso hace falta otra medida, y esa medida no puede ser un subsidio.

### 4.2 Por qué no un subsidio a la oferta

Un subsidio al proyecto (crédito tributario, tasa preferente o terreno a precio simbólico) aumenta lo que el BTR puede pagar por el suelo. En un mercado de suelo con oferta rígida, como el de las zonas bien ubicadas de Lima, ese mayor valor se traslada al precio del terreno: compiten por él tanto el BTR subsidiado como el BTS. La evidencia del principal programa de subsidio a la oferta de alquiler, el crédito tributario LIHTC de EE. UU., va en esa dirección:

- Eriksen y Rosenthal (2010) estiman que buena parte de las viviendas subsidiadas desplaza construcción que el mercado habría hecho igual. Con variables instrumentales, el desplazamiento se acerca a 100%.
- Soltas (2024) encuentra un desplazamiento de unos 75% a nivel de predio.

El subsidio termina pagando terreno y proyectos que se habrían hecho de todos modos, no viviendas adicionales. En Lima, además, encarecería el suelo para el BTS y para la vivienda social en venta. Se ampliaría la brecha que se quería cerrar.

**La paridad del IGV no es un subsidio.** Iguala a la empresa con la persona natural y no da al BTR nada que el arrendador individual no tenga. Una tasa cero con devolución del IGV de obra sí lo sería (artículo 1, régimen C).

## 5. La propuesta: separar el suelo del negocio

### 5.1 La idea

El terreno es el insumo que el BTR no puede pagar a precio BTS. Si el Estado tiene suelo bien ubicado, puede aportarlo sin venderlo ni regalarlo:

- **Instrumento:** derecho de superficie (Código Civil, arts. 1030-1034). Permite construir y explotar sobre suelo ajeno por un plazo de hasta 99 años. Al vencimiento, lo construido pasa al dueño del suelo; el Código prevé reembolsar su valor, salvo pacto en contrario. Aquí se pacta la reversión sin pago.
- **Valoración:** el terreno se aporta a valor de mercado, el que pagaría el BTS (S/ 1,015 por m² vendible en el caso de Lima Moderna).
- **Prelación:** el Estado cobra su terreno con un retorno igual a su costo de deuda (6.3%), **después** de que los inversionistas recuperen su capital con su retorno y **antes** de que se reparta el excedente.
- **Excedente:** se reparte entre el Estado y el operador. El porcentaje es una variable de la licitación.

Así el Estado no subsidia: presta un activo y lo cobra con intereses. Lo que acepta es **cobrar en segundo lugar y más tarde**, y ese es el aporte que viabiliza el modelo. Su costo es el riesgo de no cobrar todo (§6), que se mide y se reporta.

### 5.2 Al vencimiento: relicitación, no venta

Al final del primer periodo (T1 = 45 años) el edificio revierte al Estado. El Estado no lo vende por unidades: **licita un segundo periodo de 30 años** y cobra al nuevo operador el valor presente de ese periodo, descontada la renovación que este deberá hacer.

Se descarta convertir el edificio a venta (BTS) por tres razones:

- retiraría vivienda en renta justo cuando el edificio ya está pagado;
- crearía una ganancia de capital que el mercado anticiparía en el precio de las licitaciones;
- convertiría un programa de vivienda en renta en un BTS diferido con suelo público.

### 5.3 Revisión cada diez años y rotación de inversionistas

Un contrato de 45 años no puede fijar todo desde el inicio. El contrato modelo (contrato 12) prevé:

- **Revisión decenal.** Una comisión técnica independiente compara el desempeño con el modelo de la licitación (rentas, ocupación, opex, costo de capital) y puede ajustar el reparto del excedente, la renta máxima o el plan de renovaciones. El ajuste tiene límites: no puede alterar el retorno ya devengado de los inversionistas ni la prelación del Estado.
- **Cambio de paquete de inversionistas.** El operador puede ceder su posición entre etapas a un cesionario calificado, sin pedir consentimiento discrecional. Es lo esperado: el desarrollador sale al estabilizar y entra el tenedor de largo plazo.
- **Renegociación solo por causas tasadas:** cambio de ley, fuerza mayor o desequilibrio mayor a un umbral pactado. El riesgo comercial ordinario no la habilita.

### 5.4 Capital por etapas

Ningún inversionista acepta 45 años de iliquidez con un solo retorno. El esquema separa el horizonte en tramos:

**Tabla 3. Capital por etapas** (rangos estimados; nov-2026).

| Etapa | Años | Quién | Retorno o tasa | Sale cuando |
|---|---|---|---|---|
| Desarrollo | 0-3 | Desarrollador + capital de desarrollo | 12%-14% exigido | Estabiliza (año 5) |
| Obra | 1-3 | Banco: crédito de obra | ~10% TEA | Se toma el mini-perm |
| Estabilización | 4-10 | Banco: mini-perm | ~9% TEA | Se refinancia con largo plazo |
| Largo plazo | 5-45 | FIBRA, AFP, aseguradoras; bonos de titulización en soles o VAC | 6.5%-7.5% nominal | Fin de T1, o cesión a otro tenedor |

**Supuesto clave.** El costo combinado es de 7.5%. Como 40 de los 45 años son de operación, pesa sobre todo el costo del tramo de largo plazo. Es una estimación, no un dato de mercado: no hay en el Perú transacciones de vivienda en renta a 40 años que lo validen. Por eso se muestra la sensibilidad a 7% y a 8%.

Una consecuencia práctica: el modelo da a la etapa de desarrollo una TIR de 9.4% sin deuda, insuficiente para un desarrollador a riesgo. La estructura que funciona es de compromiso anticipado (*forward funding*):

- el tenedor de largo plazo compromete el capital desde la licitación;
- el desarrollador cobra un honorario más un incentivo atado a costo y plazo.

### 5.5 Qué suelo y dónde

La selección del suelo no es un detalle operativo: decide si el esquema funciona (§6) y si contribuye a una mejor ciudad.

- **Instrumentos legales.** La Ley 31313 (Desarrollo Urbano Sostenible), modificada por el D.Leg. 1674, da instrumentos de gestión del suelo y asigna al Fondo MIVIVIENDA la función de Operador Público del Suelo.
- **Marco de planificación.** El Plan de Desarrollo Metropolitano de Lima al 2040 (PLANMET 2040) es el marco para identificar zonas.
- **Criterios propuestos para elegir los lotes:**
  - a menos de 800 m de una estación de transporte masivo (Metropolitano, Línea 1 o 2, corredores);
  - zonas consolidadas con equipamiento existente;
  - alquiler de mercado no menor al promedio de Lima Moderna (el umbral del §6);
  - mezcla de ingresos dentro del edificio y del barrio;
  - suelo estatal hoy subutilizado: lotes de entidades, terrenos residuales de obras, predios de la SBN.

El cuarto criterio importa. Si el programa concentra a los hogares del bono en un solo lugar, reproduce la segregación que dice combatir. Un edificio con mezcla de unidades, con o sin bono, en una zona bien servida, cumple el objetivo urbano y además sostiene la renta de mercado que la cascada necesita.

## 6. Los números

**Tabla 4. Escenarios** (S/ por m² vendible; soles nominales; antes de IR). "VPN del Estado" es el valor presente de los flujos que recibe por su terreno, menos el terreno, descontados a su costo de deuda de 6.3%.

| Escenario | TIR inversionistas | ¿Cobran su retorno? | TIR del Estado | VPN del Estado | Recupera el terreno |
|---|---|---|---|---|---|
| E0. IGV vigente, capital 9%, 30 años | 6.1% | No | 5.4% | −239 | No |
| E1. Paridad IGV, capital 9%, 45 años | 8.2% | No | 4.8% | −480 | No |
| E2. Paridad IGV, capital 8%, 45 años | 8.0% | Sí | 5.6% | −266 | No |
| E3. Paridad IGV, capital 7.5%, 40 años | 7.5% | Sí | 6.4% | +30 | Año 40 (en el límite) |
| **E4. Propuesta: paridad IGV, capital 7.5%, 45 años** | **7.5%** | **Sí** | **6.7%** | **+160** | **Año 45** |
| E5. Paridad IGV, capital 7.5%, 50 años | 7.5% | Sí | 6.9% | +268 | Año 50 |
| E6. E4 con 15% de descuento al inquilino pagado con el terreno | 6.5% | No | 4.6% | −531 | No |

**Tabla 5. Sensibilidad de la propuesta (E4).**

| Variación | ¿Inversionistas cobran 7.5%? | VPN del Estado |
|---|---|---|
| Alquiler −10% | No (7.1%) | −477 |
| Alquiler −20% (ubicación periférica) | No (5.9%) | −586 |
| Costo de obra +10% | No (7.4%) | −380 |
| Valor de relicitación −25% | Sí | −1 |
| Capital al 7.0% | Sí | +492 |
| Capital al 8.0% | Sí (8.0%) | −266 |
| Estado se financia al 7.0% | Sí | −129 |

**Tabla 6. Primer periodo mínimo para que todos cobren** (inversionistas a su tasa y Estado con VPN ≥ 0).

| Costo del capital | Lima Moderna | Alquiler −20% |
|---|---|---|
| 7.0% | 31 años | No existe dentro de 99 años |
| 7.5% | 36 años | No existe |
| 8.0% | 59 años | No existe |
| ≥ 8.5% | No existe | No existe |

Cómo leer los números:

- **Las dos correcciones son necesarias y ninguna basta sola.** Sin paridad del IGV (E0), ni con suelo gratis en los primeros años cobran los inversionistas. Con paridad pero con capital al 9% (E1), cobran a costa del Estado.
- **El plazo es una variable de diseño, no un regalo.** Con capital al 7.5%, 36 años bastan en teoría. Se proponen 45 para que un error de estimación no convierta la operación en subsidio.
- **El margen es estrecho.** S/ 160 por m² de VPN sobre un terreno de S/ 1,015 es 16% del valor aportado. La licitación competitiva (§7) busca que ese margen vaya al Estado y no al operador.
- **Un descuento pagado con el terreno es un subsidio escondido (E6).** Si se quiere un alquiler menor, que lo pague un bono visible.
- **La periferia no funciona con este instrumento.** No es un problema de plazo: con alquileres 20% menores, el NOI no cubre el capital ni con 99 años. Para esas zonas hacen falta otros instrumentos (§9).
- **Medido con la vara de un inversionista privado (9%), el Estado cede valor (VPN −615 por m²).** El Estado acepta un retorno menor al privado porque su costo de deuda es menor y porque obtiene beneficios públicos (vivienda asequible, ciudad compacta) que no entran en la TIR. Es una decisión de política pública que conviene tomar a la vista, no un hecho técnico.

## 7. Cómo se adjudica: licitación con reparto del excedente

Para que el margen no lo capture el operador, el terreno se adjudica por licitación pública con tres variables de oferta:

1. **Porcentaje del excedente que va al Estado** (en el modelo, 50%). Gana más quien ofrece más.
2. **Renta inicial por m²**, con tope en la renta de mercado tasada e indexada a la inflación.
3. **Plan de renovaciones** con montos y años comprometidos.

Requisitos de precalificación:

- capital de largo plazo comprometido (cartas de AFP, aseguradoras o FIBRA);
- experiencia en operación de vivienda en renta;
- un modelo financiero auditable (como el que acompaña este artículo) que la entidad pueda reproducir.

## 8. A quién sirve: bono visible y graduación

### 8.1 El bono

El alquiler de mercado de un departamento de 40 m² en una ubicación tipo Lima Moderna es de unos S/ 1,302 al mes (nov-2026). El bono de la Ley 30952 (Renta Joven) cubre la brecha de pago de un tramo preciso de hogares.

**Tabla 7. Asequibilidad con bono** (esfuerzo máximo de 30% del ingreso; soles de nov-2026).

| Ingreso del hogar | Paga (30%) | Bono al alquiler | ¿Alcanza para el alquiler de mercado? |
|---|---|---|---|
| S/ 2,500 | 750 | 350 | No: faltan S/ 202 |
| S/ 3,000 | 900 | 350 | No: faltan S/ 52 |
| S/ 3,500 | 1,050 | 350 | Sí |
| S/ 4,000 | 1,200 | 350 | Sí |
| S/ 4,500 | 1,350 | No lo necesita | Sí |

El tramo objetivo va de unos S/ 3,200 a S/ 4,500 al mes. Son hogares que no califican al crédito de la vivienda nueva más barata (~S/ 5,000 de ingreso), que en parte están en el rango de Techo Propio AVN (hasta S/ 3,715) y que necesitan tiempo para formalizar o acreditar ingresos.

El bono tiene tres virtudes que el subsidio al proyecto no tiene:

- **Se ve.** Su costo, S/ 30,000 por hogar en cinco años, está en el presupuesto y se puede evaluar.
- **Es portátil y temporal.** Acompaña a la familia y termina.
- **Ahorra.** Los S/ 150 mensuales que van a la cuenta de ahorro suman S/ 9,000 en cinco años: más del ahorro mínimo de Techo Propio AVN (3% del valor de la vivienda, unos S/ 3,300 para una vivienda de S/ 109,100).

### 8.2 Graduación

La permanencia en el programa es temporal por diseño. El contrato de arrendamiento con bono (contrato 03, anexo) prevé:

- revisión anual del ingreso;
- acompañamiento para acreditar ingresos ante el sistema financiero (historial de pago puntual del alquiler reportado a centrales de riesgo, con consentimiento);
- al terminar el bono, o antes si el ingreso supera el tope, la familia pasa a tres opciones: comprar con Techo Propio o con el Nuevo Crédito Mivivienda usando el ahorro acumulado, seguir como inquilino a renta de mercado, o mudarse.

**Una lección del pasado.** El bono Renta Joven tuvo poca acogida en sus primeros años. El Fondo Mivivienda atribuyó el problema a la escasa oferta de alquiler formal: el bono existía, pero no había edificios donde usarlo. El esquema de este artículo une las dos piezas: oferta formal sobre suelo público y bono a la demanda.

### 8.3 El riesgo de que el bono suba los alquileres

Un subsidio a la demanda en un mercado con oferta fija puede subir los alquileres; hay evidencia de ese efecto con los vales de alquiler en EE. UU. (Susin, 2002). Aquí se mitiga de dos formas:

- el bono se aplica a viviendas **nuevas** del programa, que agregan oferta;
- la renta del edificio queda topada en la oferta de la licitación e indexada a la inflación, no al bono.

## 9. ¿Cuánto contribuye a la brecha? Estimación a escala

**Tabla 8. Orden de magnitud de un programa** (estimación; supone 10 edificios al año como el del modelo).

| Concepto | Valor | Cálculo |
|---|---|---|
| Viviendas por edificio | ~137 de 40 m² | 5,500 m² / 40 |
| Viviendas nuevas por año | ~1,370 | 10 × 137 |
| Proporción del déficit cuantitativo de Lima y Callao (~220,000) | ~0.6% al año | 1,370 / 220,000 |
| Suelo público comprometido por año | ~S/ 56 millones a valor de mercado (se recupera) | 10 × 5,500 × 1,015 |
| Capex privado movilizado por año | ~S/ 213 millones | 10 × 5,500 × 3,868 |
| Costo fiscal del bono, régimen estable (5 cohortes) | ~S/ 21 millones al año con la mitad de las unidades con bono (mezcla de ingresos); ~S/ 41 millones si todas lo llevan | 5 × 1,370 × 500 × 12 × 50% |
| Familias atendidas por vivienda en 45 años | ~9 | 45 / 5 años de permanencia |

En nuestra opinión, la contribución tiene tres dimensiones:

1. **En stock es pequeña.** Menos del 1% anual del déficit. No reemplaza a Techo Propio ni al Nuevo Crédito Mivivienda. Como referencia, en 2026 se transfirieron S/ 519 millones a Techo Propio para unas 14,000 familias.
2. **En flujo es mayor.** Cada vivienda en renta con graduación atiende a una familia distinta cada cinco años. En 45 años, un edificio de 137 departamentos acompaña a unas 1,200 familias en su tránsito a la vivienda propia.
3. **Lo más valioso es institucional.** El programa crearía un mercado de vivienda en renta formal, con historia de rentas, morosidad y desalojos. Eso reduce la prima de riesgo del BTR privado (tabla 2) y, con el tiempo, le permite llegar a segmentos más bajos sin ayuda.

**Lo que este instrumento no resuelve:**

- el déficit cualitativo (64% del total), que se atiende con mejoramiento;
- los hogares con ingresos menores a ~S/ 2,700, que necesitan Techo Propio en Construcción en Sitio Propio o vivienda pública en arriendo;
- la expansión informal de la periferia, que se ataca con habilitación urbana y suelo urbanizado a bajo costo, no con edificios de renta.

## 10. Alternativas comparadas

**Tabla 9. Cuatro caminos para la vivienda en renta asequible** (opinión profesional sustentada en el análisis).

| | A. BTR de mercado sin intervención | B. Subsidio a la oferta (crédito fiscal, suelo regalado) | C. Suelo público con retorno subordinado (propuesta) | D. Vivienda pública en arriendo directo (modelo chileno "Arriendo a Precio Justo") |
|---|---|---|---|---|
| Llega al tramo de la brecha | No | Sí, mientras dure el subsidio | Sí, con bono, en zonas con renta media | Sí, incluso a ingresos menores |
| Costo fiscal | Ninguno | Alto y poco visible | El bono (visible); el terreno se recupera | Alto: el Estado construye y opera |
| Efecto en el precio del suelo | Neutro | Lo sube (capitalización) | Neutro, si el terreno se valora a mercado y se licita | Neutro |
| Moviliza capital privado | Sí, poco | Sí | Sí, de largo plazo | Poco |
| Riesgo principal | No contribuye | Desplaza a la construcción privada y encarece el suelo | Margen estrecho; riesgo de contrato a largo plazo | Capacidad de gestión del Estado |
| Requisito normativo | Paridad del IGV | Ley de incentivos | Paridad del IGV + marco de derecho de superficie sobre suelo estatal | Ley y presupuesto de vivienda pública |

**Recomendación: C, con piloto.** Empezar con dos a cuatro lotes estatales en Lima Moderna y Lima Centro con alquiler de mercado comprobado. Licitarlos con el contrato 12 y medir rentas, morosidad y graduación durante cinco años antes de escalar. D es complementaria para los ingresos que C no alcanza. Chile la aplica sobre terrenos fiscales cedidos en comodato a municipios y Serviu, con rentas atadas a no más de 25% del ingreso.

## 11. Riesgos

| Riesgo | Qué lo dispara | Mitigación |
|---|---|---|
| Comercial | Alquiler menor al proyectado | Selección de suelo con renta comprobada; tasación independiente; mezcla de ingresos |
| De costo | Sobrecosto de obra mayor a 10% | Contrato NEC de precio objetivo (contrato 10); garantía del desarrollador; contingencia |
| De tasa | El capital de largo plazo cuesta 8% o más | Compromiso de capital desde la licitación; bonos en VAC; precalificación |
| Contractual y político | Cambio de reglas, revisión unilateral, presión por bajar rentas | Cláusulas de estabilidad y compensación; revisión decenal con comisión independiente; acuerdo directo con financistas (contrato 06) |
| De relicitación | El segundo periodo vale menos | Renovaciones obligatorias; estándar de mantenimiento con auditoría; valor reportado anualmente |
| Fiscal | Programa de bonos sin financiamiento | Presupuesto multianual; tope de unidades con bono por edificio |
| De captura | El margen va al operador | Licitación con reparto del excedente; modelo financiero público; revisión decenal |
| De segregación | Concentración de hogares con bono | Tope de unidades con bono por edificio; criterios del PLANMET |

## 12. Próximos pasos

1. **MEF / Congreso:** aprobar la paridad del IGV del alquiler de vivienda por empresas (régimen B), con el IGV de obra como costo. Es la condición sin la cual nada de lo anterior funciona.
2. **MVCS / Fondo MIVIVIENDA (Operador Público del Suelo) / SBN:** hacer un inventario de suelo estatal en Lima y Callao que cumpla los criterios del §5.5 y tasarlo.
3. **MVCS:** adaptar el reglamento del bono de arrendamiento (Ley 30952) para vincularlo a unidades del programa, con una cuenta de ahorro y una ruta de graduación a Techo Propio y al Nuevo Crédito Mivivienda.
4. **SMV / SBS:** confirmar que una FIBRA y las AFP pueden tener derechos de superficie sobre suelo estatal (ver "Datos a verificar").
5. **Piloto:** licitar de dos a cuatro lotes con el contrato 12 y publicar el modelo financiero de cada licitación.

## Datos a verificar

| Dato | Valor usado | Fuente sugerida |
|---|---|---|
| Déficit cuantitativo de Lima y Callao | ~220,000 viviendas (Censo 2017) | INEI, Censo 2025; MVCS; PLANMET 2040 |
| Producción anual de vivienda en Lima y Callao | 48,540 edificaciones (2024) | CAPECO, Estudio de Edificaciones Urbanas |
| Monto, tope de ingreso y reglas vigentes del bono de arrendamiento | S/ 500; 70/30; 5 años | Reglamento vigente de la Ley 30952; Fondo MIVIVIENDA |
| Costo combinado del capital por etapas | 7.5% | Cotizaciones de AFP, aseguradoras y FIBRA; spreads de bonos de titulización (BVL, clasificadoras) |
| Costo de deuda del Estado | 6.3% (soberano a ~8-10 años) | MEF, reporte diario de bonos soberanos; BCRP |
| Valor de mercado del suelo estatal candidato | S/ 1,015 por m² vendible (Lima Moderna) | Tasación independiente por lote |
| Si una FIBRA (Ley 30532) puede tener un derecho de superficie como activo inmobiliario | Supuesto: sí | SMV; tributarista; texto de la Ley 30532 y su reglamento |
| Si el derecho de superficie sobre suelo estatal puede otorgarse por 45 años con reversión sin pago | Supuesto: sí, por pacto (CC art. 1030) | Ley 29151 y reglamento (SBN); abogado administrativista |
| Número de ordenanza y criterios del PLANMET 2040 | Ordenanza 2499-2022-MML (a confirmar) | Municipalidad Metropolitana de Lima; El Peruano |
| Alquiler de cierre de los edificios multifamily en operación | US$ 170-190 por m² al año (oferta) | Rent rolls (contrato 04); avisos actualizados |
| Efecto de los vales de alquiler en los precios | Susin (2002) | *Journal of Public Economics*, 83(1) |

## Fuentes

1. MVCS, presentación a la Comisión de Vivienda del Congreso, "Vivienda de Interés Social" (4-mar-2025): https://www.congreso.gob.pe/Docs/comisiones2024/Vivienda/files/presentaciones/10_so_ministerio_de_vivienda_vis_04.03.25.pdf
2. La República, déficit de 1.56 millones de hogares (MVCS), ago-2026: https://larepublica.pe/economia/2026/08/01/vivienda-social-en-lima-invertiran-us215-millones-en-proyecto-con-mas-de-360-departamentos-en-chorrillos-hnews-31071
3. La República, entrevista con el dato del PLANMET 2040 (225,000): https://larepublica.pe/economia/2024/10/11/las-viviendas-sociales-se-venden-a-la-clase-media-o-media-alta-la-mayoria-en-lima-939750
4. Infobae, "La demagogia no construye viviendas" (13-feb-2026): https://www.infobae.com/peru/2026/02/13/la-demagogia-no-construye-viviendas/
5. Gestión, venta de viviendas nuevas en Lima 2026 (Credicorp Capital): https://gestion.pe/peru/venta-de-viviendas-nuevas-en-lima-metropolitana-creceria-22-en-2026-noticia/
6. Infobae, ingreso para crédito hipotecario sube a S/ 5,000 (4-may-2026): https://www.infobae.com/peru/2026/05/04/el-ingreso-necesario-para-calificar-a-un-credito-hipotecario-en-peru-subio-de-s4000-a-s5000-mensuales/
7. El Peruano, Techo Propio: topes de ingreso de S/ 3,715 y S/ 2,706, y transferencia de S/ 519 millones: https://www.elperuano.pe/noticia/290465-gobierno-transfiere-s-519-millones-al-fondo-mivivienda-para-bonos-de-techo-propio
8. El Peruano, valores máximos de la VIS 2026: https://elperuano.pe/noticia/298556-buscas-una-vivienda-con-techo-propio-verifica-los-nuevos-montos-autorizados
9. Gestión, "Fondos y hasta seis inmobiliarias con interés en desarrollo multifamily" (18-nov-2024): https://gestion.pe/economia/empresas/fondos-y-hasta-seis-inmobiliarias-con-interes-en-desarrollo-multifamily-que-lo-gatillara-alquiler-de-departamentos-lima-moderna-lima-top-mercado-inmobiliario-noticia/
10. Gestión, "Lima contará con más 1,000 departamentos de renta inmobiliaria en 2025" (23-jun-2024): https://gestion.pe/economia/empresas/lima-contara-con-mas-1000-departamentos-de-renta-inmobiliaria-en-2025-donde-estaran-multifamily-empresa-miraflores-san-isidro-noticia/
11. Perú Retail, Parque Arauco lanza LiveSpace La Mar: https://www.peru-retail.com/parque-arauco-lanza-su-primer-proyecto-multifamily-en-peru-con-inversion-de-us-16-millones/
12. Urbania, avisos de LiveSpace La Mar y de Av. Ricardo Palma 251 (consultados en nov-2026): https://urbania.pe/inmueble/clasificado/alclapin-alquiler-de-departamento-en-miraflores-lima-1-dormitorio-147497922 y https://urbania.pe/buscar/alquiler-de-departamentos-en-huertos-de-san-antonio--lote-38-39---santiago-de-surco--lima--lima
13. Gob.pe, Bono de Arrendamiento para Vivienda (Renta Joven): https://www.gob.pe/33623-bono-de-arrendamiento-para-vivienda-bav
14. El Peruano, el bono Renta Joven de S/ 500 por cinco años (70/30): https://elperuano.pe/noticia/153135-gobierno-disena-nuevo-subsidio-para-alquiler-de-vivienda
15. La República, baja colocación del bono Renta Joven por falta de oferta formal (30-ene-2020): https://larepublica.pe/economia/2020/01/30/bono-renta-se-entregaron-solo-30-de-8000-subsidios
16. Gerencie, IVA y arrendamiento de vivienda en Colombia (ET art. 476, num. 15): https://www.gerencie.com/impuesto-a-las-ventas-en-el-arrendamiento-de-inmuebles.html
17. SII de Chile, arriendo de inmueble sin amoblar no gravado con IVA: https://www.sii.cl/preguntas_frecuentes/impuestos_mensuales/001_130_1214.htm
18. BCN Chile, llamado de Arriendo a Precio Justo con terrenos en comodato: https://www.bcn.cl/leychile/navegar?idNorma=1223072
19. MINVU, *Revista Redes* n.º 1, Arriendo a Precio Justo (renta de hasta 25% del ingreso): https://centrodeestudios.minvu.gob.cl/wp-content/uploads/2023/07/REVISTA-REDES_1-ARRIENDO-JUSTO.pdf
20. Asquith, B., Mast, E. y Reed, D. (2023), "Local Effects of Large New Apartment Buildings in Low-Income Areas", *Review of Economics and Statistics*, 105(2), 359-375. Versión de trabajo: https://www.philadelphiafed.org/-/media/FRBP/Assets/working-papers/2020/wp20-07.pdf
21. Eriksen, M. y Rosenthal, S. (2010), "Crowd out effects of place-based subsidized rental housing: New evidence from the LIHTC program", *Journal of Public Economics*, 94(11-12), 953-966: https://econpapers.repec.org/RePEc:eee:pubeco:v:94:y:2010:i:11-12:p:953-966
22. Soltas, E. (2024), "Tax Incentives and the Supply of Low-Income Housing" (resumen de estimaciones en NBER): https://conference.nber.org/conf_papers/f240610/f240610.slides.pdf
23. Ley 31313 y D.Leg. 1674: https://busquedas.elperuano.pe/normaslegales/ley-de-desarrollo-urbano-sostenible-ley-n-31313-1976352-2/ y https://img.lpderecho.pe/wp-content/uploads/2024/09/Decreto-Legislativo-1674-LPDerecho.pdf
24. Boletín IVUDS-URP sobre la Ley 31313 (Fondo MIVIVIENDA como Operador Público del Suelo): https://www.urp.edu.pe/pdf/id/32620/n/boletin-ivuds-03-2021.pdf
25. MEF, reporte diario de bonos soberanos (30-set-2026): https://www.mef.gob.pe/contenidos/english/report/2026/Daily_09_30_26.pdf
26. Código Civil, arts. 1030-1034 (derecho de superficie); Ley 30952 (Bono de Arrendamiento para Vivienda); Ley 30532 (FIBRA); Ley 29151 (Sistema Nacional de Bienes Estatales); D.Leg. 1177; Ley 32379 (VIS). Texto oficial en el SPIJ y El Peruano.

*Este artículo es un análisis financiero y de política pública. No constituye asesoría legal, tributaria ni de inversión. La estructura propuesta debe validarse con abogados administrativistas y tributaristas, y con las entidades competentes, antes de implementarse.*
