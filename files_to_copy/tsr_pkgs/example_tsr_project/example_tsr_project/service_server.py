import rclpy  # import biblioteki do obsługi ROS2
from rclpy.node import Node
from example_tsr_msgs.srv import ExampleSrvType  # Import wiadomości serwisowej ROS2 typu ExampleSrvType z pakietu example_tsr_msgs

class ExampleServiceServer(Node):  # Utworzenie klasy dla Node'a
    def __init__(self):
        super().__init__('example_service_server')  # unikalna nazwa node'a
        
        # Utworzenie atrybutu klasy będącego Serwerem serwisowym obsługującym wiadomość typu ExampleSrvType na serwisie o podanej nazwie /example_service. Po otrzymaniu żądania wywoływana jest natychmiast metoda self.service_callback
        self.srv = self.create_service(ExampleSrvType, 'example_service', self.service_callback)
        self.get_logger().info('Serwis example_service uruchomiony.')

    def service_callback(self, request, response):
    	# request - żądanie wysłane przez klienta. Dostępne pola wynikają ze struktury wiadomości, które znajdują się nad ---
    	# response - odpowiedź wysłana przez serwer dla klienta. Dostępne pola wynikają ze struktury wiadomości, które znajdują się pod ---
        self.get_logger().info(f'Przetwarzanie żądania: {request.request_value}')

        # Logika przetwarzania żądania
        if request.request_value > 0:
            response.success = True
            response.message = "Otrzymano wartość dodatnią."
        else:
            response.success = False
            response.message = "Wartość musi być większa od zera."

		# Zwrócenie odpowiedzi
        return response

def main(args=None):
	# Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()
    
    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy ExampleServiceServer
    node = ExampleServiceServer()

	# Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
    rclpy.spin(node)

	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()

    # Zamyka połączenie z ROS2.
    rclpy.shutdown()

if __name__ == '__main__':
	# uruchomienie node'a
    main()

