from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='primer_paquete',
            executable='fusion_realsense_nav',
            name='fusion_realsense_nav',
            output='screen',
        ),
        Node(
            package='primer_paquete',
            executable='puente_arduino',
            name='puente_arduino',
            output='screen',
        ),
    ])
