from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    '''
    sensing = Node(
        package="control",
        executable="sensing",
    )
    '''
    input_controller = Node(
        package= "control",
        executable= "input_control",
    )

    motor_1 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        name="motor_1",
        parameters=[
            {"topic_info": "/P1_info"},
            {"topic_command": "/P1"},
            {"referencia": 16.0},
            {"stepPin": 36},
            {"dirPin": 38},
            {"enPin": 40},
            {"limits": (3.0,27.0)},
            {"tolerancia": 0.5},
            {"step":0.5},
            {"freq": 1000}
        ]
    )

    motor_2 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        name="motor_2",
        parameters=[
            {"topic_info": "/P2_info"},
            {"topic_command": "/P2"},
            {"referencia": 15.0},
            {"stepPin": 33},
            {"dirPin": 35},
            {"enPin": 37},
            {"limits": (3.5,18.0)},
            {"tolerancia": 0.5},
            {"step":0.5},
            {"invertir": True},
            {"freq": 1000}
        ]
    )

    motor_3 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        name="motor_3",
        parameters=[
            {"topic_info": "/R1_info"},
            {"topic_command": "/R1"},
            {"referencia": 0.0},
            {"stepPin": 19},
            {"dirPin": 21},
            {"enPin": 23},
            {"limits": (0.0,180.0)},
            {"tolerancia": 2.0},
            {"freq": 100}
        ]
    )

    motor_4 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        name="motor_4",
        parameters=[
            {"topic_info": "/R2_info"},
            {"topic_command": "/R2"},
            {"referencia": 0.0},
            {"stepPin": 3},
            {"dirPin": 5},
            {"enPin": 7},
            {"limits": (0.0,180.0)},
            {"tolerancia": 2.0},
            {"freq": 100}
        ]
    )

    actuador = Node(
        package="control",
        executable="actuador"
    )

    #ld.add_action(sensing)
    ld.add_action(input_controller)
    ld.add_action(motor_1)
    ld.add_action(motor_2)
    ld.add_action(motor_3)
    ld.add_action(motor_4)
    ld.add_action(actuador)
    return ld