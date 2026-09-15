# Anexo – Repositorio del sistema

El código fuente, la estructura del workspace ROS 2, la documentación de los modelos y las instrucciones de ejecución correspondientes al sistema de visión artificial desarrollado se encuentran disponibles en el siguiente repositorio:

**Repositorio:** https://github.com/Jjgranja/sistema-vision-artificial-robot-movil

El repositorio reúne la estructura utilizada para la integración de la Intel RealSense D415, la ejecución de los modelos YOLOv8 en la Jetson Orin Nano, la publicación del tópico `/estado_vision` y la comunicación con Arduino para la intervención física sobre el robot móvil de alto torque.

Los archivos binarios de los modelos entrenados pueden mantenerse fuera del repositorio cuando su tamaño o licencia así lo requieran; en ese caso, su ubicación y forma de incorporación quedan documentadas dentro de la carpeta `modelos/`.
