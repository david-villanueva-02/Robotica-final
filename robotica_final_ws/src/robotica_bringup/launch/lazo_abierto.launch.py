from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # Add controller Node
    input_controller = Node(
        package= "control",
        executable= "input_control",
        name="input_controller"
    )

    motor_1 = Node(
        package="control",
        executable="simple_motor",
        name="motor_1",
        parameters=[
            {"stepPin": 36},
            {"dirPin": 38},
            {"enPin": 40},
            {"motorTopic": "/P1"},
            {"freq": 1000}
        ]
    )

    motor_2 = Node(
        package="control",
        executable="simple_motor",
        name="motor_2",
        parameters=[
            {"stepPin": 33},
            {"dirPin": 35},
            {"enPin": 37},
            {"motorTopic": "/P2"},
            {"freq": 1000},
            {"invertir": True}
        ]
    )

    motor_3 = Node(
        package="control",
        executable="simple_motor",
        name="motor_3",
        parameters=[
            {"stepPin": 19},
            {"dirPin": 21},
            {"enPin": 23},
            {"motorTopic": "/R1"},
            {"freq": 10}
        ]
    )

    motor_4 = Node(
        package="control",
        executable="simple_motor",
        name="motor_4",
        parameters=[
            {"stepPin": 3},
            {"dirPin": 5},
            {"enPin": 7},
            {"motorTopic": "/R2"},
            {"freq": 10}
        ]
    )

    ld.add_action(input_controller)
    ld.add_action(motor_1)
    ld.add_action(motor_2)
    ld.add_action(motor_3)
    ld.add_action(motor_4)

    return ld