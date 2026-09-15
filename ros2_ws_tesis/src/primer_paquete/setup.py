from setuptools import find_packages, setup

package_name = 'primer_paquete'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/vision_robot.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='José Julián Granja Trávez',
    maintainer_email='noreply@example.com',
    description='Sistema de visión artificial y puente de comunicación con Arduino.',
    license='All rights reserved',
    entry_points={
        'console_scripts': [
            'fusion_realsense_nav = primer_paquete.fusion_realsense_nav:main',
            'puente_arduino = primer_paquete.puente_arduino:main',
        ],
    },
)
