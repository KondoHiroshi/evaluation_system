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
import sis_reader

os.chdir("/home/amigos/")

class sis_iv(object):
    def __init__(self):

        self.pub_vol = rospy.Publisher("sis_vol_cmd", Float64, queue_size=1)

        self.t = datetime.datetime.now()
        self.ut = self.t.strftime("%Y%m%d-%H%M%S")
        initv = input("start_voltage = ? [mV]")
        lastv = input("finish_voltage = ? [mV]")
        interval = input("interval_voltage = ? [mV]")

        repeat = (int(lastv)-int(initv))/float(interval)

    def measure(self, initv, interval, repeat):
        da_all = []
        for i in range(repeat+1):
            da = []
            vol = initv + interval*i
            msg = Float64()
            msg.data = vol
            self.pub_vol.publish(vol)
            time.sleep(0.1)
            ret = reader.iv_reader()
            da.append(ret[0])
            da.append(ret[1])
            print(da)
            da_all.append(da)
            np.savetxt("sis_iv_{0}.txt".format(self.ut), np.array(da_all), delimiter=" ")
        iv.iv_plot()

    def iv_plot(self):
        plt.title("SIS-IV")
        plt.xlabel("V[mV]")
        plt.ylabel("I[uA]")
        iv = np.loadtxt("sis_iv_{0}.txt".format(self.ut))
        plt.plot(iv[:,0], iv[:,1], linestyle='solid', marker=None, color="red")
        plt.savefig("sis_iv_{0}.png".format(self.ut))
        plt.show()

if __name__ == "__main__" :
    rospy.init_node("sis_iv_measure")
    reader = sis_reader.sis_reader()
    iv = sis_iv()
    sys.exit(iv.measure())
