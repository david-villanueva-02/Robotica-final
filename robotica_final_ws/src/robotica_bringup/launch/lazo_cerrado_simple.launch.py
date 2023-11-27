from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    sensing = Node(
        package="control",
        executable="sensing",
        name="sensing_node",
    )

    input_controller = Node(
        package= "control",
        executable= "input_control",
        name="input_controller"
    )

    motor_1 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        parameters=[
            {"topic_info","/P1_info"},
            {"topic_command": "/P1"},
            {"referencia": 0.0},
            {"stepPin": 36},
            {"dirPin": 38},
            {"enPin": 40},
            {"limits": (0.0,30.0)},
            {"P_PID":0.0},
            {"I_PID": 10000.0},
            {"D_PID:": 0}
        ]
    )

    motor_2 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        parameters=[
            {"topic_info","/P2_info"},
            {"topic_command": "/P2"},
            {"referencia": 0.0},
            {"stepPin": 33},
            {"dirPin": 35},
            {"enPin": 37},
            {"limits": (0.0,100.0)},
            {"P_PID":0.0},
            {"I_PID": 10000.0},
            {"D_PID:": 0}
        ]
    )

    motor_3 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        parameters=[
            {"topic_info","/R1_info"},
            {"topic_command": "/R1"},
            {"referencia": 0.0},
            {"stepPin": 19},
            {"dirPin": 21},
            {"enPin": 23},
            {"limits": (0.0,180.0)},
            {"P_PID":0.0},
            {"I_PID": 10000.0},
            {"D_PID:": 0}
        ]
    )

    motor_4 = Node(
        package= "control",
        executable= "simple_lazo_cerrado",
        parameters=[
            {"topic_info","/R2_info"},
            {"topic_command": "/R2"},
            {"referencia": 0.0},
            {"stepPin": 3},
            {"dirPin": 5},
            {"enPin": 7},
            {"limits": (0.0,180.0)},
            {"P_PID":0.0},
            {"I_PID": 10000.0},
            {"D_PID:": 0}
        ]
    )


    ld.add_action(sensing)
    ld.add_action(input_controller)
    ld.add_action(motor_1)
    ld.add_action(motor_2)
    ld.add_action(motor_3)
    ld.add_action(motor_4)
    return ld