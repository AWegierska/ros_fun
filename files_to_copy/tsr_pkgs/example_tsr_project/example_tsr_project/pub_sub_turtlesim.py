import rclpy # import biblioteki do obsługi ROS2
from rclpy.node import Node
from turtlesim.msg import Pose # Import wiadomości ROS2 typu Pose z pakietu turtlesim
from geometry_msgs.msg import Twist # Import wiadomości ROS2 typu Twist z pakietu geometry_msgs

class ContinuousMovementTurtlesim(Node):  # Utworzenie klasy dla Node'a
	def __init__(self):
		super().__init__('continuous_turtle_movement')  # unikalna nazwa node'a
		self.direction_right = True  # Odpowiada za nadzorowanie kierunku ruchu robota True - w prawo, False - w lewo
		# Utworzenie atrybutu klasy będącego Publisherem wiadomości typu Twist na temacie /turtle1/cmd_vel.
		self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
		
		# Utworzenie atrybutu klasy będącego Subscriberem wiadomości typu Pose na temacie /turtle1/pose.
		self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.callback, 10)

	def callback(self, pose_msg):
		# Subscriber odbiera informację o położeniu i je analizuje. W funkcji pojawia się wysłanie wiadomości		
		vel_msg = Twist()
		if self.direction_right:
			vel_msg.linear.x = 0.5
			vel_msg.angular.z = 0.0
		else:
			vel_msg.linear.x = -0.5
			vel_msg.angular.z = 0.0

		if pose_msg.x > 7:
			self.direction_right = False
		elif pose_msg.x < 2:
			self.direction_right = True

		# wysłanie przeanalizowanych danych    
		self.publisher_.publish(vel_msg)

		
def main(args=None):
	# Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
	rclpy.init(args=args)
	
	# Utworzenie nowego obiektu węzła ROS2 na podstawie klasy ContinuousMovementTurtlesim
	node = ContinuousMovementTurtlesim() 

	# Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
	rclpy.spin(node)  
	
	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
	node.destroy_node()
	
	# Zamyka połączenie z ROS2.
	rclpy.shutdown() 
		
if __name__ == '__main__':
	# uruchomienie node'a
	main() 
