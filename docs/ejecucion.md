# Ejecución del sistema

## Requisitos principales

- Ubuntu 22.04
- ROS 2 Humble
- Intel RealSense D415
- NVIDIA Jetson Orin Nano 8 GB
- Python 3
- Ultralytics YOLOv8
- OpenCV
- NumPy
- PySerial

## Preparación del entorno

Instale los paquetes ROS 2 necesarios:

```bash
sudo apt update
sudo apt install ros-humble-cv-bridge ros-humble-realsense2-camera
```

Instale las dependencias Python:

```bash
python3 -m pip install -r requirements.txt
```

Compile el workspace:

```bash
cd ros2_ws_tesis
colcon build --symlink-install
source install/setup.bash
```

## Pesos de los modelos

Coloque los archivos:

```text
/home/jetson/tesis_julian/modelos/yolov8n.pt
/home/jetson/tesis_julian/modelos/best_personalizado.pt
```

Las rutas pueden modificarse mediante parámetros del nodo si el proyecto se ejecuta desde otra ubicación.

## Ejecución de la cámara

```bash
ros2 launch realsense2_camera rs_launch.py \
  rgb_camera.color_profile:=640x480x30 \
  depth_module.depth_profile:=640x480x30
```

## Ejecución de la visión

En otra terminal:

```bash
source ros2_ws_tesis/install/setup.bash
ros2 run primer_paquete fusion_realsense_nav
```

## Enlace con Arduino

En una tercera terminal:

```bash
source ros2_ws_tesis/install/setup.bash
ros2 run primer_paquete puente_arduino
```

El puerto serial y la velocidad deben configurarse de acuerdo con la conexión real del Arduino.

## Verificación

Para comprobar la publicación del estado de visión:

```bash
ros2 topic echo /estado_vision
```

Para observar la frecuencia:

```bash
ros2 topic hz /estado_vision
```

Durante las pruebas del trabajo de grado se registró una frecuencia aproximada de 18 Hz para este tópico.
