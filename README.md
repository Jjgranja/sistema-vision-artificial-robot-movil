# Sistema de visión artificial – Robot móvil

Repositorio del trabajo de grado **“Sistema de Visión Artificial con Aprendizaje Profundo Embebido en Plataforma Acelerada para Aplicaciones Inteligentes”**.

El sistema reemplaza la visión Kinect utilizada en la arquitectura previa por una **Intel RealSense D415** y ejecuta la percepción en una **Jetson Orin Nano 8 GB** con **ROS 2 Humble** y **YOLOv8**. El control normal del robot mediante APK/Bluetooth se conserva; la visión actúa como una capa de asistencia para detener o corregir el movimiento ante obstáculos.

## Archivos

- `fusion_realsense_nav.py`: nodo de visión. Ejecuta `yolov8n.pt` y `best_personalizado.pt`, combina sus detecciones con la profundidad de la RealSense y publica `/estado_vision`.
- `puente_arduino.py`: recibe `/estado_vision` y envía al Arduino los comandos `O`, `L`, `X`, `D` y `A`.
- `codigo_arduino_vision.ino`: integración del control base del robot con los comandos provenientes de la capa visual, conservando el control Bluetooth.
- `data.yaml`: clases del modelo personalizado (`door`, `wall`, `window`).
- `requirements.txt`: dependencias Python adicionales.

Los pesos utilizados en la Jetson se ubicaron en:

```text
/home/jetson/tesis_julian/modelos/yolov8n.pt
/home/jetson/tesis_julian/modelos/best_personalizado.pt
```

## Lógica de decisión

| Distancia | Posición | Acción |
|---|---|---|
| `< 400 mm` | cualquiera | DETENER |
| `400–700 mm` | izquierda | GIRO DERECHA |
| `400–700 mm` | centro | DETENER |
| `400–700 mm` | derecha | GIRO IZQUIERDA |
| `700–1000 mm` | cualquiera | ALERTA |
| `>= 1000 mm` | cualquiera | SEGURO |

La profundidad asociada a cada detección se calcula mediante la mediana de una región **5×5** alrededor del centro de la caja delimitadora, descartando valores de profundidad iguales a cero.

## Ejecución

1. Iniciar la RealSense:

```bash
ros2 launch realsense2_camera rs_launch.py \
  depth_module.depth_profile:=640x480x30 \
  rgb_camera.color_profile:=640x480x30
```

2. En otra terminal, con ROS 2 cargado:

```bash
python3 fusion_realsense_nav.py
```

3. En una tercera terminal:

```bash
python3 puente_arduino.py
```

El puente usa por defecto `/dev/ttyACM0` a `9600` baudios. Si el Arduino aparece en otro puerto, cambie la constante `PUERTO` al inicio del archivo.

## Comandos enviados al Arduino

```text
SEGURO         -> O
ALERTA         -> L
DETENER        -> X
GIRO DERECHA   -> D
GIRO IZQUIERDA -> A
```

`O` y `L` permiten continuar con el mando manual previamente recibido; `X`, `D` y `A` realizan la intervención visual correspondiente.

## Modelo personalizado

Dataset final: **301 imágenes**.

```text
Entrenamiento: 241
Validación:     40
Prueba:         20
Clases:         door, wall, window
```

El entrenamiento final se realizó durante 50 épocas, con imágenes de 640 px y `batch=16`. Los resultados de validación reportados fueron `P=0.601`, `R=0.492`, `mAP50=0.495` y `mAP50-95=0.389`.

## Observación

Durante las pruebas se identificó menor estabilidad de la profundidad aproximadamente entre **300 y 400 mm**. Por esta razón, ese intervalo se conserva como una limitación experimental del sistema y no se presenta como una zona de operación confiable.

**Autor:** José Julián Granja Trávez – Ingeniería Mecatrónica, Universidad Técnica del Norte.
