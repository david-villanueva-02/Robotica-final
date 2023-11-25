from setuptools import find_packages, setup

package_name = 'control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='david',
    maintainer_email='david.villanueva.guzman@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensing = control.sensing:main',
            'input_control = control.input_control:main',
            'motor_1 = control.motor_1:main',
            'motor_2 = control.motor_2:main',
            'motor_3 = control.motor_3:main',
            'motor_4 = control.motor_4:main'
        ],
    },
)
