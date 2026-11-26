# Multifamily Viabilización

**Documentos estándar para financiar y operar vivienda en renta (Build-to-Rent / Multifamily) en el Perú, sin subsidios y con neutralidad competitiva.**

Autor: **Juan Germán Gayoso Arnillas** · Versión 2.1 · Noviembre 2026

[![Licencia: CC BY-NC 4.0](https://img.shields.io/badge/Licencia-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## Los artículos: elemento principal

El repositorio tiene dos artículos encadenados. El primero mide **dónde y bajo qué condiciones** el multifamily funciona en el mercado. El segundo responde si puede **contribuir a cerrar la brecha de vivienda** en Lima y Callao, y con qué modelo de negocio.

### 1. 👉 [Vivienda en renta en Lima: dónde y bajo qué condiciones es viable hoy](articulo/financiamiento-vivienda-en-renta-peru.md)

Es un primer esbozo de viabilidad de mercado. El artículo mide, con un modelo de flujo de caja publicado y datos de mercado de noviembre de 2026, si un edificio de vivienda para renta (BTR) puede pagar el precio de mercado del terreno en Lima Moderna, que fija el proyecto para venta (BTS).

**Conclusión:** con el régimen tributario actual, no puede. En el caso base, la TIR no apalancada es 0.5% frente a un umbral de 9%, porque el rendimiento sobre costo (5.69%) es menor que el cap de salida (6.50%). La ingeniería financiera hace el proyecto financiable, pero no lo hace viable: todas las herramientas juntas llevan la TIR a 1.2%. El BTR compite por suelo de mercado solo si se combinan neutralidad del IGV, una prima de renta de al menos 20% demostrada y un cap de salida de 6.0% o menos. Fuera de eso, es viable en nichos donde el suelo no se paga a precio BTS (terreno aportado, joint ventures, tierra en balance). Los edificios ya lanzados en Miraflores, con rentas de oferta ~50% sobre el promedio de Lima Moderna, coinciden con ese mapa: producto de 40-60 m², estrato medio-alto, Lima Top.

### 2. 👉 [¿Puede la vivienda en renta ayudar a cerrar la brecha de vivienda en Lima y Callao?](articulo/btr-y-brecha-de-vivienda-lima-callao.md)

**Conclusión:** el multifamily de mercado no llega a la brecha, y subsidiar el modelo encarecería el suelo. Puede contribuir, en escala acotada, si el terreno sale del negocio:

- el Estado aporta suelo bien ubicado en derecho de superficie por 45 años, a valor de mercado, y lo cobra en segundo lugar en la cascada de retornos;
- el alquiler de vivienda de empresas tiene paridad de IGV con el de la persona natural;
- el capital entra por etapas, con un costo combinado de ~7.5%;
- al vencimiento, el Estado relicita el edificio, no lo vende.

Así los inversionistas cobran 7.5% y el Estado recupera su terreno con una TIR de 6.66% (VPN +S/ 160 por m² a su costo de 6.3%), con un margen estrecho. La periferia no cierra. La asequibilidad sale de un bono visible a la familia (Ley 30952), que la prepara para pasar a Techo Propio o al Nuevo Crédito Mivivienda.

Todo lo demás en este repositorio está al servicio del artículo:

- **[Memoria de cálculo del artículo 1](articulo/memoria-de-calculo.md)** y **[del artículo 2](articulo/memoria-de-calculo-suelo-publico.md):** fórmulas, supuestos con fuente y resultados, para que un tercero pueda revisar cada número.
- **Hojas de cálculo con fórmulas:** [artículo 1](modelo/memoria-de-calculo.xlsx) y [artículo 2](modelo/memoria-suelo-publico.xlsx). Supuestos editables; reproducen los modelos en Python.
- **Modelos en Python:** [`modelo_multifamily.py`](modelo/modelo_multifamily.py) y [`modelo_suelo_publico.py`](modelo/modelo_suelo_publico.py). Ver [modelo/README.md](modelo/README.md).
- **[Revisión de pares](articulo/revision-de-pares.md):** hallazgos por ronda, correcciones y observaciones abiertas.
- **[Validación normativa](articulo/validacion-normativa.md):** qué normas se contrastaron, cuáles están pendientes y cómo afecta cada una al modelo.
- **Modelos estándar:** los documentos que hacen operable la estructura cuando el proyecto ya cierra (ver abajo). Sus valores referenciales están calibrados con el modelo.

## Documentos de soporte

### Validación

| Documento | Descripción |
|---|---|
| [Memoria de cálculo, artículo 1](articulo/memoria-de-calculo.md) | Fórmulas, supuestos y resultados del modelo BTS/BTR |
| [Memoria de cálculo, artículo 2](articulo/memoria-de-calculo-suelo-publico.md) | Cascada, plazos y asequibilidad del esquema de suelo público |
| [Hoja Excel, artículo 1](modelo/memoria-de-calculo.xlsx) | Modelo con fórmulas vivas y supuestos editables |
| [Hoja Excel, artículo 2](modelo/memoria-suelo-publico.xlsx) | Cascada anual con fórmulas vivas, escenarios y asequibilidad |
| [Revisión de pares](articulo/revision-de-pares.md) | Rondas de revisión, correcciones y temas abiertos |
| [Validación normativa del artículo](articulo/validacion-normativa.md) | Normas contrastadas con el corpus, normas pendientes y su efecto en el modelo |

### Modelos estándar que viabilizan la propuesta

Si cada banco, fondo, FIBRA, tasador y administrador negocia sus propios documentos, cada operación cuesta más y tarda más. Estos modelos los puede adoptar cualquier empresa sin modificar las cláusulas núcleo.

| # | Documento | Para qué sirve |
|---|---|---|
| 01 | [Préstamo Mini-Perm](contratos/01-prestamo-mini-perm.md) | Financia el edificio terminado durante la colocación y la estabilización, hasta su venta o refinanciamiento |
| 02 | [Compraventa futura (Forward Purchase Agreement)](contratos/02-compraventa-futura-fpa.md) | Una FIBRA, un FIRBI o un fondo se compromete a comprar el edificio terminado y estabilizado |
| 03 | [Arrendamiento de vivienda en edificio de renta](contratos/03-arrendamiento-vivienda-en-renta.md) | Contrato uniforme por unidad: cedible, pagado en cuenta del fideicomiso, con reajuste anual |
| 04 | [Formato de reporte de desempeño (rent roll)](contratos/04-formato-reporte-desempeno-rent-roll.md) | Campos e indicadores únicos para financistas, compradores, tasadores y fiduciarios |
| 05 | [Fideicomiso de administración y garantía](contratos/05-fideicomiso-administracion-garantia.md) | Cascada de las rentas, reservas y venta extrajudicial |
| 06 | [Acuerdo directo (Direct Agreement)](contratos/06-acuerdo-directo-financista.md) | Aviso, periodo de cura y sustitución del vendedor frente al financista |
| 07 | [Financiamiento puente de terreno (Land Bridge Note)](contratos/07-land-bridge-note.md) | Deuda de terreno y licencias con desembolsos atados a hitos |
| 08 | [Acuerdo entre acreedores (Intercreditor)](contratos/08-acuerdo-entre-acreedores.md) | Prelación, bloqueo de pagos, periodo de espera y derechos del acreedor mezzanine |
| 09 | [Administración de edificio (Property Management)](contratos/09-administracion-edificio.md) | Indicadores de servicio, honorario ligado al NOI y reemplazo por el financista |
| 10 | [Construcción (adaptación NEC ECC)](contratos/10-construccion-nec-ecc.md) | Suma alzada o precio objetivo, aviso temprano, eventos compensables y criterio de ciclo de vida |
| 11 | [Metodología de tasación por enfoque de renta](contratos/11-metodologia-tasacion-enfoque-renta.md) | Cap rate, vacancia estructural y gastos normalizados estándar; opción de plazo finito para derecho de superficie |
| 12 | [Derecho de superficie sobre suelo público](contratos/12-derecho-de-superficie-suelo-publico.md) | Cesión de suelo estatal con el valor del terreno subordinado en la cascada, reversión sin pago, relicitación, revisión decenal, unidades con bono y graduación |

Los contratos 01 a 11 incluyen una opción secundaria para operar sobre suelo público, coherente con el contrato 12 (el 07 no se necesita en ese caso).

### Cómo encajan

```
Terreno ──► [07] Land Bridge ──► [10] Construcción ──► [01] Mini-Perm ──► Venta a FIBRA / FIRBI / fondo
                                       │                     │                    ▲
                                       └──────── [05] Fideicomiso ────────────────┤
                                                   │      ▲                       │
                              [03] Arrendamientos ─┘      │              [02] Compraventa futura
                              [09] Administración ─► [04] Reporte              │
                                                          │              [06] Acuerdo directo
                              [08] Acuerdo entre acreedores · [11] Tasación (LTV y precio)

Suelo público (artículo 2):
Estado ──► [12] Derecho de superficie ──► [10] Construcción ──► [01] Mini-Perm ──► [02] Cesión a tenedor de largo plazo
              │  cascada: inversionistas → Estado → excedente (en [05])        │
              └─ bono a la familia ──► [03] Arrendamiento con bono ──► [04]/[09] reporte de graduación
```

## Cómo usar los modelos

Todos los modelos siguen el estilo de los contratos estándar **NEC**: redacción directa, en tiempo presente, sin remisiones cruzadas entre cláusulas.

1. **Cláusulas núcleo.** Son iguales para todos los usuarios. No se modifican.
2. **Datos del Contrato.** Allí va todo lo que cambia de una operación a otra: montos, plazos, tasas e indicadores. Los valores marcados como *referencial* son solo orientativos.
3. **Opciones secundarias (X1, X2, ...).** Las partes eligen las que usan y las listan en los Datos del Contrato.
4. **Base legal de referencia.** Al final de cada modelo hay una tabla de normas. Las normas marcadas *"No incluida: verificar"* deben revisarse contra su texto vigente antes de usar el modelo.

> **Aviso importante.** Estos documentos son modelos de referencia, no asesoría legal, tributaria ni financiera. Antes de usarlos en una operación real, cada parte debe revisarlos con sus asesores.

## Licencia y atribución

© 2026 Juan Germán Gayoso Arnillas. Esta obra está bajo licencia **[Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.es)**. El texto completo está en [LICENSE](LICENSE).

**Puedes:**
- copiar y redistribuir el material en cualquier medio o formato; y
- adaptarlo, transformarlo y construir a partir de él.

**Bajo estas condiciones:**
- **Atribución.** Debes dar crédito al autor, enlazar la licencia e indicar si hiciste cambios.
- **No comercial.** No puedes usar el material con fines comerciales.

Una empresa que use un modelo para documentar sus propias operaciones no está vendiendo el modelo. Aun así, conviene que verifique con su asesor si su uso concreto califica como no comercial según la licencia. Para usos comerciales, como vender o licenciar los modelos o incluirlos en un producto pagado, se requiere autorización escrita del autor.

**Cita sugerida:**

> Gayoso Arnillas, Juan Germán (2026). *Multifamily Viabilización: documentos estándar para vivienda en renta en el Perú*. https://github.com/JuanGayoso/Multifamily_Viabilizacion. Licencia CC BY-NC 4.0.
