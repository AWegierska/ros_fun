import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from turtlesim.msg import Pose
from example_tsr_msgs.srv import AddGoToPose


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')  # unikalna nazwa node'a
        # Serwis
        self.srv = self.create_service(AddGoToPose, 'turtle_go_to_pose', self.add_go_to_pose_callback)

        # Publikowanie prędkości
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Publikowanie statusu
        self.status_publisher = self.create_publisher(String, '/turtle1/status', 10)

        # Subskrypcja pozycji
        self.pose_subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # Aktualna pozycja
        self.current_pose = Pose()
        # Aktualny status
        self.current_status = String()
        
        # Lista aktualnych celów do których ma dojechać robot.
        self.goals = []
        # Utworzenie timera, co 1s wywołuje się metoda self.timer_callback
        self.timer = self.create_timer(0.1, self.movement_callback)
        self.get_logger().info("Serwer turtle_go_to_pose uruchomiony.")

    def pose_callback(self, msg):
        """Aktualizacja bieżącej pozycji robota"""
        self.current_pose = msg       

    def add_go_to_pose_callback(self, request, response):
        """Obsługa żądania serwisowego - sterowanie robotem do celu"""
        self.get_logger().info(f'Otrzymano żądanie: X={request.goal_pose.x}, Y={request.goal_pose.y}')
        self.goals.append(request.goal_pose)
        response.success = True
        response.message = "Dodano nowy cel."
        self.get_logger().info(response.message)
        return response
                
    def movement_callback(self):
        if self.goals: 
            vel_msg = Twist()
            if self.euclidean_distance(self.goals[0]) >= 0.1:
		        # Porportional controller.
		        # https://en.wikipedia.org/wiki/Proportional_control

                if abs(self.angular_vel(self.goals[0])) > 0.2:
		            # Angular velocity in the z-axis.
                    vel_msg.angular.z = 0.6
                else:
		            # Linear velocity in the x-axis.
                    vel_msg.linear.x = self.linear_vel(self.goals[0])
		            # Angular velocity in the z-axis.
                    vel_msg.angular.z = self.angular_vel(self.goals[0])

		        # Publishing our vel_msg
                self.cmd_vel_publisher.publish(vel_msg)
                self.current_status.data = "IN PROGRESS"
                self.status_publisher.publish(self.current_status)   
            else:
                vel_msg.linear.x = 0.0
                vel_msg.angular.z = 0.0
                self.cmd_vel_publisher.publish(vel_msg)

                self.current_status.data = "DONE"
                self.status_publisher.publish(self.current_status)
                del self.goals[0]
        else:
            self.current_status.data = "FREE"
            self.status_publisher.publish(self.current_status)
  
    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return math.sqrt(math.pow((goal_pose.x - self.current_pose.x), 2) +
                         math.pow((goal_pose.y - self.current_pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        vel = constant * self.euclidean_distance(goal_pose)
        return min(max(-1.5, vel), 1.5)

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return math.atan2(goal_pose.y - self.current_pose.y, goal_pose.x - self.current_pose.x)

    def angular_vel(self, goal_pose, constant=6.0):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * (self.steering_angle(goal_pose) - self.current_pose.theta)


def main():
    # Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()
    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy SimplePublisher
    node = TurtleController()
    # Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
    rclpy.spin(node)
    # Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()
    # Zamyka połączenie z ROS2.
    rclpy.shutdown()

if __name__ == '__main__':
    main()

