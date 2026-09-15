# Workspace ROS 2

Este directorio contiene la estructura del paquete ROS 2 utilizado para la integración del sistema de visión con el robot.

## Paquete

`primer_paquete`

Ejecutables principales:

- `fusion_realsense_nav`: detección, profundidad y lógica de decisión.
- `puente_arduino`: recepción de `/estado_vision` y envío del comando correspondiente hacia Arduino.

## Compilación

```bash
colcon build --symlink-install
source install/setup.bash
```

## Ejecución

```bash
ros2 run primer_paquete fusion_realsense_nav
ros2 run primer_paquete puente_arduino
```
