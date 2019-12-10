#!/bin/bash

gnome-terminal --window --command roscore
sleep 2

gnome-terminal --tab --command "rosrun turtlesim turtlesim_node"
sleep 2
rosservice call kill turtle1

#2
rosservice call spawn 2.2 2.5 0 turtle2
rosservice call turtle2/teleport_relative 2 3.14
rosservice call turtle2/teleport_relative 3 4.14
rostopic pub -1 /turtle2/cmd_vel geometry_msgs/Twist -- '[3.0, 0.0, 0.0]' '[0.0, 0.0, 3.5]'
rosservice call kill turtle2

#4
rosservice call spawn 3.2 2.5 1.57 turtle4
rosservice call turtle4/teleport_relative 3.8 0
rosservice call turtle4/teleport_relative 2.3 3.14
rosservice call turtle4/teleport_relative 1.3 4.71
rosservice call turtle4/teleport_relative 2.7 4.3
rosservice call kill turtle4

#3
rosservice call spawn 3.7 2.5 0 turtle3
rosservice call turtle3/teleport_relative 0.3 0
rostopic pub -1 /turtle3/cmd_vel geometry_msgs/Twist -- '[3.14, 0.0, 0.0]' '[0.0, 0.0, 3.14]'
rosservice call turtle3/teleport_relative 0.2 0
rosservice call turtle3/teleport_relative 0.2 3.14
rostopic pub -1 /turtle3/cmd_vel geometry_msgs/Twist -- '[3.14, 0.0, 0.0]' '[0.0, 0.0, 3.14]'
rosservice call kill turtle3

#9
rosservice call spawn 5.5 2.5 0 turtle9
rostopic pub -1 /turtle9/cmd_vel geometry_msgs/Twist -- '[5.3, 0.0, 0.0]' '[0.0, 0.0, 2.5]'
rostopic pub -1 /turtle9/cmd_vel geometry_msgs/Twist -- '[5, 0.0, 0.0]' '[0.0, 0.0, 5.7]'
rosservice call kill turtle9

#5
rosservice call spawn 8.0 2.5 0 turtle5
rostopic pub -1 /turtle5/cmd_vel geometry_msgs/Twist -- '[4.0, 0.0, 0.0]' '[0.0, 0.0, 3.14]'
rosservice call turtle5/teleport_relative 1.5 4.71
rosservice call turtle5/teleport_relative 1.5 4.71
rosservice call kill turtle5

#3
rosservice call spawn 9.8 2.5 0 turtle3
rosservice call turtle3/teleport_relative 0.3 0
rostopic pub -1 /turtle3/cmd_vel geometry_msgs/Twist -- '[3.14, 0.0, 0.0]' '[0.0, 0.0, 3.14]'
rosservice call turtle3/teleport_relative 0.2 0
rosservice call turtle3/teleport_relative 0.2 3.14
rostopic pub -1 /turtle3/cmd_vel geometry_msgs/Twist -- '[3.14, 0.0, 0.0]' '[0.0, 0.0, 3.14]'
rosservice call kill turtle3
