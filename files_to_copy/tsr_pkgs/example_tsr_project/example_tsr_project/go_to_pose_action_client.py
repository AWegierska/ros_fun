import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_tsr_msgs.action import GoToPose  # Import wiadomości dla akcji typu GoToPose z pakietu example_tsr_msgs
from turtlesim.msg import Pose


class GoToPoseActionClient(Node):
    def __init__(self):
        super().__init__('goto_pose_action_client')
        # Utworzenie klienta dla serwera akcji, który obsługuje typ wiadomości GoToPose dla akcji o nazwie (na temacie) 'goto_pose'
        self.action_client = ActionClient(self, GoToPose, 'goto_pose')

    def send_goal(self, x, y):
        """Wysyła cel do serwera akcji"""
        # Utworzenie wiadomości z celem.
        goal_msg = GoToPose.Goal()
        goal_msg.goal_pose = Pose()
        goal_msg.goal_pose.x = x
        goal_msg.goal_pose.y = y

        self.get_logger().info(f"Wysyłanie celu: ({x}, {y})")
        # Blokuje kod do momentu, aż serwer akcji (Action Server) stanie się dostępny.
        # Zastosowanie: Gdy klient akcji uruchamia się szybciej niż serwer i musi poczekać, aż serwer się podniesie.
        self.action_client.wait_for_server()

        # Wysyła żądanie wykonania akcji asynchronicznie (bez blokowania programu).
        # Klient od razu przechodzi do następnej operacji, nie czekając na zakończenie akcji.
        self.send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        
        # Po pewnym czasie serwer odpowiada, czy zaakceptował cel.
        # Jeśli tak, przechodzimy do oczekiwania na wynik końcowy. Do metody self.goal_response_callback
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Obsługuje odpowiedź serwera na żądanie celu"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Cel odrzucony przez serwer.")
            return

        self.get_logger().info("Cel zaakceptowany, czekam na wynik...")
        
        # Uruchamia asynchroniczne oczekiwanie na wynik akcji (goal_handle.get_result_async()).
        # Dzięki temu program nie blokuje się i może w międzyczasie obsługiwać inne operacje (np. otrzymywać feedback z serwera).
        self.get_result_future = goal_handle.get_result_async()
        
        # Gdy serwer akcji zakończy wykonywanie zadania, ta linia wywoła result_callback().
        # result_callback() odbierze wynik akcji i wyświetli komunikat końcowy. Przejście do metody self.result_callback
        self.get_result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        """Obsługuje odbiór feedbacku o postępie"""
        self.get_logger().info(f"Pozostała odległość do celu: {feedback_msg.feedback.distance_remaining:.2f}m")

    def result_callback(self, future):
        """Obsługuje odbiór wyniku końcowego akcji"""
        result = future.result().result
        self.get_logger().info(f"Wynik akcji: {result.message} (Sukces: {result.success})")


def main():
    # Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()
    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy GoToPoseActionClient
    node = GoToPoseActionClient()

    # Wysyłanie celu (np. x=5.0, y=3.0)
    node.send_goal(5.0, 3.0)

    # Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
    rclpy.spin(node)
    # Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()
    # Zamyka połączenie z ROS2.
    rclpy.shutdown()

if __name__ == '__main__':
    main()

