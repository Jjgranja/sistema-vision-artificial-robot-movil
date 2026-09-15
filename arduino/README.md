# Interfaz con Arduino Mega

El sistema de visión se comunica con el Arduino mediante un conjunto reducido de comandos de un carácter. El Arduino conserva la responsabilidad de ejecutar la intervención física sobre los motores del robot.

| Estado recibido desde ROS 2 | Comando serial | Acción esperada |
|---|---|---|
| `SEGURO` | `O` | Mantener operación normal |
| `ALERTA` | `L` | Estado preventivo |
| `DETENER` | `X` | Detener el robot |
| `GIRO DERECHA` | `D` | Ejecutar giro a la derecha |
| `GIRO IZQUIERDA` | `A` | Ejecutar giro a la izquierda |

El firmware original del sistema de control del robot no se reproduce aquí porque no fue proporcionado como archivo fuente dentro del material disponible para construir este repositorio. El nodo `puente_arduino.py` implementa el contrato de comunicación empleado por la capa de visión.
