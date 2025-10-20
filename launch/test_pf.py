from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Launch arguments
    map_file = DeclareLaunchArgument('map_yaml')
    use_sim_time = DeclareLaunchArgument('use_sim_time', default_value="true")

    # Lifecycle manager setup
    lifecycle_nodes = ['map_server']
    autostart = True

    start_lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'autostart': autostart},
            {'node_names': lifecycle_nodes}
        ]
    )

    return LaunchDescription([
        map_file,
        use_sim_time,

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[{"yaml_filename": LaunchConfiguration('map_yaml')}],
            output='screen'
        ),

        Node(
            package='robot_localization',
            executable='pf.py',
            name='my_pf',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
            emulate_tty=True,
            output='screen'
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_odom_broadcaster',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
        ),

        # Lifecycle manager
        start_lifecycle_manager
    ])
