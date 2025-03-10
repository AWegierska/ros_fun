from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'example_tsr_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('config', '*.rviz'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'new_talker_node_name = example_tsr_project.new_publisher:main',
        	'turtle1_cmd_vel_pub = example_tsr_project.new_publisher_turtlesim_velocities:main',
        	'simple_subscriber = example_tsr_project.new_subscriber:main',
        	'turtle1_pose_sub = example_tsr_project.new_subscriber_turtlesim_pose:main',
        	'turtle1_continuous_movement = example_tsr_project.pub_sub_turtlesim:main',
     		'service_server = example_tsr_project.service_server:main',
     		'service_client = example_tsr_project.service_client:main',
     		'turtle_controller = example_tsr_project.turtle_controller:main',
     		'turtle_client = example_tsr_project.turtle_client:main',
     		'goto_pose_action_server = example_tsr_project.go_to_pose_action_server:main',
     		'goto_pose_action_client = example_tsr_project.go_to_pose_action_client:main',
     		'parameters_node = example_tsr_project.parameters_node:main',
     		'tf_static_broadcaster = example_tsr_project.tf_static_broadcaster:main',
		'tf_dynamic_broadcaster = example_tsr_project.tf_dynamic_broadcaster:main',
		'tf_listener = example_tsr_project.tf_listener:main',
        ],
    },
)
