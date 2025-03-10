import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer  # Import obiektu do obsługi akcji
from example_tsr_msgs.action import GoToPose  # Import wiadomości dla akcji typu GoToPose z pakietu example_tsr_msgs
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from rclpy.executors import MultiThreadedExecutor  # Dodanie importu i wielowątkowość była konieczna do prawidłowego odczytu aktualnego położenia robota przez Subscriber pose_subscription podczas realizacji akcji dojazdu do punktu. Rozwiązało to problem z brakiem możliwości wysłania kolejnego celu.
import math
import time


class GoToPoseActionServer(Node):
    def __init__(self):
        super().__init__('goto_pose_action_server')
        # Utworzenie serwera dla akcji o nazwie 'goto_pose', który jest typu GoToPose. execute_callback jest to argument dla którego podaje się metode klasy lub inną funkcję, która ma zostać wykonana po odebraniu żądania dotyczącego wykonania akcji.
        self.action_server = ActionServer(
            self,
            GoToPose,
            'goto_pose',
            execute_callback=self.execute_callback)

        # Publikowanie prędkości
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # Odbiór pozycji
        self.pose_subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        # Aktualna pozycja
        self.current_pose = Pose()
        self.get_logger().info("Serwer akcji goto_pose uruchomiony.")

    def pose_callback(self, msg):
        """Aktualizacja bieżącej pozycji robota"""
        self.current_pose = msg   

    def execute_callback(self, goal_handle):
        """Obsługuje wykonanie akcji - nawigacja do pozycji"""
        self.get_logger().info(f"Rozpoczęto dojazd do: ({goal_handle.request.goal_pose.x}, {goal_handle.request.goal_pose.y})")

        goal = goal_handle.request.goal_pose
        success = False
        
        # Utworzenie wiadomości dla prędkości i Feedback
        vel_msg = Twist()
        feedback_msg = GoToPose.Feedback()

        # Rozpoczęcie autonomicznego dojazdu do celu
        while rclpy.ok():
            distance = self.euclidean_distance(goal)

            if distance >= 0.1:
                if abs(self.angular_vel(goal)) > 0.2:
                    vel_msg.angular.z = 0.6
                else:
                    vel_msg.linear.x = self.linear_vel(goal)
                    vel_msg.angular.z = self.angular_vel(goal)

                self.cmd_vel_publisher.publish(vel_msg)
            else:
                success = True
                vel_msg.linear.x = 0.0
                vel_msg.angular.z = 0.0
                self.cmd_vel_publisher.publish(vel_msg)
                break

            # Wysyłanie feedbacku
            feedback_msg.distance_remaining = distance
            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(f"Odległość do celu: {distance:.2f}m")

            time.sleep(0.1)  # Uniknięcie 100% obciążenia procesora

        # Wysłanie wyniku akcji
        result = GoToPose.Result()
        result.success = success
        result.message = "Robot dotarł do celu!" if success else "Nie udało się dotrzeć do celu."
        goal_handle.succeed()  # Ustawienie zakończenia obsługi akcji
        self.get_logger().info(result.message)

        return result  # odesłanie wyniku

    def euclidean_distance(self, goal_pose):
        """Odległość euklidesowa do celu"""
        return math.sqrt(math.pow((goal_pose.x - self.current_pose.x), 2) +
                         math.pow((goal_pose.y - self.current_pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        """Obliczanie prędkości liniowej"""
        vel = constant * self.euclidean_distance(goal_pose)
        return min(max(-1.5, vel), 1.5)

    def steering_angle(self, goal_pose):
        """Obliczanie kąta do sterowania"""
        return math.atan2(goal_pose.y - self.current_pose.y, goal_pose.x - self.current_pose.x)

    def angular_vel(self, goal_pose, constant=6.0):
        """Obliczanie prędkości kątowej"""
        return constant * (self.steering_angle(goal_pose) - self.current_pose.theta)


def main():
    # Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()
    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy GoToPoseActionServer
    node = GoToPoseActionServer()

    # Użycie MultiThreadedExecutor zamiast spin()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()

    # Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()
    # Zamyka połączenie z ROS2.
    rclpy.shutdown()


if __name__ == '__main__':
    main()

