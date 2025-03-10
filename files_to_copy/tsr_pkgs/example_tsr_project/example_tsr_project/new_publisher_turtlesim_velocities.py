import rclpy # import biblioteki do obsługi ROS2
from rclpy.node import Node
from geometry_msgs.msg import Twist  # Import wiadomości ROS2 typu Twist z pakietu geometry_msgs

class VelTurtlePublisher(Node):  # Utworzenie klasy dla Node'a
	def __init__(self):
		super().__init__('turtlesim_cmd_vel_publisher')  # unikalna nazwa node'a. Jest to nazwa widoczna na liście ros2 node list. Uruchomienie wynikające z konfiguracji może mieć inną nazwę.
		
		# Utworzenie atrybutu klasy będącego Publisherem wiadomości typu Twist na temacie /turtle1/cmd_vel.
		self.vel_publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
		
		# Utworzenie timera, co 0.2s wywołuje się metoda self.timer_callback
		self.timer = self.create_timer(0.2, self.timer_callback)
		
	def timer_callback(self):
		msg = Twist()  # Utworzenie wiadomości ROS2 typu Twist

		# Uzupełnienie pól wiadomości
		msg.linear.x = 1.0
		msg.angular.z = 1.0
		
		# Wysłanie wiadomości
		self.vel_publisher_.publish(msg)

		
def main(args=None):
	# Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
	rclpy.init(args=args)
	
	# Utworzenie nowego obiektu węzła ROS2 na podstawie klasy VelTurtlePublisher
	node = VelTurtlePublisher() 

	# Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
	rclpy.spin(node)  
	
	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
	node.destroy_node()
	
	# Zamyka połączenie z ROS2.
	rclpy.shutdown() 
		
if __name__ == '__main__':
	# uruchomienie node'a
	main() 
