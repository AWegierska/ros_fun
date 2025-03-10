import rclpy # import biblioteki do obsługi ROS2
from rclpy.node import Node
from example_tsr_msgs.msg import ExampleMsgType  # Import wiadomości ROS2 typu ExampleMsgType z pakietu example_tsr_msgs

class SimpleSubscriber(Node):  # Utworzenie klasy dla Node'a
	def __init__(self):
		super().__init__('simple_subscriber')  # unikalna nazwa node'a
		
		# Utworzenie atrybutu klasy będącego Subscriberem wiadomości typu ExampleMsgType na temacie /new_unique_topic_name.
		self.subscription = self.create_subscription(ExampleMsgType, '/new_unique_topic_name', self.callback, 10)

	def callback(self, msg):
		self.get_logger().info(f'Id wiadomości: {msg.id} \nOdebrano: {msg}')


def main(args=None):
	# Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
	rclpy.init(args=args)
	
	# Utworzenie nowego obiektu węzła ROS2 na podstawie klasy SimpleSubscriber
	node = SimpleSubscriber() 

	# Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
	rclpy.spin(node)  
	
	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
	node.destroy_node()
	
	# Zamyka połączenie z ROS2.
	rclpy.shutdown() 
		
if __name__ == '__main__':
	# uruchomienie node'a
	main() 
