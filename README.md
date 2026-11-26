# Multifamily Viabilización

**Documentos estándar para financiar y operar vivienda en renta (Build-to-Rent / Multifamily) en el Perú, sin subsidios y con neutralidad competitiva.**

Autor: **Juan Germán Gayoso Arnillas** · Versión 1.0 · Noviembre 2026

[![Licencia: CC BY-NC 4.0](https://img.shields.io/badge/Licencia-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## De qué trata

El proyecto parte de una tesis: la vivienda en renta no necesita subsidios que le den ventaja sobre los proyectos de venta (Build-to-Sell) en la competencia por el suelo. Su viabilidad tiene que salir del modelo de negocio y de una buena ingeniería financiera.

Una parte importante de esa ingeniería es **reducir el costo de transacción**. Si cada banco, fondo, FIBRA, tasador y administrador negocia sus propios documentos, cada operación cuesta más y tarda más. Por eso este repositorio ofrece un juego completo de **modelos estandarizados**, que cualquier empresa puede adoptar sin modificar las cláusulas núcleo.

## Contenido

### Artículo

| Documento | Descripción |
|---|---|
| [Financiamiento de Vivienda en Renta en el Perú: Neutralidad Competitiva e Ingeniería Financiera](articulo/financiamiento-vivienda-en-renta-peru.md) | Diagnóstico, tesis de neutralidad competitiva y propuesta de instrumentos financieros y documentales |

### Modelos estándar

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
| 11 | [Metodología de tasación por enfoque de renta](contratos/11-metodologia-tasacion-enfoque-renta.md) | Cap rate, vacancia estructural y gastos normalizados estándar |

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
