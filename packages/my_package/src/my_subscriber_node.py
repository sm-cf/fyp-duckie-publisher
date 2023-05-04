#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
from duckietown_msgs.msg import WheelsCmdStamped
import socket
class MySubscriberNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(MySubscriberNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.sub = rospy.Subscriber('/myrobot/wheels_driver_node/wheels_cmd_executed', WheelsCmdStamped, self.callback)
                                   #'/myrobot/wheels_driver_node/wheels_cmd_executed'
        self.PORT = 5556
        self.HOST = ""
        self.open_server()
        rospy.on_shutdown(self.my_shutdown)

    def open_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allowing host to reuse port if already open
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1) #disable concatenation of packets (nagles algorithm)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        self.conn,self.addr = self.s.accept()
        #self.conn.send(b"poop")

    def my_shutdown(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def callback(self, data):
        #rospy.loginfo("I heard %s", data.vel_left)
        try:
            self.conn.send(bytes(f"{data.vel_left}:{data.vel_right};",encoding="utf-8"))
        except:
            return

if __name__ == '__main__':
    # create the node
    node = MySubscriberNode(node_name='my_subscriber_node')
    # keep spinning
    rospy.spin()