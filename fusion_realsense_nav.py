#!/usr/bin/env python3

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from ultralytics import YOLO

MODELO_BASE = '/home/jetson/tesis_julian/modelos/yolov8n.pt'
MODELO_PERSONALIZADO = '/home/jetson/tesis_julian/modelos/best_personalizado.pt'
CONFIANZA = 0.35


class LectorCamaraFusion(Node):
    def __init__(self):
        super().__init__('fusion_realsense_nav')

        self.bridge = CvBridge()
        self.depth_frame = None
        self.modelo_base = YOLO(MODELO_BASE)
        self.modelo_personalizado = YOLO(MODELO_PERSONALIZADO)

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

        self.get_logger().info('Sistema de visión iniciado')

    def depth_callback(self, msg):
        self.depth_frame = self.bridge.imgmsg_to_cv2(
            msg, desired_encoding='passthrough'
        )

    @staticmethod
    def obtener_profundidad(depth, cx, cy):
        h, w = depth.shape[:2]
        x0, x1 = max(0, cx - 2), min(w, cx + 3)
        y0, y1 = max(0, cy - 2), min(h, cy + 3)

        region = depth[y0:y1, x0:x1]
        valores = region[region > 0]

        if valores.size == 0:
            return None

        return float(np.median(valores))

    @staticmethod
    def obtener_zona(cx, ancho):
        if cx < ancho / 3:
            return 'IZQUIERDA'
        if cx > (2 * ancho) / 3:
            return 'DERECHA'
        return 'CENTRO'

    @staticmethod
    def decidir(distancia, zona):
        if distancia < 400:
            return 'DETENER'

        if distancia < 700:
            if zona == 'IZQUIERDA':
                return 'GIRO DERECHA'
            if zona == 'DERECHA':
                return 'GIRO IZQUIERDA'
            return 'DETENER'

        if distancia < 1000:
            return 'ALERTA'

        return 'SEGURO'

    def detectar(self, frame):
        detecciones = []

        for modelo in (self.modelo_base, self.modelo_personalizado):
            resultados = modelo.predict(
                frame,
                conf=CONFIANZA,
                verbose=False,
            )

            for resultado in resultados:
                if resultado.boxes is None:
                    continue

                for box in resultado.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    cls_id = int(box.cls[0].item())
                    nombre = resultado.names.get(cls_id, str(cls_id))
                    confianza = float(box.conf[0].item())

                    detecciones.append({
                        'bbox': (x1, y1, x2, y2),
                        'clase': nombre,
                        'confianza': confianza,
                    })

        return detecciones

    def rgb_callback(self, msg):
        if self.depth_frame is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        alto, ancho = frame.shape[:2]
        candidatos = []

        for det in self.detectar(frame):
            x1, y1, x2, y2 = det['bbox']
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            if not (0 <= cx < self.depth_frame.shape[1] and
                    0 <= cy < self.depth_frame.shape[0]):
                continue

            distancia = self.obtener_profundidad(self.depth_frame, cx, cy)
            if distancia is None:
                continue

            zona = self.obtener_zona(cx, ancho)
            candidatos.append((distancia, zona, det['clase']))

        if candidatos:
            distancia, zona, clase = min(candidatos, key=lambda item: item[0])
            estado = self.decidir(distancia, zona)
            self.get_logger().info(
                f'{clase} | {distancia:.0f} mm | {zona} | {estado}'
            )
        else:
            estado = 'SEGURO'

        mensaje = String()
        mensaje.data = estado
        self.pub_estado.publish(mensaje)


def main(args=None):
    rclpy.init(args=args)
    nodo = LectorCamaraFusion()

    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
