#!/usr/bin/env python3

import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

PUERTO = '/dev/ttyACM0'
BAUDRATE = 9600


class PuenteArduino(Node):
    def __init__(self):
        super().__init__('puente_arduino')

        self.mapa = {
            'SEGURO': 'O',
            'ALERTA': 'L',
            'DETENER': 'X',
            'GIRO DERECHA': 'D',
            'GIRO IZQUIERDA': 'A',
        }

        self.arduino = serial.Serial(PUERTO, BAUDRATE, timeout=1)
        self.create_subscription(
            String,
            '/estado_vision',
            self.estado_callback,
            10,
        )

        self.get_logger().info(
            f'Puente Arduino conectado en {PUERTO} a {BAUDRATE} baudios'
        )

    def estado_callback(self, msg):
        estado = msg.data.strip().upper()
        comando = self.mapa.get(estado)

        if comando is None:
            return

        self.arduino.write(comando.encode('ascii'))
        self.get_logger().info(f'{estado} -> {comando}')

    def destroy_node(self):
        if self.arduino.is_open:
            self.arduino.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    nodo = PuenteArduino()

    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
