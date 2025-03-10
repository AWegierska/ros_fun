import rclpy  # import biblioteki do obsługi ROS2
from rclpy.node import Node
from example_tsr_msgs.srv import ExampleSrvType  # Import wiadomości serwisowej ROS2 typu ExampleSrvType z pakietu example_tsr_msgs


class ExampleServiceClient(Node):  # Utworzenie klasy dla Node'a
    def __init__(self):
        super().__init__('example_service_client')  # unikalna nazwa node'a
        
        # Utworzenie atrybutu klasy będącego Klientem serwisowym wysyłającym żądanie typu ExampleSrvType na serwisie o podanej nazwie /example_service. Nie następuje jeszcze wysłanie.
        self.client = self.create_client(ExampleSrvType, 'example_service')

		# Pętla oczekująca na dostępność serwisu. Jeśli nie jest jeszcze uruchomiony to zapobiega wystąpienia błędu wynikającego z jego braku.
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Oczekiwanie na dostępność serwisu...')

    def send_request(self, value):  # metoda od wysyłania żądania na serwer. value jest dowolną przekazywaną wartością typu int
    	# Utworzenie żądania. Zwrócić uwagę na pojawiający się po . Request()
        request = ExampleSrvType.Request()
        
        # Uzupełnienie pola wiadomości przekazaną w metodzie klasy wartością value.
        request.request_value = value 

        self.get_logger().info(f'Wysyłanie żądania z wartością: {value}')
        
        # Wywołuje serwis asynchronicznie (bez blokowania programu), wysyłając request do serwera. Zwraca obiekt future, który reprezentuje przyszłą odpowiedź od serwera.
        future = self.client.call_async(request)
        
        # Gwarantuje, że program nie przejdzie dalej, dopóki serwer nie zwróci odpowiedzi.
        rclpy.spin_until_future_complete(self, future)
        
        # Pobiera wynik z future, czyli faktyczną odpowiedź zwróconą przez serwer.
        response = future.result()
        if response:
            self.get_logger().info(f'Odpowiedź serwera: success={response.success}, message="{response.message}"')
        else:
            self.get_logger().error('Błąd podczas komunikacji z serwerem.')


def main():
	# Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()

    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy ExampleServiceClient
    client_node = ExampleServiceClient()
    
    # Wysłanie żądania na serwer /example_service
    client_node.send_request(10)  
    
	# Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    client_node.destroy_node()
    
	# Zamyka połączenie z ROS2.
    rclpy.shutdown()


if __name__ == '__main__':
	# uruchomienie node'a
    main()


