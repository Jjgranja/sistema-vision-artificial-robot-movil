"""Nodo ROS 2 de visión y navegación asistida.

Implementación de referencia reconstruida a partir de la arquitectura y lógica
funcional documentadas en el trabajo de grado. Ajuste rutas y parámetros a la
instalación real de la Jetson antes de ejecutar.
"""

from pathlib import Path

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from ultralytics import YOLO


class FusionRealSenseNav(Node):
    def __init__(self):
        super().__init__('fusion_realsense_nav')

        self.declare_parameter(
            'modelo_base',
            '/home/jetson/tesis_julian/modelos/yolov8n.pt',
        )
        self.declare_parameter(
            'modelo_personalizado',
            '/home/jetson/tesis_julian/modelos/best_personalizado.pt',
        )
        self.declare_parameter('confianza', 0.35)

        base_path = self.get_parameter('modelo_base').value
        custom_path = self.get_parameter('modelo_personalizado').value
        self.conf = float(self.get_parameter('confianza').value)

        if not Path(base_path).exists():
            self.get_logger().warning(f'No se encontró modelo base: {base_path}')
        if not Path(custom_path).exists():
            self.get_logger().warning(
                f'No se encontró modelo personalizado: {custom_path}'
            )

        self.modelo_base = YOLO(base_path)
        self.modelo_personalizado = YOLO(custom_path)

        self.bridge = CvBridge()
        self.depth_frame = None

        self.pub_estado = self.create_publisher(String, '/estado_vision', 10)

        self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.rgb_callback,
            10,
        )
        self.create_subscription(
            Image,
            '/camera/camera/depth/image_rect_raw',
            self.depth_callback,
            10,
        )

        self.get_logger().info('Nodo fusion_realsense_nav iniciado.')

    def depth_callback(self, msg: Image):
        self.depth_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    @staticmethod
    def profundidad_mediana(depth: np.ndarray, cx: int, cy: int):
        """Obtiene la mediana de valores válidos en una vecindad 5x5."""
        h, w = depth.shape[:2]
        x0, x1 = max(0, cx - 2), min(w, cx + 3)
        y0, y1 = max(0, cy - 2), min(h, cy + 3)
        region = depth[y0:y1, x0:x1]
        valores = region[region > 0]
        if valores.size == 0:
            return None
        return float(np.median(valores))

    @staticmethod
    def zona_horizontal(cx: int, ancho: int):
        if cx < ancho / 3:
            return 'IZQUIERDA'
        if cx > 2 * ancho / 3:
            return 'DERECHA'
        return 'CENTRO'

    @staticmethod
    def decidir_estado(distancia_mm: float, zona: str):
        if distancia_mm < 400:
            return 'DETENER'
        if distancia_mm < 700:
            if zona == 'IZQUIERDA':
                return 'GIRO DERECHA'
            if zona == 'DERECHA':
                return 'GIRO IZQUIERDA'
            return 'DETENER'
        if distancia_mm < 1000:
            return 'ALERTA'
        return 'SEGURO'

    def extraer_detecciones(self, frame):
        detecciones = []
        for modelo in (self.modelo_base, self.modelo_personalizado):
            resultados = modelo.predict(frame, conf=self.conf, verbose=False)
            for resultado in resultados:
                if resultado.boxes is None:
                    continue
                nombres = resultado.names
                for box in resultado.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    cls_id = int(box.cls[0].item())
                    confianza = float(box.conf[0].item())
                    detecciones.append(
                        {
                            'bbox': (x1, y1, x2, y2),
                            'clase': nombres.get(cls_id, str(cls_id)),
                            'confianza': confianza,
                        }
                    )
        return detecciones

    def rgb_callback(self, msg: Image):
        if self.depth_frame is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        h, w = frame.shape[:2]
        profundidad = self.depth_frame

        candidatos = []
        for det in self.extraer_detecciones(frame):
            x1, y1, x2, y2 = det['bbox']
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            if not (0 <= cx < profundidad.shape[1] and 0 <= cy < profundidad.shape[0]):
                continue

            distancia = self.profundidad_mediana(profundidad, cx, cy)
            if distancia is None:
                continue

            zona = self.zona_horizontal(cx, w)
            candidatos.append((distancia, zona, det))

        if not candidatos:
            estado = 'SEGURO'
        else:
            distancia, zona, _ = min(candidatos, key=lambda item: item[0])
            estado = self.decidir_estado(distancia, zona)

        mensaje = String()
        mensaje.data = estado
        self.pub_estado.publish(mensaje)


def main(args=None):
    rclpy.init(args=args)
    nodo = FusionRealSenseNav()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
