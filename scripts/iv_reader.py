#! /usr/bin/env python3
import rospy
import os, sys, time ,datetime

import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32


class iv_readear(objevt):
    def __init__(self):
        rospy.Subscriber("sis_vol", Float64, self.vol_switch)
        rospy.Subscriber("sis_cur", Float64, self.cur_switch)

    def vol_switch(self,q):
        self.vol = q.data

    def cur_switch(self,q):
        self.cur = q.data

    def iv_readear(self):
        ad = []
        ad.append(self.vol)
        ad.append(self.cur)
        return da

if __name__ == "__main__" :
    rospy.init_node("iv_readear")
    rospy.spin()
