# Sistema de Visión Artificial para Robot Móvil de Alto Torque

Repositorio asociado al trabajo de grado **“Sistema de Visión Artificial con Aprendizaje Profundo Embebido en Plataforma Acelerada para Aplicaciones Inteligentes”**, desarrollado en la Carrera de Ingeniería en Mecatrónica de la Universidad Técnica del Norte.

**Autor:** José Julián Granja Trávez  
**Plataforma:** NVIDIA Jetson Orin Nano 8 GB  
**Sensor RGB-D:** Intel RealSense D415  
**Middleware:** ROS 2 Humble  
**Detección:** YOLOv8 / Ultralytics

## Descripción

El proyecto implementa una capa de percepción e intervención asistida sobre un robot móvil diferencial de alto torque. La Intel RealSense D415 proporciona imagen RGB y profundidad; la Jetson Orin Nano ejecuta los modelos de detección, consulta la profundidad del obstáculo y aplica una lógica de decisión. El resultado se publica en `/estado_vision` y se comunica a un Arduino encargado de ejecutar la intervención física.

El control manual existente mediante APK/Bluetooth se conserva; el sistema de visión funciona como una capa adicional de seguridad frente a obstáculos.

## Arquitectura funcional

```text
Intel RealSense D415
        │
        ├── RGB ───────────────┐
        └── Profundidad ───────┤
                               ▼
                    Jetson Orin Nano
                   ROS 2 + YOLOv8
                               │
                     /estado_vision
                               │
                               ▼
                       puente_arduino
                               │
                               ▼
                         Arduino Mega
                               │
                               ▼
                    Movimiento del robot
```

## Modelos utilizados

- `yolov8n.pt`: detector general preentrenado.
- `best_personalizado.pt`: detector personalizado para `door`, `wall` y `window`.

El modelo personalizado fue desarrollado a partir de un dataset final de **301 imágenes**, dividido en 241 imágenes de entrenamiento, 40 de validación y 20 de prueba.

## Lógica de decisión

| Distancia | Zona | Estado | Comando |
|---|---|---|---|
| `d < 400 mm` | Cualquiera | DETENER | `X` |
| `400 ≤ d < 700 mm` | Izquierda | GIRO DERECHA | `D` |
| `400 ≤ d < 700 mm` | Centro | DETENER | `X` |
| `400 ≤ d < 700 mm` | Derecha | GIRO IZQUIERDA | `A` |
| `700 ≤ d < 1000 mm` | Cualquiera | ALERTA | `L` |
| `d ≥ 1000 mm` | Cualquiera | SEGURO | `O` |

La posición horizontal se obtiene a partir del centro de la caja delimitadora y la profundidad se estima mediante la mediana de valores válidos dentro de una vecindad de 5×5 píxeles alrededor de dicho punto.

## Resultados principales

El modelo personalizado obtuvo `P=0.601`, `R=0.492`, `mAP50=0.495` y `mAP50-95=0.389`. Durante la ejecución embebida, `/estado_vision` se publicó alrededor de 18 Hz, mientras la cámara RGB se mantuvo próxima a 30 Hz. Las pruebas físicas verificaron detención y giros según la posición y distancia de los obstáculos.

Se observó una menor confiabilidad operativa de la percepción de profundidad aproximadamente entre **300 y 400 mm**, aspecto documentado como limitación del sistema.

## Estructura del repositorio

```text
.
├── README.md
├── CITATION.cff
├── requirements.txt
├── dataset/
│   └── README.md
├── modelos/
│   └── README.md
├── docs/
│   ├── arquitectura.md
│   ├── ejecucion.md
│   ├── pruebas.md
│   └── anexo_tesis.md
└── ros2_ws_tesis/
    ├── README.md
    └── src/
        └── primer_paquete/
            ├── package.xml
            ├── setup.py
            ├── setup.cfg
            ├── resource/primer_paquete
            ├── primer_paquete/
            │   ├── __init__.py
            │   ├── fusion_realsense_nav.py
            │   └── puente_arduino.py
            └── launch/
                └── vision_robot.launch.py
```

## Instalación rápida

```bash
sudo apt update
sudo apt install ros-humble-cv-bridge ros-humble-realsense2-camera
python3 -m pip install -r requirements.txt
```

Clone el repositorio y compile el workspace:

```bash
git clone https://github.com/Jjgranja/sistema-vision-artificial-robot-movil.git
cd sistema-vision-artificial-robot-movil/ros2_ws_tesis
colcon build --symlink-install
source install/setup.bash
```

Consulte [`docs/ejecucion.md`](docs/ejecucion.md) para el procedimiento de ejecución y parámetros configurables.

## Nota sobre modelos y dataset

Los pesos entrenados y las imágenes originales del dataset pueden superar el tamaño conveniente para un repositorio académico. La carpeta `modelos/` documenta dónde colocar `best_personalizado.pt`, mientras `dataset/README.md` conserva la estructura, clases y particiones empleadas en el trabajo.

## Documentación académica

El texto sugerido para citar este repositorio dentro de los anexos del trabajo de grado se encuentra en [`docs/anexo_tesis.md`](docs/anexo_tesis.md).
