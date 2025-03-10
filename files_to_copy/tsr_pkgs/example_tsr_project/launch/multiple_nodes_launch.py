import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # nazw pakietu
    package_name = 'example_tsr_project'

    # Pobranie ścieżki do katalogu pakietu
    package_dir = get_package_share_directory(package_name)

    # Ścieżka do pliku launch, który uruchamia talkera i subskrybenta
    topic_launch_file = os.path.join(package_dir, 'launch', 'topic_example_launch.py')

    # Ścieżka do pliku konfiguracyjnego YAML dla węzła parameters_node
    config_file = os.path.join(package_dir, 'config', 'robot_controller_config.yaml')
    # Ścieżka do pliku konfiguracyjnego YAML (konfiguracja tła) dla węzła turtlesim
    bg_color_config_file = os.path.join(package_dir, 'config', 'turtlesim_bg.yaml')

    return LaunchDescription([
        # Uruchomienie istniejącego launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(topic_launch_file)
        ),

        # Uruchomienie węzła parameters_node z załadowaną konfiguracją YAML
        Node(
            package=package_name,
            executable='parameters_node',
            name='robot_controller',
            output='screen',
            parameters=[config_file]
        ),
        
        # Wczytanie parametrów koloru tła dla turtlesim - wykonanie polecenia w terminalu ros2 param load /turtlesim path/turtlesim_bg.yaml
        ExecuteProcess(
            cmd=['ros2', 'param', 'load', '/turtlesim', bg_color_config_file],
            output='screen'
        )
    ])

