import rclpy
import math
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


def create_pose(nav, x, y, yaw=0.0):
    pose = PoseStamped()
    pose.header.frame_id = "map"
    pose.header.stamp = nav.get_clock().now().to_msg()

    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(yaw / 2)
    pose.pose.orientation.w = math.cos(yaw / 2)

    return pose


def navigate(nav, x, y, yaw=0.0):
    goal = create_pose(nav, x, y, yaw)

    # Nav2 handles path planning and obstacle avoidance
    nav.goToPose(goal)

    while not nav.isTaskComplete():
        feedback = nav.getFeedback()

        if feedback:
            print("Distance remaining:", feedback.distance_remaining)

    return nav.getResult() == TaskResult.SUCCEEDED


def drop_off():
    # TODO: Connect robotic arm using MoveIt
    print("Dropping off object")


def main():
    rclpy.init()
    nav = BasicNavigator()

    # TODO: Replace with actual starting pose and destination
    home = (0.0, 0.0, 0.0)
    destination = (3.0, 2.0, 0.0)

    nav.setInitialPose(create_pose(nav, *home))
    nav.waitUntilNav2Active()

    # Navigate to destination
    if navigate(nav, *destination):
        drop_off()

        # Return to starting position
        if navigate(nav, *home):
            print("Delivery completed!")
        else:
            print("Return failed!")
    else:
        print("Destination unreachable!")

    nav.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()