import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.node import ParameterDescriptor
from rcl_interfaces.msg import SetParametersResult
from geometry_msgs.msg import Twist  # Import wiadomości ROS2 typu Twist z pakietu geometry_msgs
import time

class RobotController(Node):
    """
    Węzeł odpowiedzialny za wysyłanie maksymalnej prędkości obrotowej wynikającej
    z ustawionego parametru. Zmiana wartości parametru robot_max_w powoduje zmianę
    prędości obrotowej robota.
    """
    def __init__(self):
        super().__init__('robot_controller')

        # Deklarowanie parametrów z wartościami domyślnymi
        self.declare_parameter('robot_max_v', 0.0)
        self.declare_parameter('robot_max_w', 1.0)
        self.declare_parameter('robot_type', 'default_type')

        # Parametr tylko do odczytu
        self.declare_parameter('robot_id', 'ROBOT_001', descriptor=ParameterDescriptor(read_only=True))

        # Pobranie wartości parametrów
        self.robot_max_v = self.get_parameter('robot_max_v').value
        self.robot_max_w = self.get_parameter('robot_max_w').value
        self.robot_type = self.get_parameter('robot_type').value
        self.robot_id = self.get_parameter('robot_id').value  # Read-only

		# Utworzenie atrybutu klasy będącego Publisherem wiadomości typu Twist na temacie /turtle1/cmd_vel.
        self.vel_publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
		# Utworzenie timera, co 0.2s wywołuje się metoda self.timer_callback
        self.timer = self.create_timer(0.2, self.timer_callback)
		
        self.get_logger().info(f'Starting robot {self.robot_id} with max speed:\n-linear {self.robot_max_v} \n-angular: {self.robot_max_w}')

        # Subskrypcja zmiany parametrów w czasie działania
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        """
        Funkcja wywoływana przy zmianie parametrów
        """
        # Aktualizacja wartości parametrów
        for param in params:
            if param.name == "robot_max_v" and param.type_ == Parameter.Type.DOUBLE:
                self.robot_max_v = param.value
                self.get_logger().info(f'Updated linear speed: {self.robot_max_v}')
            elif param.name == "robot_max_w" and param.type_ == Parameter.Type.DOUBLE:
                self.robot_max_w = param.value
                self.get_logger().info(f'Updated angular speed: {self.robot_max_w}')
            elif param.name == "robot_type" and param.type_ == Parameter.Type.STRING:
                self.robot_type = param.value
                self.get_logger().info(f'Updated type: {self.robot_type}')
            elif param.name == "robot_id":
                self.get_logger().warning("Attempt to change read-only parameter 'robot_id' was blocked.")
        
        # Wysłanie informacji o pomyślnym zakończeniu procedury zmiany parametrów
        return SetParametersResult(successful=True)  

    def timer_callback(self):
        msg = Twist()  # Utworzenie wiadomości ROS2 typu Twist

		# Uzupełnienie pól wiadomości
        msg.linear.x = 2.0
        msg.angular.z = self.robot_max_w
		
		# Wysłanie wiadomości
        self.vel_publisher_.publish(msg)

		
def main(args=None):
    # Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init(args=args)

    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy RobotController
    node = RobotController()
    # Obsługa błędu wynikająca z pojawiania się przerwania z klawiatury ctrl+c
    try:
    	# Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
        rclpy.spin(node)  # Obsługa zdarzeń ROS2
    except KeyboardInterrupt: 
        node.get_logger().info("Shutting down Robot Controller.")

	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()

    # Zamyka połączenie z ROS2.
    rclpy.shutdown()

if __name__ == '__main__':
    main()

