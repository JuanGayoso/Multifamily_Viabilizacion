# Contrato Modelo de Derecho de Superficie sobre Suelo Público para Vivienda en Renta

Versión estándar 1.0 · Por: Juan Germán Gayoso Arnillas · 2026-11-26

## Nota de uso

Este modelo sirve para que una entidad pública con suelo bien ubicado lo ceda en derecho de superficie a un operador privado. El operador construye y opera un edificio de vivienda en renta. El Estado no vende ni regala el terreno:

- **Valoración:** lo aporta a valor de mercado.
- **Cobro:** lo cobra en segundo lugar en la cascada de retornos, después de los inversionistas y antes del excedente.
- **Vencimiento:** recibe el edificio sin pago al final del primer periodo y licita un segundo periodo.

Es el instrumento que propone el artículo [*¿Puede la vivienda en renta ayudar a cerrar la brecha de vivienda en Lima y Callao?*](../articulo/btr-y-brecha-de-vivienda-lima-callao.md). Los valores referenciales salen del modelo [`modelo/modelo_suelo_publico.py`](../modelo/modelo_suelo_publico.py); ver [`articulo/memoria-de-calculo-suelo-publico.md`](../articulo/memoria-de-calculo-suelo-publico.md).

**Lo que este contrato no hace.**

- No da al operador un descuento sobre el terreno ni una renta garantizada.
- No financia descuentos de alquiler con el terreno. Si la política pública quiere un alquiler menor para ciertos hogares, lo paga un bono a la familia, visible en el presupuesto (cláusula 60).
- No prevé la conversión del edificio a venta por unidades.

**Cuándo funciona.** El modelo publicado muestra que el esquema cierra sin subsidio solo con cuatro condiciones juntas:

1. alquiler de vivienda exonerado del IGV (paridad con la persona natural);
2. costo combinado del capital cercano a 7.5% en soles;
3. primer periodo de 45 años;
4. una ubicación con alquileres de mercado al menos iguales al promedio de Lima Moderna.

En ubicaciones con alquileres 20% menores no cierra con ningún plazo legal. La entidad debe verificar estas condiciones con un modelo financiero propio antes de licitar.

**Cómo se arma.** Como los demás modelos del repositorio:

- **Cláusulas núcleo:** no se modifican.
- **Datos del Contrato:** recogen lo que cambia de un proyecto a otro.
- **Opciones secundarias:** las partes eligen las que usan.

Cada cláusula dice quién hace qué, en tiempo presente. Los términos definidos van con mayúscula inicial.

**Advertencia.** Este es un modelo de referencia. Antes de usarlo, la entidad verifica con un abogado administrativista estos cuatro puntos:

- si la operación se rige por la normativa del Sistema Nacional de Bienes Estatales (Ley 29151), por el régimen de Asociaciones Público Privadas (D.Leg. 1362) o por otra norma especial;
- qué autorizaciones necesita;
- si la reversión sin reembolso requiere un pacto expreso (Código Civil, art. 1030);
- cómo se inscribe el derecho de superficie y se constituyen garantías sobre él.

Ver "Base legal de referencia".

## 1. Disposiciones generales

**10. Acciones**

10.1 El Concedente y el Superficiario actúan como se indica en este contrato.

10.2 Las partes actúan de buena fe y en un espíritu de confianza y cooperación.

**11. Definiciones**

11.1 En este contrato, los términos con mayúscula inicial tienen el significado siguiente:

- **Bono** es el bono de arrendamiento para vivienda (Ley 30952) u otro subsidio a la demanda que el Estado paga a un Hogar Elegible, indicado en los Datos del Contrato.
- **Cascada** es el orden de aplicación del Flujo del Proyecto descrito en la cláusula 31.
- **Comisión Técnica** es el panel de tres expertos independientes que conduce la Revisión Decenal.
- **Concedente** es la entidad pública titular del Terreno.
- **Edificio** es la edificación de vivienda en renta, con sus áreas comunes y equipamiento, que el Superficiario construye en el Terreno.
- **Excedente** es el Flujo del Proyecto que queda después de pagar el Saldo de los Inversionistas y el Saldo del Concedente.
- **Flujo del Proyecto** es, en cada año, la suma de ingresos cobrados menos costos de operación, reserva de reposición, renovaciones e inversión de obra, antes de servicio de deuda e Impuesto a la Renta, calculada según el Anexo 3.
- **Hogar Elegible** es el hogar que cumple los requisitos del Bono.
- **Inversionistas** son los que aportan capital o deuda al Proyecto, en cualquiera de sus Etapas.
- **Etapa** es cada fase del Proyecto: Desarrollo, Estabilización y Largo Plazo, definidas en la cláusula 50.
- **Periodo** es el plazo del derecho de superficie indicado en los Datos del Contrato (T1).
- **Relicitación** es el concurso que el Concedente convoca para un segundo periodo de explotación del Edificio después del Periodo.
- **Retorno de los Inversionistas** es la tasa anual indicada en los Datos del Contrato (r_inv).
- **Retorno del Concedente** es la tasa anual indicada en los Datos del Contrato (r_est).
- **Revisión Decenal** es el procedimiento de la sección 7.
- **Saldo de los Inversionistas** es la suma de los aportes de los Inversionistas capitalizada al Retorno de los Inversionistas, menos lo que la Cascada les ha pagado.
- **Saldo del Concedente** es el Valor del Terreno capitalizado al Retorno del Concedente desde la Fecha de Entrega, menos lo que la Cascada le ha pagado.
- **Terreno** es el inmueble descrito en los Datos del Contrato.
- **Valor del Terreno** es el valor de mercado del Terreno a la Fecha de Entrega, según la tasación de la cláusula 30.

**12. Interpretación y ley aplicable**

12.1 Este contrato se rige por la ley peruana.

12.2 Si hay contradicción entre las cláusulas núcleo y los Datos del Contrato, prevalecen los Datos del Contrato, salvo en las cláusulas 31 (Cascada), 40 (reversión sin pago) y 70 (límites de la Revisión Decenal), que prevalecen siempre.

**13. Comunicaciones**

13.1 Toda comunicación se hace por escrito al correo electrónico indicado en los Datos del Contrato.

**14. Aviso temprano**

14.1 Cada parte avisa a la otra apenas conoce un hecho que pueda retrasar la obra, reducir la renta, aumentar el costo o afectar el valor del Edificio al final del Periodo.

14.2 Las partes se reúnen dentro de los diez días siguientes al aviso para acordar cómo reducir el efecto.

## 2. Objeto y plazo

**20. Constitución del derecho de superficie**

20.1 El Concedente constituye a favor del Superficiario un derecho de superficie sobre el Terreno por el Periodo, para construir y operar el Edificio como vivienda en renta.

20.2 El Superficiario usa el Edificio solo para vivienda en renta y los usos complementarios indicados en los Datos del Contrato (comercio de primer piso, estacionamientos, servicios). No vende unidades ni constituye propiedad horizontal para venta.

20.3 El Concedente entrega el Terreno libre de ocupantes, cargas y gravámenes en la Fecha de Entrega indicada en los Datos del Contrato.

20.4 Las partes inscriben el derecho de superficie en el Registro de Predios dentro del plazo indicado en los Datos del Contrato. Los gastos son del Superficiario.

**21. Contraprestación**

21.1 El Superficiario no paga una renta fija por el Terreno. La contraprestación del Concedente son los pagos que recibe por la Cascada (cláusula 31), el Excedente que le corresponde y el valor de la Relicitación (cláusula 80).

**22. Criterios urbanos del Edificio**

22.1 El Superficiario diseña y opera el Edificio conforme a los criterios urbanos indicados en los Datos del Contrato: densidad, mezcla de tipologías, primer piso activo, accesibilidad, estacionamientos de bicicletas, eficiencia energética y conexión con el transporte público. Estos criterios provienen del plan de desarrollo urbano aplicable (en Lima, el PLANMET 2040 y los planes distritales).

## 3. Valor del Terreno y Cascada

**30. Valor del Terreno**

30.1 El Valor del Terreno es el valor de mercado del Terreno para su mejor uso alternativo, calculado por el método residual de un proyecto de vivienda para venta con la tasa de retorno de mercado del promotor.

30.2 Lo determina un tasador independiente, inscrito en el registro de peritos de la SBS y elegido de común acuerdo, antes de la firma. El Valor del Terreno figura en los Datos del Contrato y no se ajusta después.

**31. Cascada**

31.1 Cada año, el Fiduciario (cláusula 100) aplica el Flujo del Proyecto en este orden:

(a) **Primero**, a los Inversionistas, hasta reducir a cero el Saldo de los Inversionistas.

(b) **Segundo**, al Concedente, hasta reducir a cero el Saldo del Concedente.

(c) **Tercero**, el Excedente se reparte entre el Concedente y el Superficiario en la proporción indicada en los Datos del Contrato.

31.2 Si el Flujo del Proyecto de un año es negativo (por obra o por renovaciones), lo aportan los Inversionistas y se suma al Saldo de los Inversionistas.

31.3 El servicio de la deuda del Proyecto se paga con lo que la Cascada asigna a los Inversionistas. Los financistas no tienen prelación sobre el Concedente respecto del Saldo del Concedente, salvo lo previsto en la cláusula 101 para la ejecución de garantías.

31.4 El Fiduciario informa al Concedente y al Superficiario, cada trimestre, los saldos de la Cascada calculados según el Anexo 3.

**32. Retorno del Concedente**

32.1 El Retorno del Concedente es la tasa de financiamiento del Tesoro Público en soles para un plazo comparable a la Fecha de Entrega, según la curva publicada por el MEF o el BCRP. Figura en los Datos del Contrato y no se ajusta después.

**33. Saldo no recuperado**

33.1 Si al final del Periodo el Saldo del Concedente no está en cero, la diferencia se descuenta del valor que la Relicitación paga al Superficiario, si lo hay (cláusula 81), y el resto se extingue. El Concedente asume ese riesgo a cambio de la reversión del Edificio sin pago.

## 4. Desarrollo y operación

**40. Reversión sin pago**

40.1 Al vencer el Periodo, el Edificio, sus instalaciones y su equipamiento pasan a propiedad del Concedente sin que el Concedente pague reembolso ni compensación alguna. Las partes pactan expresamente esta reversión sin reembolso, conforme al artículo 1030 del Código Civil.

40.2 El Superficiario entrega el Edificio en el estado de mantenimiento exigido por el Anexo 4, con las renovaciones del plan de la cláusula 43 ejecutadas.

**41. Construcción**

41.1 El Superficiario construye el Edificio conforme al proyecto aprobado, la licencia de edificación y el plazo indicado en los Datos del Contrato.

41.2 El Superficiario contrata la obra con un contrato de precio objetivo o de suma alzada con garantías de fiel cumplimiento (ver contrato 10 del repositorio).

**42. Operación**

42.1 El Superficiario opera el Edificio con un administrador profesional (ver contrato 09) y cumple los indicadores de servicio del Anexo 4.

42.2 El Superficiario fija la renta de cada unidad sin exceder la renta máxima indicada en los Datos del Contrato. La renta máxima se reajusta cada año por la variación del Índice de Precios al Consumidor de Lima Metropolitana.

**43. Plan de renovaciones y reserva**

43.1 El Superficiario ejecuta las renovaciones mayores en los años y por los montos mínimos indicados en los Datos del Contrato.

43.2 El Superficiario deposita cada año en la cuenta de reserva del Fideicomiso el porcentaje de la renta indicado en los Datos del Contrato.

43.3 Las renovaciones que caen en los dos últimos años del Periodo no se ejecutan. Su monto se descuenta del valor de la Relicitación y se informa en las bases.

## 5. Capital por etapas

**50. Etapas**

50.1 El Proyecto tiene tres Etapas:

- **Desarrollo:** desde la firma hasta la conformidad de obra.
- **Estabilización:** desde la conformidad de obra hasta que la ocupación llega a la ocupación estabilizada durante dos trimestres seguidos.
- **Largo Plazo:** desde el fin de la Estabilización hasta el fin del Periodo.

**51. Cesión entre Etapas**

51.1 El Superficiario puede ceder su posición contractual, o las acciones de la sociedad superficiaria, a un Cesionario Calificado al terminar cualquier Etapa, con aviso previo de treinta días al Concedente.

51.2 Es Cesionario Calificado quien cumple los requisitos de experiencia y solvencia indicados en los Datos del Contrato. Una FIBRA, un fondo de inversión, una AFP o una aseguradora que contrate un administrador con la experiencia requerida es Cesionario Calificado.

51.3 El Concedente solo puede oponerse si el cesionario no es Cesionario Calificado o está impedido de contratar con el Estado.

51.4 La cesión no cambia la Cascada, el Saldo de los Inversionistas ni el Saldo del Concedente.

**52. Compromiso de capital de largo plazo**

52.1 En la oferta de la licitación, el Superficiario acredita el compromiso del inversionista de Largo Plazo de adquirir su posición al fin de la Estabilización, a un precio calculado según el Anexo 5.

52.2 El desarrollador cobra un honorario de desarrollo y un incentivo por costo y plazo, indicados en los Datos del Contrato, pagados por el Superficiario.

## 6. Unidades con Bono y graduación

**60. Unidades para Hogares Elegibles**

60.1 El Superficiario destina a Hogares Elegibles con Bono el porcentaje de unidades indicado en los Datos del Contrato, distribuidas en todo el Edificio y sin diferencias de calidad.

60.2 Los Hogares Elegibles pagan la renta de mercado del Edificio. El Bono cubre parte de ella; el resto lo paga el hogar. El Superficiario no da descuentos financiados con el Terreno ni con la Cascada.

60.3 Si no hay Hogares Elegibles en lista de espera, el Superficiario puede arrendar la unidad a otro inquilino por un plazo no mayor de un año.

**61. Graduación**

61.1 El Superficiario, por medio del administrador:

(a) verifica cada año el ingreso de los Hogares Elegibles con la entidad que paga el Bono;

(b) reporta, con el consentimiento del hogar, el historial de pago puntual de la renta a las centrales de riesgo;

(c) informa a cada hogar, un año antes del fin del Bono, sobre los programas de vivienda a los que puede acceder (Techo Propio, Nuevo Crédito Mivivienda) y el saldo de su cuenta de ahorro.

61.2 Al terminar el Bono, el hogar puede seguir como inquilino a renta de mercado. El Superficiario no está obligado a renovar el contrato en condiciones distintas.

61.3 El Superficiario reporta cada semestre los indicadores de graduación del Anexo 6 (ver contrato 04, tabla de unidades con Bono).

## 7. Revisión Decenal

**70. Procedimiento y límites**

70.1 Cada diez años desde la Fecha de Entrega, la Comisión Técnica compara el desempeño del Proyecto con el modelo financiero de la oferta: rentas, ocupación, opex, costo de capital y estado del Edificio.

70.2 La Comisión Técnica puede recomendar ajustes en:

- el reparto del Excedente;
- la renta máxima;
- el porcentaje de unidades con Bono;
- el plan de renovaciones;
- los criterios urbanos de operación.

70.3 Ningún ajuste puede:

(a) reducir el Saldo de los Inversionistas ya devengado ni cambiar el Retorno de los Inversionistas;

(b) cambiar el orden de la Cascada ni el Retorno del Concedente;

(c) prorrogar el Periodo más allá del máximo legal.

70.4 Los ajustes recomendados rigen si ninguna parte los objeta en treinta días. Si alguna los objeta, la controversia se resuelve según la sección 14.

70.5 Cada parte nombra un experto y los dos nombran al tercero. Los honorarios se pagan con cargo al Flujo del Proyecto.

## 8. Relicitación al vencimiento

**80. Relicitación**

80.1 Tres años antes del fin del Periodo, el Concedente convoca la Relicitación de un segundo periodo de explotación por el plazo indicado en los Datos del Contrato (T2).

80.2 Las bases informan el estado del Edificio, el rent roll de los últimos tres años y las renovaciones pendientes.

80.3 El adjudicatario paga al Concedente el monto de su oferta.

**81. Participación del Superficiario**

81.1 El Superficiario puede presentarse a la Relicitación en igualdad de condiciones.

81.2 Si al final del Periodo el Saldo del Concedente está en cero y el Superficiario cumplió el plan de renovaciones, recibe el porcentaje del valor de la Relicitación indicado en los Datos del Contrato, como incentivo para entregar el Edificio en buen estado. Este porcentaje es referencialmente cero en el caso base.

**82. Sin conversión a venta**

82.1 Ninguna disposición de este contrato faculta al Concedente ni al Superficiario a vender el Edificio por unidades al final del Periodo. El Edificio se mantiene como vivienda en renta mientras el Concedente no decida otro uso público por norma con rango de ley.

## 9. Equilibrio y cambio de ley

**90. Causas tasadas**

90.1 Las partes solo pueden pedir el restablecimiento del equilibrio económico del contrato por:

(a) un cambio de ley posterior a la firma que afecte específicamente a la vivienda en renta o al derecho de superficie: por ejemplo, la derogación de la exoneración del IGV del alquiler de vivienda o un control de rentas;

(b) fuerza mayor no asegurable;

(c) un acto del Concedente que no esté previsto en el contrato.

90.2 El riesgo comercial (renta, ocupación, costo de obra, costo del capital) es del Superficiario y no habilita el restablecimiento.

90.3 El restablecimiento procede si el efecto acumulado sobre el valor presente del Flujo del Proyecto supera el umbral indicado en los Datos del Contrato. Se hace, en este orden de preferencia: ajustando el reparto del Excedente, la renta máxima o, como último recurso, el Periodo.

## 10. Fideicomiso, garantías y financistas

**100. Fideicomiso**

100.1 El Superficiario constituye un fideicomiso de administración y garantía (ver contrato 05) que recibe todos los ingresos del Edificio y aplica la Cascada.

100.2 El Concedente es fideicomisario respecto del Saldo del Concedente y de su parte del Excedente.

**101. Garantías de los financistas**

101.1 El Superficiario puede constituir hipoteca sobre el derecho de superficie inscrito y garantía mobiliaria sobre sus acciones y sus derechos de cobro, a favor de sus financistas.

101.2 La ejecución de esas garantías transfiere el derecho de superficie, con todas las obligaciones de este contrato, a un Cesionario Calificado. No afecta el Saldo del Concedente ni la reversión sin pago.

101.3 El Concedente firma con los financistas un acuerdo directo (ver contrato 06) que les da aviso de incumplimiento, un periodo de cura y el derecho de sustituir al Superficiario.

## 11. Información y transparencia

**110. Información**

110.1 El Superficiario entrega al Concedente, cada trimestre, el rent roll y el reporte de desempeño estándar (contrato 04), y cada año sus estados financieros auditados y la actualización del modelo financiero.

110.2 El Concedente publica cada año, en su portal, el resumen del desempeño del Proyecto, los saldos de la Cascada y los indicadores de graduación, sin datos personales de los inquilinos.

## 12. Incumplimiento y terminación

**120. Incumplimientos del Superficiario**

120.1 Son incumplimientos graves:

- no terminar la obra en el plazo máximo indicado en los Datos del Contrato;
- destinar el Edificio a un uso distinto;
- no ejecutar las renovaciones;
- no depositar los ingresos en el Fideicomiso;
- incumplir los indicadores de servicio durante cuatro trimestres seguidos.

120.2 Ante un incumplimiento grave, el Concedente avisa al Superficiario y a los financistas. Estos tienen el periodo de cura indicado en el acuerdo directo.

120.3 Si el incumplimiento no se cura, el Concedente puede terminar el contrato. Entonces licita el derecho de superficie por el plazo que falta y paga a los Inversionistas, con lo que obtenga, el menor entre el Saldo de los Inversionistas y el precio obtenido menos los costos de la licitación y el Saldo del Concedente.

**121. Incumplimientos del Concedente y terminación por interés público**

121.1 Si el Concedente termina el contrato por interés público o por su propio incumplimiento, paga a los Inversionistas el Saldo de los Inversionistas más la deuda del Proyecto pendiente, en el plazo indicado en los Datos del Contrato.

## 13. Seguros

**130. Seguros**

130.1 El Superficiario contrata y mantiene los seguros indicados en los Datos del Contrato: todo riesgo de construcción, todo riesgo de propiedad (incluido terremoto), responsabilidad civil y lucro cesante.

130.2 El Concedente y el Fiduciario son beneficiarios o asegurados adicionales. Las indemnizaciones por daño se aplican a la reconstrucción.

## 14. Solución de controversias

**140. Trato directo, expertos y arbitraje**

140.1 Las partes intentan resolver la controversia por trato directo durante treinta días.

140.2 Las controversias técnicas o financieras (cálculo de la Cascada, Revisión Decenal, restablecimiento del equilibrio) se someten a un experto o a la Comisión Técnica, cuyo dictamen es obligatorio salvo error manifiesto.

140.3 Las demás controversias se resuelven por arbitraje de derecho, en la institución indicada en los Datos del Contrato, conforme al D.Leg. 1071 y a las reglas aplicables a las entidades públicas.

## Opciones secundarias

**Opción S1. Reparto del Excedente escalonado**

S1.1 El reparto del Excedente al Concedente sube al porcentaje indicado en los Datos del Contrato cuando la TIR del proyecto supera el umbral indicado.

**Opción S2. Cuenta de reserva de relicitación**

S2.1 Desde el año T1 − 10, el Superficiario deposita en el Fideicomiso el porcentaje de la renta indicado en los Datos del Contrato. Esa cuenta garantiza el estado del Edificio al final del Periodo. Se libera a la entrega conforme.

**Opción S3. Tramo de deuda indexado al VAC**

S3.1 La deuda de Largo Plazo puede emitirse en VAC. Los contratos de arrendamiento incluyen un reajuste anual de la renta por inflación (ver contrato 01, opción X3).

**Opción S4. Edificio verde**

S4.1 El Superficiario obtiene la certificación EDGE o equivalente antes del fin de la Estabilización y la mantiene.

## Datos del Contrato

### Parte Uno: datos que llena el Concedente

| Dato | Valor |
|---|---|
| Concedente (entidad, RUC, representante, norma que autoriza la cesión) |  |
| Terreno (dirección, partida registral, área, zonificación) |  |
| Fecha de Entrega |  |
| Valor del Terreno (S/) y tasador | Referencial: S/ 1,015 por m² vendible (Lima Moderna, nov-2026) |
| Periodo (T1) | 45 años (referencial) |
| Segundo periodo para la Relicitación (T2) | 30 años (referencial) |
| Retorno del Concedente (r_est) | 6.3% anual (referencial: bono soberano en soles) |
| Retorno de los Inversionistas (r_inv) | 7.5% anual (referencial; según la oferta) |
| Reparto del Excedente al Concedente | 50% (referencial; variable de la licitación) |
| Renta máxima inicial por m² y reajuste | Renta de mercado tasada; IPC de Lima |
| Unidades para Hogares Elegibles (% del total) | 30%-50% (referencial) |
| Bono aplicable y entidad que lo paga | Bono de Arrendamiento para Vivienda (Ley 30952); Fondo MIVIVIENDA |
| Criterios urbanos | Según el PLANMET 2040 y la zonificación |
| Plan de renovaciones (años y % del costo) | Años 20 y 35, 10% cada una (referencial) |
| Reserva de reposición | 2% de la renta (referencial) |
| Requisitos de Cesionario Calificado |  |
| Umbral para el restablecimiento del equilibrio | 10% del VP del Flujo del Proyecto (referencial) |
| Participación del Superficiario en la Relicitación | 0% (referencial) |
| Plazo de pago por terminación por interés público |  |
| Seguros y montos mínimos |  |
| Institución arbitral |  |
| Opciones secundarias elegidas y sus datos |  |
| Direcciones y correos |  |

**Nota de calibración.** Con los valores referenciales, el modelo publicado da:

- inversionistas: 7.5%, con el saldo en cero en el año 37;
- Concedente: TIR de 6.66% y VPN de +S/ 160 por m² a su costo de 6.3%.

El margen es estrecho. Un alquiler 10% menor o un costo de obra 10% mayor lo vuelven negativo. Por eso el Periodo, el reparto del Excedente y la renta deben fijarse con el modelo de cada terreno, no copiarse.

Con 36 años el VPN apenas es positivo. Con 40 queda en +S/ 30 por m² y con 50, en +S/ 268. Si el costo del capital ofertado es 8%, el plazo mínimo sube a 59 años.

### Parte Dos: datos que llena el Superficiario

| Dato | Valor |
|---|---|
| Superficiario (razón social, RUC, partida, representantes) |  |
| Desarrollador, honorario e incentivo |  |
| Inversionista de Largo Plazo comprometido y precio según el Anexo 5 |  |
| Financistas y garantías |  |
| Fiduciario |  |
| Administrador del Edificio |  |
| Plazo de obra y plazo máximo |  |
| Modelo financiero de la oferta (Anexo 3) |  |
| Direcciones y correos |  |

### Anexos estándar

1. Plano y partida del Terreno.
2. Proyecto arquitectónico y criterios urbanos.
3. Modelo financiero y método de cálculo del Flujo del Proyecto y de la Cascada.
4. Estándar de mantenimiento e indicadores de servicio.
5. Fórmula de precio del compromiso de Largo Plazo.
6. Indicadores de graduación de Hogares Elegibles.

## Base legal de referencia

| Materia | Norma | Estado |
|---|---|---|
| Derecho de superficie: plazo máximo de 99 años, transmisibilidad, reversión y reembolso salvo pacto | Código Civil, arts. 1030-1034 | Verificar texto vigente |
| Disposición y gestión de predios estatales; actos de administración | Ley 29151 y su reglamento (SBN) | Verificar: autorizaciones y procedimiento |
| Asociaciones Público Privadas (si la operación califica como APP) | D.Leg. 1362 y su reglamento | Verificar si aplica |
| Instrumentos de gestión del suelo; Operador Público del Suelo (Fondo MIVIVIENDA) | Ley 31313, modificada por D.Leg. 1674 | Verificar alcance |
| Vivienda de interés social | Ley 32379 y reglamento | Verificar |
| Bono de Arrendamiento para Vivienda | Ley 30952 y reglamento | Verificar monto y requisitos vigentes |
| Arrendamiento, desalojo notarial, RAV y FUA | D.Leg. 1177 | Verificar |
| IGV del alquiler de vivienda por empresas (paridad) | TUO Ley del IGV; PL 58-2026 (proyecto) | Condición de viabilidad; verificar estado |
| FIBRA como tenedor de largo plazo | Ley 30532 y reglamento de la SMV | Verificar si un derecho de superficie es activo elegible |
| Hipoteca sobre derecho de superficie; garantía mobiliaria | Código Civil; D.Leg. 1400 | Verificar |
| Arbitraje con entidades públicas | D.Leg. 1071 | Verificar |
| Plan de desarrollo urbano | PLANMET 2040 (Municipalidad Metropolitana de Lima) | Verificar ordenanza aprobatoria |

Antes de usar el modelo en una operación real, todas las normas deben revisarse contra su texto vigente.
