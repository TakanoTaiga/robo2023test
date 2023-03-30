from launch import LaunchDescription , actions
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os.path


def generate_launch_description():
    MACRO_MDC_ASYNC = False
    MACRO_MDC_SYNC = True
    
    return LaunchDescription([
        # Physical Controller
        Node(
            package='smart_controller_gateway',
            executable='smart_controller_gateway_node',
            parameters=[{'is_publish_twist' : True}],
            remappings=[
                ('/smart_controller_gateway/output/twist' , '/robo2022/cmd_vel/rover'),
                ('/smart_controller_gateway/output/smartui' , '/sc_client/SmartUI'),
                ('/smart_controller_gateway/output/gamepad' , '/sc_client/gamepad'),
            ],
        ),
        # Joysic to vector
        Node(
            package='team_support',
            executable='joy2vel4a',
            remappings=[
                ('/joy' , '/sc_client/gamepad'),
                ('/SmartUI' , '/sc_client/SmartUI')
            ],
            on_exit=actions.Shutdown(),
        ),
        
        # Smoothers
        Node(
            package='robo2022',
            executable='motion_smoother',
            remappings=[
                ('/cmd_vel/in' ,  '/robo2022/cmd_vel/rover'),
                ('/cmd_vel/out' , '/smoothed_cmd_vel/main/rover')
            ],
            parameters=[{'gain' : 0.05}],
            name='main'
        ),

        # Main block
        Node(
            package='robo2022',
            executable='robo2022',
            remappings=[
                ('/robo2022/cmd_vel/updown' , '/smoothed_cmd_vel/main/updown'),
                ('/robo2022/cmd_vel/rover' , '/smoothed_cmd_vel/main/rover')
            ]
            
        ),
        Node(
            package='team_support',
            executable='a_team',
            remappings=[
                ('/joy' , '/sc_client/joy'),
                ('/SmartUI' , '/sc_client/SmartUI'),
            ],
        ),
        
        # Hardware connector
        Node(
            package='robo2022',
            executable='mdc2022Connect',
            on_exit=actions.Shutdown(),
            parameters=[{'device_file' : '/dev/ttyACM0'},{'async' : MACRO_MDC_ASYNC}],
            remappings=[
                ('robo2022util/team/cmd_pwr' , 'robo2022util/a_team/cmd_pwr'),
            ],
        ),
    ])
