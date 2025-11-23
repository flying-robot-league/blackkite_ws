import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import RegisterEventHandler, ExecuteProcess
from launch.substitutions import FindExecutable


from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution

def generate_launch_description():

    # Launch RSP
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('drone'), 'launch', 'rsp.launch.py')]),
        launch_arguments={'use_sim_time': ['true']}.items(),
    )
    
    
    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': [str(os.path.join(get_package_share_directory('drone'), 'worlds', 'empty_simulation_world.sdf'))], 
        'on_exit_shutdown': 'true'}.items(),
    )
    
    # Spawn robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                  '-name', 'blackkite',
                  '-z', '3.07'],
        output='screen'
    )
    
    # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen'
    )
    
    return LaunchDescription([
        rsp,
        gazebo,
        bridge,
        spawn_entity,
    ])