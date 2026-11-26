# Formato Estándar de Reporte de Desempeño de Edificio de Vivienda en Renta (Rent Roll)

Versión estándar 1.0 · Por: Juan Germán Gayoso Arnillas · 2026-11-25

## Nota de uso

Este formato fija cómo un edificio de vivienda en renta informa su desempeño a financistas, compradores, tasadores, fiduciarios y aseguradores. Un mismo formato para todo el mercado permite comparar edificios, calcular los indicadores de los contratos de financiamiento sin discusiones y armar series históricas que reduzcan el costo de capital del sector.

**Quién lo usa.** El Administrador lo prepara. El Propietario lo firma y lo envía. El Agente del financiamiento, el fiduciario, el comprador bajo una compraventa futura y el tasador lo reciben.

**Cómo se arma.** El formato tiene cuatro partes:

1. **Reglas de preparación.** Son iguales para todos los usuarios. No se modifican.
2. **Tablas estándar.** Cada tabla tiene campos obligatorios. El usuario puede agregar columnas al final, pero no quita ni renombra las existentes.
3. **Definiciones de indicadores.** Fórmulas únicas para Ocupación, morosidad, rotación, Ingreso Operativo Neto y DSCR.
4. **Datos del Reporte.** Lo que cambia de un edificio a otro.

**Advertencia.** Este es un formato de referencia. Cuando un contrato de financiamiento define un indicador de otra forma, prevalece la definición del contrato, y el reporte lo indica en una nota.

## 1. Reglas de preparación

**10. Acciones**

10.1 El Administrador prepara el reporte con la información de su sistema de gestión y de los estados de la Cuenta Recaudadora.

10.2 El Propietario revisa el reporte, lo firma y lo envía a los destinatarios indicados en los Datos del Reporte.

10.3 Los destinatarios usan el reporte solo para administrar su financiamiento, su inversión o su encargo.

**11. Definiciones**

11.1 En este formato, los términos con mayúscula inicial tienen el significado siguiente:

- **Administrador** es la empresa que gestiona el Edificio.
- **Cuenta Recaudadora** es la cuenta donde se depositan las Rentas.
- **Edificio** es el inmueble descrito en los Datos del Reporte.
- **Periodo** es el mes calendario que cubre el reporte.
- **Propietario** es el titular del Edificio o el fideicomiso que lo tiene.
- **Renta Contratada** es la renta mensual vigente según cada contrato de arrendamiento, sin Servicios.
- **Renta Cobrada** es la renta efectivamente depositada en la Cuenta Recaudadora en el Periodo, sin importar a qué mes corresponde.
- **Renta de Mercado** es la renta que el Administrador estima para una unidad vacante, sustentada en las tres últimas colocaciones comparables.
- **Unidad** es cada departamento del Edificio. Los estacionamientos y depósitos se reportan aparte.

**12. Frecuencia y plazos**

12.1 El reporte mensual se envía dentro de los quince días siguientes al cierre del Periodo.

12.2 El reporte trimestral agrega el estado de resultados del Edificio y el cálculo de los indicadores de los últimos doce meses.

12.3 El reporte anual agrega los estados financieros auditados del Propietario, cuando existen.

**13. Formato del archivo**

13.1 El reporte se envía en hoja de cálculo editable (.xlsx o .csv), con una pestaña por tabla, y en PDF firmado.

13.2 Las fechas se escriben en formato AAAA-MM-DD. Los montos se escriben sin separador de miles y con punto decimal. La moneda se indica en una columna.

13.3 Cada Unidad conserva el mismo código en todos los reportes.

**14. Confidencialidad y datos personales**

14.1 El reporte no identifica a los arrendatarios por nombre ni documento. Usa un código anónimo por contrato.

14.2 Los destinatarios guardan reserva del reporte y no lo entregan a terceros sin autorización del Propietario, salvo a sus auditores, reguladores y asesores.

**15. Aviso temprano**

15.1 El Administrador avisa al Propietario y a los destinatarios, sin esperar el reporte mensual, apenas conoce un hecho que pueda reducir la Renta Cobrada en más del porcentaje indicado en los Datos del Reporte, o que afecte la seguridad o habitabilidad del Edificio.

## 2. Tablas estándar

**20. Tabla A: Rent roll por Unidad**

| Campo | Descripción |
|---|---|
| codigo_unidad | Código fijo de la Unidad |
| tipologia | Estudio, 1D, 2D, 3D |
| area_m2 | Área techada |
| piso | Número de piso |
| estado | Ocupada / Vacante disponible / Vacante en preparación / Fuera de servicio |
| codigo_contrato | Código anónimo del contrato vigente |
| fecha_inicio | Inicio del contrato vigente |
| fecha_fin | Vencimiento del contrato vigente |
| moneda | PEN / USD |
| renta_contratada | Renta mensual vigente |
| renta_mercado | Renta de Mercado, si la Unidad está vacante |
| concesiones | Meses de gracia o descuentos vigentes, en monto mensual equivalente |
| garantia_recibida | Monto de garantía en poder del Propietario |
| saldo_vencido | Rentas vencidas y no pagadas al cierre |
| dias_atraso | Días del saldo vencido más antiguo |
| ultimo_reajuste | Fecha y porcentaje del último reajuste |
| tipo_arrendatario | Persona natural / Corporativo |

**21. Tabla B: Movimientos del Periodo**

| Campo | Descripción |
|---|---|
| codigo_unidad | Código de la Unidad |
| tipo_movimiento | Ingreso / Salida / Renovación / Terminación anticipada / Desalojo |
| fecha | Fecha del movimiento |
| renta_anterior | Renta del contrato que termina, si aplica |
| renta_nueva | Renta del contrato que inicia, si aplica |
| dias_vacancia | Días entre la salida anterior y el ingreso |
| costo_preparacion | Gasto de puesta a punto de la Unidad |

**22. Tabla C: Antigüedad de la morosidad**

| Tramo | Número de contratos | Monto |
|---|---|---|
| 1 a 30 días |  |  |
| 31 a 60 días |  |  |
| 61 a 90 días |  |  |
| Más de 90 días |  |  |
| En proceso de restitución |  |  |

**23. Tabla D: Estado de resultados del Edificio**

| Concepto | Periodo | Acumulado del año | Presupuesto del año |
|---|---|---|---|
| Renta potencial bruta (todas las Unidades a Renta Contratada o de Mercado) |  |  |  |
| (–) Vacancia |  |  |  |
| (–) Concesiones |  |  |  |
| (–) Incobrables |  |  |  |
| Otros ingresos (estacionamientos, depósitos, servicios) |  |  |  |
| **Ingreso efectivo** |  |  |  |
| (–) Administración del Edificio |  |  |  |
| (–) Mantenimiento y reparaciones |  |  |  |
| (–) Servicios no recuperados |  |  |  |
| (–) Seguros |  |  |  |
| (–) Impuesto predial y arbitrios |  |  |  |
| (–) Marketing y colocación |  |  |  |
| **Ingreso Operativo Neto** |  |  |  |
| (–) Reserva de mantenimiento mayor |  |  |  |
| (–) Servicio de deuda |  |  |  |
| **Flujo disponible para el Propietario** |  |  |  |

**24. Tabla E: Indicadores**

| Indicador | Periodo | Últimos 12 meses | Mínimo o máximo contractual |
|---|---|---|---|
| Ocupación física |  |  |  |
| Ocupación económica |  |  |  |
| Morosidad |  |  |  |
| Rotación anual |  |  |  |
| Días promedio de vacancia |  |  |  |
| Tasa de renovación |  |  |  |
| Margen operativo (Ingreso Operativo Neto / Ingreso efectivo) |  |  |  |
| DSCR |  |  |  |
| LTV (con la última tasación) |  |  |  |
| Saldo de reservas |  |  |  |

**25. Tabla F: Mantenimiento mayor y eventos**

| Campo | Descripción |
|---|---|
| fecha | Fecha del evento o la obra |
| descripcion | Qué pasó o qué se hizo |
| monto | Costo |
| fuente | Reserva / Seguro / Propietario |
| estado | Abierto / Cerrado |

## 3. Definiciones de indicadores

**30. Fórmulas**

30.1 **Ocupación física** = Unidades ocupadas al cierre / total de Unidades. Una Unidad fuera de servicio cuenta en el denominador.

30.2 **Ocupación económica** = Renta Cobrada del Periodo / renta potencial bruta del Periodo.

30.3 **Morosidad** = saldo vencido con más de treinta días / Renta Contratada mensual total.

30.4 **Rotación anual** = salidas de los últimos doce meses / número promedio de Unidades ocupadas en esos meses.

30.5 **Tasa de renovación** = contratos renovados / contratos que vencieron en los últimos doce meses.

30.6 **Ingreso Operativo Neto** = ingreso efectivo menos gastos operativos, sin restar servicio de deuda, depreciación, reserva de mantenimiento mayor ni Impuesto a la Renta.

30.7 **DSCR** = Ingreso Operativo Neto de los últimos doce meses / servicio de deuda de esos mismos doce meses.

30.8 **LTV** = saldo de la deuda / valor del Edificio según la última tasación por enfoque de renta.

**31. Conciliación**

31.1 La Renta Cobrada del reporte coincide con los depósitos del Periodo en el estado de la Cuenta Recaudadora. Toda diferencia se explica en una nota.

31.2 El número de Unidades de la Tabla A coincide con la declaratoria de edificación inscrita.

## 4. Firma y responsabilidad

**40. Declaración**

40.1 El Propietario declara, con su firma, que el reporte refleja fielmente la información de su sistema de gestión y de la Cuenta Recaudadora.

40.2 Si el Propietario descubre un error en un reporte enviado, lo corrige en el reporte siguiente y lo comunica a los destinatarios.

**41. Auditoría**

41.1 Los destinatarios indicados en los Datos del Reporte pueden revisar, una vez al año y a su costo, los contratos y estados de cuenta que sustentan el reporte, con aviso de diez días hábiles.

## Opciones secundarias

**Opción X1. Indicadores ambientales**

X1.1 El reporte agrega consumo de energía (kWh/m²), consumo de agua (m³/Unidad) y estado de la certificación EDGE o equivalente.

**Opción X2. Envío automatizado**

X2.1 El Administrador envía las Tablas A a E por conexión directa a la plataforma del destinatario, en el formato de datos indicado en los Datos del Reporte.

**Opción X3. Revisión por tercero**

X3.1 Un auditor independiente revisa el reporte trimestral antes de su envío.

## Datos del Reporte

| Dato | Valor |
|---|---|
| Edificio (nombre, dirección, partida registral, número de Unidades) |  |
| Propietario (razón social, RUC) |  |
| Administrador (razón social, RUC, responsable) |  |
| Destinatarios y correos |  |
| Contratos que exigen el reporte (financiamiento, compraventa futura, fideicomiso) |  |
| Moneda de reporte |  |
| Umbral de aviso temprano (% de Renta Cobrada) | 5% (referencial) |
| Primer Periodo reportado |  |
| Opciones secundarias elegidas |  |

Los valores marcados como referenciales son orientativos.

## Base legal de referencia

| Materia | Norma | Estado en el corpus |
|---|---|---|
| Protección de datos personales | Ley 29733 | No incluida: verificar |
| Información a inversionistas de FIBRA y FIRBI | Ley 30532 y DS 336-2018-EF; normas de la SMV | Corpus: Ley 30532 y DS 336-2018-EF vigentes; normas SMV no incluidas: verificar |
| Tasación por enfoque de renta | Reglamento Nacional de Tasaciones | No incluida: verificar |

Antes de usar el formato, las normas marcadas como no incluidas deben revisarse contra su texto vigente.
