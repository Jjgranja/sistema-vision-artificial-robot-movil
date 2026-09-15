# Pruebas y validación

## Distancias y estados

La validación incluyó pruebas de profundidad y cambio de estado alrededor de los umbrales definidos para la lógica de decisión.

Se verificaron transiciones próximas a:

- 1000 mm: `SEGURO → ALERTA`
- 700 mm: `ALERTA → DETENER`
- Alejamiento: `DETENER → ALERTA → SEGURO`

Las tres repeticiones realizadas mostraron correspondencia satisfactoria entre los umbrales programados y los cambios de estado observados.

## Pruebas por zonas

A una distancia cercana a 600 mm se evaluaron obstáculos en izquierda, centro y derecha:

- Izquierda: giro hacia la derecha.
- Centro: detención.
- Derecha: giro hacia la izquierda.

La condición central presentó alternancia temporal entre zonas durante la aproximación, pero el robot terminó ejecutando la detención al confirmarse la detección frontal.

## Profundidad

Entre 600 y 1200 mm las mediciones de la RealSense D415 se mantuvieron próximas a las distancias de referencia. Entre 300 y 400 mm se observaron variaciones operativas entre los estados `DETENER` y `SEGURO`, por lo que este intervalo fue identificado como zona de menor confiabilidad para la lógica de navegación.

## Frecuencias

- RGB: 29.31–29.74 Hz
- Profundidad: 25.57–29.44 Hz
- `/estado_vision`: aproximadamente 18 Hz

## Recursos de la Jetson Orin Nano

Durante las pruebas se registró aproximadamente 39.2 % de uso de RAM, sin uso de swap. La GPU mostró actividad variable durante la inferencia y las temperaturas de CPU y GPU se mantuvieron alrededor de 73–74 °C en las condiciones evaluadas.

Estas mediciones corresponden a la ejecución documentada en el trabajo de grado y no representan una caracterización universal de la plataforma.
