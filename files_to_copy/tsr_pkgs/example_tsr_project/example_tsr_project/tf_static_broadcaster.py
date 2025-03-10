import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

class StaticTFPublisher(Node):
    def __init__(self):
        super().__init__('tf_static_broadcaster')
        
        # Utworzenie obiektu umożliwiającego publikowanie statycznych transformat
        self.tf_broadcaster = StaticTransformBroadcaster(self)
        
        # Wywołanie metody odpowiedzialnej za opbulikowanie statycznej transformaty
        self.publish_static_transform()
    
    def publish_static_transform(self):
        # Utworzenie i uzupełnienie wiadomości dla transformaty
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        # Ustawienie układu współrzędnych będący układem odniesienia
        t.header.frame_id = 'base_link'
        # Nowy układ współrzędnych
        t.child_frame_id = 'sensor'
        # Współrzędne nowego układu wyrazone w układzie odniesienia
        t.transform.translation.x = 0.5
        t.transform.translation.y = 0.0
        t.transform.translation.z = 1.0
        t.transform.rotation.w = 1.0
        
        # Opublikowanie transformaty
        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info('Opublikowano statyczną transformację.')


def main():
    # Inicjalizacja ROS2 dla programu, musi być wykonana przed utworzeniem jakiegokolwiek węzła (node'a).
    rclpy.init()
    # Utworzenie nowego obiektu węzła ROS2 na podstawie klasy StaticTFPublisher
    node = StaticTFPublisher()

    # Spin umożliwia węzłowi ROS2 działanie i oczekuje na zdarzenia. Brak linii spowoduje natychmiastowe zakończenie działania programu.
    rclpy.spin(node) 

    # Usuwa węzeł przed zamknięciem programu. Zwalnia zasoby pamięci zajmowane przez ten obiekt.
    node.destroy_node()
    # Zamyka połączenie z ROS2.
    rclpy.shutdown()


if __name__ == '__main__':
    main()
