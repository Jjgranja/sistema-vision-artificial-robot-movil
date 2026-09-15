# Arquitectura del sistema

La aplicación final se implementó como una capa de percepción e intervención asistida sobre un robot móvil diferencial de alto torque.

## Flujo principal

```text
Intel RealSense D415
   │
   ├── Imagen RGB
   └── Profundidad
          │
          ▼
Jetson Orin Nano
ROS 2 Humble + OpenCV + Ultralytics
          │
          ├── YOLOv8n: clases generales
          ├── Modelo personalizado: door / wall / window
          ├── Consulta de profundidad
          └── Lógica de decisión
          │
          ▼
/estado_vision
          │
          ▼
puente_arduino
          │
          ▼
Arduino Mega
          │
          ▼
Intervención física sobre el robot
```

## Estados y comandos

- `SEGURO` → `O`
- `ALERTA` → `L`
- `DETENER` → `X`
- `GIRO DERECHA` → `D`
- `GIRO IZQUIERDA` → `A`

El control manual mediante APK/Bluetooth permanece disponible. La visión actúa como una capa adicional de asistencia frente a obstáculos.

## Cámara

La RealSense D415 se utilizó con perfiles RGB y profundidad de 640×480 a 30 Hz. Los tópicos principales documentados fueron:

```text
/camera/camera/color/image_raw
/camera/camera/depth/image_rect_raw
```

## Profundidad

Para cada detección se toma el centro de la caja delimitadora. Alrededor de este punto se consulta una vecindad de hasta 5×5 píxeles, se descartan profundidades iguales a cero y se utiliza la mediana de los valores positivos como distancia representativa.

## Zonas horizontales

La imagen se divide en tres regiones según la coordenada horizontal del centro de la detección:

```text
Izquierda | Centro | Derecha
```

La zona, junto con la distancia estimada, determina el estado publicado por el sistema.
