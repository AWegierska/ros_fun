import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math

class DynamicTFPublisher(Node):
    def __init__(self):
        super().__init__('tf_static_broadcaster')
        # Utworzenie obiektu umożliwiającego publikowanie dynamicznych transformat
        self.tf_broadcaster = TransformBroadcaster(self)
        # Utworzenie timera publikującego nowe wartości transformaty (wywołanie metody  broadcast_transform)
        self.timer = self.create_timer(0.1, self.broadcast_transform)
        self.angle = 0.0
    
    def broadcast_transform(self):
        # Utworzenie i uzupełnienie wiadomości dla transformaty
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
         # Ustawienie układu współrzędnych będący układem odniesienia
        t.header.frame_id = 'world'
        # Nowy układ współrzędnych
        t.child_frame_id = 'base_link'
        # Współrzędne nowego układu wyrazone w układzie odniesienia
        t.transform.translation.x = math.cos(self.angle)
        t.transform.translation.y = math.sin(self.angle)
        t.transform.translation.z = 0.0
        t.transform.rotation.w = 1.0
        
        # Opublikowanie transformaty
        self.tf_broadcaster.sendTransform(t)
        self.angle += 0.1


def main():
    # Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()
    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy DynamicTFPublisher
    node = DynamicTFPublisher()

    # Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
    rclpy.spin(node) 

    # Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()
    # Zamyka połączenie z ROS2.
    rclpy.shutdown()


if __name__ == '__main__':
    main()
