#! /usr/bin/env python3
import rospy
import os, sys, time ,datetime
import numpy as np
import matplotlib.pyplot as plt

import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

sys.path.append("/home/amigos/ros/src/evaluation_system/scripts")
from . import iv_readear

class sis_iv(object):
    def __init__(self):

        self.pub_vol = rospy.Publisher("sis_vol_cmd", Float64, queue_size=1)

        reader = iv_readear.iv_readear()

        self.t = datetime.datetime.now()
        self.ut = self.t.strftime("%Y%m%d-%H%M%S")

    def measure(self, initv=-10, interval=0.1, repeat=200):
        for i in range(repeat+1):
            da = []
            vol = initv + interval*i
            msg = Float64()
            msg.data = vol
            self.pub_vol.publish(vol)
            time.sleep(0.1)
            ret = reader.iv_readear()
            da.append(ret[0])
            da.append(ret[1])
            da_all.append(da)
            numpy.savetxt("sis_iv_{0}.txt".format(ut), numpy.array(da_ll), delimiter=" ")


    def iv_plot(self):
        print("a")
        plt.title("SIS-IV")
        plt.xlabel("vol[mV]")
        plt.ylabel("cur[uA]")
        iv = numpy.loadtxt("sis_iv_{0}.txt".format(ut))
        plt.plot(iv[:,0], iv[:,1], linestyle='solid', marker=None, color="red")
        plt.savefig("sis_iv_{0}.png".format(ut))


if __name__ == "__main__" :
    rospy.init_node("sis_iv_measure")
    iv = sis_iv()
    iv.start_thread()
    iv.measure()





"""
import rospy
import std_msgs
import time
from std_msgs.msg import Float64
rospy.init_node("test")
initv=-10
interval=0.1
repeat=200
pub_vol = rospy.Publisher("sis_vol_cmd", Float64, queue_size=1)
for i in range(repeat+1):
    vol = initv + interval*i
    msg = Float64()
    msg.data = vol
    pub_vol.publish(vol)
    time.sleep(0.1)
"""
