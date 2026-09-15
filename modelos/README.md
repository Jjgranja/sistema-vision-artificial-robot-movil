# Modelos de detección

El sistema emplea dos modelos YOLOv8 durante la inferencia:

- `yolov8n.pt`: modelo base para clases generales.
- `best_personalizado.pt`: modelo entrenado para las clases `door`, `wall` y `window`.

## Modelo personalizado

Configuración de entrenamiento documentada en el trabajo de grado:

| Parámetro | Valor |
|---|---|
| Modelo inicial | `yolov8s.pt` |
| Épocas | 50 |
| Tamaño de entrada | 640 px |
| Batch | 16 |
| Dispositivo de entrenamiento | CPU |
| Modelo final | `best_personalizado.pt` |

Métricas finales registradas:

- Precisión: `0.601`
- Recall: `0.492`
- mAP50: `0.495`
- mAP50-95: `0.389`

## Ubicación esperada

En la Jetson Orin Nano los pesos se organizaron en:

```text
/home/jetson/tesis_julian/modelos/
├── yolov8n.pt
└── best_personalizado.pt
```

Los archivos `.pt` no se incluyen automáticamente en este repositorio hasta disponer de los binarios originales del proyecto.
