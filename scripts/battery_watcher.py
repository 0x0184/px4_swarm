#!/usr/bin/python
import subprocess

dist = subprocess.check_output('rosversion --distro', shell=True).replace('\n', '')

import rospy
if dist == 'kinetic':   # float32 percentage
    from sensor_msgs.msg import BatteryState
else:
    from mavros_msgs.msg import BatteryState

import pymysql.cursors
from datetime import datetime

DATABASE_HOST = 'localhost'
DATABASE_USER = 'root'
DATABASE_PASS = 'PASSWORD_OF_ROOT'
DATABASE_NAME = 'uavdb'

# Connect to the database
conn = pymysql.connect(host=DATABASE_HOST,
                        user=DATABASE_USER,
                        password=DATABASE_PASS,
                        db=DATABASE_NAME,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

def callback_with_system_id(message, system_id='1'):
    global conn
    rospy.loginfo("[battery_watcher] ID: {0}, Voltage: {1}".format(system_id, message.voltage))
    query = 'UPDATE realtime SET battery = %s, ReceiveDate = %s WHERE UAV_ID = %s'
    conn.cursor().execute(query, (message.voltage, datetime.now(), system_id))
    conn.commit()

def callback_generator(uav_id):
    return lambda message: callback_with_system_id(message, system_id=uav_id)

def listener():
    rospy.init_node('battery_watcher', anonymous=True)

    # Latitude Longitude GPSAltitude PressureAltitude ReceiveDate roll pitch raw
    # heading(orientation) flight_mode battery_status gps_status gps_time

    for i in xrange(1, 4):
        rospy.Subscriber('mavros{}/battery'.format(i), BatteryState, callback_generator(uav_id=i+1))
    rospy.spin()


if __name__ == '__main__':
    listener()