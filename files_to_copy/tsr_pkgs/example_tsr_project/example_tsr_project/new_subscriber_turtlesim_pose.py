import rclpy # import biblioteki do obsługi ROS2
import math
from rclpy.node import Node
from turtlesim.msg import Pose  # Import wiadomości ROS2 typu Pose z pakietu turtlesim

class TurtlePoseSubscriber(Node):  # Utworzenie klasy dla Node'a
	def __init__(self):
		super().__init__('turtlesim_pose_subscriber')  # unikalna nazwa node'a
		
		# Utworzenie atrybutu klasy będącego Subscriberem wiadomości typu Pose na temacie /turtle1/pose.
		self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.callback, 10)

	def callback(self, msg):
		x = msg.x
		y = msg.y
		theta = math.degrees(msg.theta)
		self.get_logger().info(f'{x=}, {y=}, {theta=} stopni')
		
		
def main(args=None):
	# Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
	rclpy.init(args=args)
	
	# Utworzenie nowego obiektu węzła ROS2 na podstawie klasy TurtlePoseSubscribr
	node = TurtlePoseSubscriber() 

	# Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
	rclpy.spin(node)  
	
	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
	node.destroy_node()
	
	# Zamyka połączenie z ROS2.
	rclpy.shutdown() 
		
if __name__ == '__main__':
	# uruchomienie node'a
	main() 
