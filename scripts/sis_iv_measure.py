#! /usr/bin/env python3
import rospy
import os, sys, time ,datetime
import numpy as np
import matplotlib.pyplot as plt

import threading
import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class sis_iv(object):
    def __init__(self):

        self.pub_vol = rospy.Publisher("sis_vol_cmd", Float64, queue_size=1)
        rospy.Subscriber("sis_vol", Float64, self.vol_switch)
        rospy.Subscriber("sis_cur", Float64, self.cur_switch)

        self.vol_list = []
        self.cur_list = []

        self.vol_flag = 0
        self.cur_flag = 0

        self.t = datetime.datetime.now()
        self.ut = self.t.strftime("%Y%m%d-%H%M%S")

    def vol_switch(self,q):
        self.vol = q.data

    def cur_switch(self,q):
        self.cur = q.data

    def vol_reader(self):
        while not rospy.is_shutdown():
            if self.vol_flag == 0:
                time.sleep(0.1)
                continue
            vol = self.vol
            self.vol_list.append(vol)
            continue

    def cur_reader(self):
        while not rospy.is_shutdown():
            if self.vol_flag == 0:
                time.sleep(0.1)
                continue
            self.cur_list.append(self.cur)
            continue

    def measure(self, initv=-10, interval=0.1, repeat=200):
        self.vol_flag = 1
        self.cur_flag = 1
        for i in range(repeat+1):
            vol = initv + interval*i
            msg = Float64()
            msg.data = vol
            self.pub_vol.publish(vol)
            time.sleep(0.1)
        self.vol_flag = 0
        self.cur_flag = 0
        self.iv_plot()
        plt.savefig("test_{0}.png".format(ut))
        plt.show()

    def iv_plot(self):
        print("a")
        plt.title("SIS-IV")
        plt.xlabel("vol[mV]")
        plt.ylabel("cur[uA]")
        x = self.vol_list
        y = self.cur_list
        plt.plot(x,y)
        plt.show()

    def start_thread(self):
        th1 = threading.Thread(target=self.vol_reader)
        th1.setDaemon(True)
        th1.start()
        th2 = threading.Thread(target=self.cur_reader)
        th2.setDaemon(True)
        th2.start()


if __name__ == "__main__" :
    rospy.init_node("sis_iv_measure")
    iv = sis_iv()
    iv.start_thread()
    iv.measure()
    rospy.spin()




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
