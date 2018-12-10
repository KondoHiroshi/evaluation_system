#! /usr/bin/env python3
import rospy
import os, sys, time ,datetime
import numpy as np
import matplotlib.pyplot as plt

import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int64

sys.path.append("/home/amigos/ros/src/evaluation_system/scripts")
import tz_reader

os.chdir("/home/amigos/TZ")

class yfactor(object):
    def __init__(self):

        self.pub_vol_ch1 = rospy.Publisher("sis_vol_cmd_ch1", Float64, queue_size=1)
        self.pub_vol_ch2 = rospy.Publisher("sis_vol_cmd_ch2", Float64, queue_size=1)
        self.pub_vol_ch3 = rospy.Publisher("sis_vol_cmd_ch3", Float64, queue_size=1)
        self.pub_vol_ch4 = rospy.Publisher("sis_vol_cmd_ch4", Float64, queue_size=1)

        self.t = datetime.datetime.now()
        self.ut = self.t.strftime("%Y%m%d-%H%M%S")

    def measure_hot(self, initv, interval, repeat):
        da_all = []
        for i in range(repeat+1):
            da = []
            vol = initv+interval*i
            msg = Float64()
            msg.data = vol
            self.pub_vol_ch1.publish(vol)
            self.pub_vol_ch2.publish(vol)
            self.pub_vol_ch3.publish(vol)
            self.pub_vol_ch4.publish(vol)
            time.sleep(0.1)
            ret = reader.piv_reader()
            time.sleep(0.01)
            da.append(ret[0])
            da.append(ret[1])
            da.append(ret[2])
            da.append(ret[3])
            da.append(ret[4])
            da.append(ret[5])
            print(da)
            da_all.append(da)
            time.sleep(0.01)
            np.savetxt("yfactor_hot_{0}_{1}.txt".format(self.ut,save_name), np.array(da_all), delimiter=" ")

    def pv_iv_plot(self):
        hot = np.loadtxt("yfactor_hot_{0}_{1}.txt".format(self.ut,save_name))
        fig ,(ax1, ax3) = plt.subplots(ncols=2, figsize=(12,4))
        ax2 = ax1.twinx()
        ax1.scatter(hot[:,0], hot[:,1],linestyle='solid', marker=".", color="green" ,label='I-V')
        ax2.scatter(hot[:,0], hot[:,2],linestyle='solid', marker=".", color="red", label='HOT')
        ax1.set_title("yfactor_Hot_Cold_measurement_ch1")
        ax1.set_xlabel("voltage[mV]")
        ax1.set_ylabel("current[uA]")
        ax2.set_ylabel("power[dBm]")
        ax2.legend(loc='upper right')

        ax4 = ax3.twinx()
        ax3.scatter(hot[:,3], hot[:,4],linestyle='solid', marker=".", color="green" ,label='I-V')
        ax4.scatter(hot[:,3], hot[:,5],linestyle='solid', marker=".", color="red", label='HOT')
        ax3.set_title("yfactor_Hot_Cold_measurement_ch2")
        ax3.set_xlabel("voltage[mV]")
        ax3.set_ylabel("current[uA]")
        ax4.set_ylabel("power[dBm]")
        ax4.legend(loc='upper right')

        plt.subplots_adjust(wspace=1.0, hspace=1.0)

        plt.savefig("yfactor_hot_{0}_{1}.png".format(self.ut,save_name))
        plt.show()



if __name__ == "__main__" :
    rospy.init_node("yfactor_hotcold")
    reader = tz_reader.reader()
    yf = yfactor()
    initv = int(input("start_voltage = ? [mV]"))
    lastv = int(input("finish_voltage = ? [mV]"))
    interval = float(input("interval_voltage = ? [mV]"))
    save_name = str(input("save_name="))
    repeat = int((lastv-initv)/interval)
    input("Are you ready HOT measurement?\n Press enter")
    print("Measuring HOT")
    yf.measure_hot(initv,interval,repeat)
    sys.exit(yf.pv_iv_plot())

#20181204
#change for tz
#written by H.Kondo
