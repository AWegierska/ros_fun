# Jazda na podstawie https://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal
import rclpy
from rclpy.node import Node
from example_tsr_msgs.srv import AddGoToPose
from geometry_msgs.msg import Pose



class TurtleClient(Node):
    def __init__(self):
        super().__init__('turtle_client')
        self.client = self.create_client(AddGoToPose, 'turtle_go_to_pose')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Oczekiwanie na dostępność serwisu...")

    def send_goal(self, x, y):
        request = AddGoToPose.Request()
        request.goal_pose.x = x
        request.goal_pose.y = y

        self.get_logger().info(f"Wysyłanie żądania dojazdu do: X={x}, Y={y}")
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        if response:
            self.get_logger().info(f"Odpowiedź: success={response.success}, message='{response.message}'")
        else:
            self.get_logger().error("Brak odpowiedzi z serwera.")

def main():
    rclpy.init()
    client = TurtleClient()
    client.send_goal(3.0, 3.0)  # Przykładowa pozycja docelowa
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

