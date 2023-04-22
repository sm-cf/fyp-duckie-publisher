#!/usr/bin/env python3

# import external libraries
import rospy

# import libraries which are part of the package (i.e. in the include dir)
#import library

# import DTROS-related classes
from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType #,DTReminder

# import messages and services
from std_msgs.msg import Float32
from duckietown_msgs.msg import SegmentList, Segment, BoolStamped
from sensor_msgs.msg import Joy

class myJoystickNode(DTROS):
    def __init__(self, node_name):
        super(myJoystickNode, self).__init__(
            node_name=node_name,
            node_type=NodeType.PERCEPTION
        )
        
        # Setting up parameters
        self.detection_freq = DTParam(
            '~detection_freq',
            param_type=ParamType.INT,
            min_value=-1,
            max_value=30
        )
        # ...
        
        # Generic attributes
        self.axes = [0.0,0.0,1.0,0.0,0.,0.0,0.0,0.0]
        self.buttons = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        # ...

        # Publishers
        self.pub = rospy.Publisher(
            '~joy',
            Joy,
            queue_size=1,
            dt_topic_type=TopicType.VISUALIZATION
        )


if __name__ == '__main__':
    jn = myJoystickNode(node_name='my_joystick_node')
    jn.run()
    msg = Joy(header=None,axes=jn.axes,buttons=jn.buttons)
    jn.pub.publish(msg)
    rospy.signal_shutdown(jn)
    #rospy.spin()
