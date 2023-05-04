#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
from sensor_msgs.msg import Joy
import socket
class MyPublisherNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(MyPublisherNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.axes = [0.0]*8 #[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.buttons = [0]*15 #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.pub = rospy.Publisher('/myrobot/joy', Joy, queue_size=1)
        #self.sub = rospy.Subscriber('/myrobot/wheels_driver_node/wheels_cmd_executed', String, self.callback)
        rospy.on_shutdown(self.my_shutdown)
        self.PORT = 5555
        self.HOST = ""
        self.open_server()


    def open_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allowing host to reuse port if already open
            self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1) #disable concatenation of packets (nagles algorithm)
            self.s.bind((self.HOST, self.PORT))
            self.s.listen()
            self.conn,self.addr = self.s.accept()

    #def callback(self, data):
    #    rospy.loginfo("I heard %s", data.data)
    #    self.conn.send(b"hiya!")

    def my_shutdown(self): #close tcp connection before shutting down node
        self.axes = [0.0] * 8        
        self.pub.publish(Joy(header=None,axes=self.axes,buttons=self.buttons))
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close() #without this the bot will never turn off
    def run(self):
        # publish message every 1 second
        #rate = rospy.Rate(0.1)
        #while not rospy.is_shutdown():
        #    msg = Joy(header=None,axes=self.axes,buttons=self.buttons)
        #    self.pub.publish(msg)
        #    rate.sleep()
        
        with self.conn:
            while not rospy.is_shutdown():
                data = self.conn.recv(1024)
                if not data:
                    break
                data = data.decode("utf-8").split(";")[-2].split(":") #message format: "{forward}:{steering};"
                self.axes[1] = float(data[0])
                self.axes[3] = float(data[1])

                    #self.axes[1], self.axes[3] = unpack("<2d",data)
                    
                msg = Joy(header=None, axes = self.axes, buttons=self.buttons)
                self.pub.publish(msg)
                    #conn.sendall(data)
                #msg = Joy(header=None,axes=self.axes,buttons=self.buttons)
                #self.pub.publish(msg)
            #s.close()
            #self.axes[1] =0.0
            #self.axes[3] =0.0
            #self.pub.publish(Joy(header=None,axes=self.axes,buttons=self.buttons))
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
