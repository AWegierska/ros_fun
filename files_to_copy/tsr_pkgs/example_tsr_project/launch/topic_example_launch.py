from launch import LaunchDescription
from launch_ros.actions import Node

# Funkcja zwraca opis LaunchDescription wskazujący na kolejne węzły jakie zostaną uruchomione.
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='example_tsr_project',  # nazwa pakietu, w którym znajduje się węzeł
            executable='new_talker_node_name',  # nazwa z entry_points w setup.py (po lewo =)
            name='talker_node',  # nazwa węzła, może być taka jak w pliku wykonywalnym albo dowolna (wtedy można uruchomić ten sam węzeł wiele razy pod inną nazwą.
            output='screen',
            parameters=[{'message_frequency': 2.0}]  # Przykładowy parametr
        ),
        Node(
            package='example_tsr_project',
            executable='simple_subscriber',
            name='subscriber_node',
            output='screen'
        )
    ])

