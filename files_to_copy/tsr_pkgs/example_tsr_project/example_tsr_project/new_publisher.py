import rclpy # import biblioteki do obsługi ROS2
from rclpy.node import Node
from example_tsr_msgs.msg import ExampleMsgType  # Import wiadomości ROS2 typu ExampleMsgType z pakietu example_tsr_msgs

class SimplePublisher(Node):  # Utworzenie klasy dla Node'a
	def __init__(self):
		super().__init__('simple_publisher')  # unikalna nazwa node'a
		
		# Utworzenie atrybutu klasy będącego Publisherem wiadomości typu ExampleMsgType na temacie /new_unique_topic_name.
		self.publisher_ = self.create_publisher(ExampleMsgType, '/new_unique_topic_name', 10)
		
		# Utworzenie timera, co 1s wywołuje się metoda self.timer_callback
		self.timer = self.create_timer(1.0, self.timer_callback)  
		
	def timer_callback(self):
		msg = ExampleMsgType()  # Utworzenie wiadomości ROS2 typu ExampleMsgType

		# Uzupełnienie pól wiadomości
		msg.id = 123
		msg.name = "Nowa wiadomosc"
		msg.is_valid = True
		msg.dynamic_integer_array = [3, 4, 5]
		
		# Wysłanie wiadomości
		self.publisher_.publish(msg)
		
		# Wysłanie informacji do logów.
		self.get_logger().info(f'Opublikowano: {msg}') 
		
def main(args=None):
	# Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
	rclpy.init(args=args)
	
	# Utworzenie nowego obiektu węzła ROS2 na podstawie klasy SimplePublisher
	node = SimplePublisher() 

	# Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
	rclpy.spin(node)  
	
	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
	node.destroy_node()
	
	# Zamyka połączenie z ROS2.
	rclpy.shutdown() 
		
if __name__ == '__main__':
	# uruchomienie node'a
	main() 
