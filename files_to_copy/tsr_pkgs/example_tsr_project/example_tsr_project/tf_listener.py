import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros import Buffer, TransformListener

class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        # Buffer pozwala na przechowywanie historii transformacji, dzięki czemu można uzyskać przeszłe i przyszłe transformacje.
        self.tf_buffer = Buffer()
        # TransformListener to obiekt nasłuchujący, który odbiera dane o transformacjach publikowane w systemie ROS2. Nasłuchuje transformacje publikowane przez TransformBroadcaster i przechowuje je w tf_buffer.
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.lookup_transform)
    
    def lookup_transform(self):
        try:
            # pobiera transformację pomiędzy world (ramka nadrzędna) a base_link (ramka podrzędna). Wynik zawiera translację (x, y, z) oraz rotację (quaternion) między podanymi układami współrzędnych.
            tr = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
            self.get_logger().info(f"Transformacja: {tr}")
            self.get_logger().info(f"Wektor translacji: {tr.transform.translation}")
            self.get_logger().info(f"Przesuniecie x: {tr.transform.translation.x}")
            self.get_logger().info(f"Wektor rotacji: {tr.transform.rotation}")
            self.get_logger().info(f"rotacja w: {tr.transform.rotation.w}\n")
        except TransformException as e:
            self.get_logger().warn(f"Nie udało się pobrać transformacji: {str(e)}")


def main():
    # Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()
    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy TFListener
    node = TFListener()

    # Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
    rclpy.spin(node) 

    # Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()
    # Zamyka połączenie z ROS2.
    rclpy.shutdown()


if __name__ == '__main__':
    main()
