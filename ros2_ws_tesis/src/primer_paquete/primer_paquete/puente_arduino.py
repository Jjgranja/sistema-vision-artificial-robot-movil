"""Puente ROS 2 -> Arduino para los estados del sistema de visión.

Mapeo documentado en el trabajo de grado:
SEGURO=O, ALERTA=L, DETENER=X, GIRO DERECHA=D, GIRO IZQUIERDA=A.
"""

import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PuenteArduino(Node):
    def __init__(self):
        super().__init__('puente_arduino')

        self.declare_parameter('puerto', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)

        puerto = self.get_parameter('puerto').value
        baudrate = int(self.get_parameter('baudrate').value)

        self.mapa = {
            'SEGURO': 'O',
            'ALERTA': 'L',
            'DETENER': 'X',
            'GIRO DERECHA': 'D',
            'GIRO IZQUIERDA': 'A',
        }

        self.serial = None
        try:
            self.serial = serial.Serial(puerto, baudrate, timeout=1)
            self.get_logger().info(f'Conectado a Arduino en {puerto} @ {baudrate}.')
        except serial.SerialException as exc:
            self.get_logger().error(f'No fue posible abrir el puerto serial: {exc}')

        self.create_subscription(String, '/estado_vision', self.estado_callback, 10)

    def estado_callback(self, msg: String):
        estado = msg.data.strip().upper()
        comando = self.mapa.get(estado)
        if comando is None:
            self.get_logger().warning(f'Estado no reconocido: {msg.data}')
            return

        if self.serial is None or not self.serial.is_open:
            self.get_logger().warning(
                f'Comando {comando} no enviado: puerto serial no disponible.'
            )
            return

        self.serial.write(comando.encode('ascii'))

    def destroy_node(self):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()
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
