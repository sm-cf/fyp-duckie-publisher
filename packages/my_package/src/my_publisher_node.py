#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
from sensor_msgs.msg import Joy
class MyPublisherNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(MyPublisherNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.axes = [0.0,1.0,0.0,0.0,0.,0.0,0.0,0.0]
        self.buttons = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.done = False
        self.pub = rospy.Publisher('/myrobot/joy', Joy, queue_size=1)

    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(0.1)
        while not rospy.is_shutdown():
            msg = Joy(header=None,axes=self.axes,buttons=self.buttons)
            self.pub.publish(msg)
            rate.sleep()
        
        return
        rate = rospy.Rate(1) # 1Hz
        while not rospy.is_shutdown():
            message = "Hello World! from %s" % os.environ['VEHICLE_NAME']
            rospy.loginfo("Publishing message: '%s'" % message)
            self.pub.publish(message)
            rate.sleep()

if __name__ == '__main__':
    # create the node
    node = MyPublisherNode(node_name='my_publisher_node')
    # run node
    node.run()
    # keep spinning
    rospy.spin()
