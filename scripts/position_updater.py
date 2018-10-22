#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
import pymysql.cursors
import datetime

DATABASE_HOST = 'localhost'
DATABASE_USER = 'root'
DATABASE_PASS = 'PASSWORD_OF_ROOT'
DATABASE_NAME = 'uavdb'

# Connect to the database
conn = pymysql.connect(host=DATABASE_HOST,
                        user=DATABASE_USR,
                        password=DATABASE_PASS,
                        db=DATABASE_NAME,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
"""
def callback(message):
    global conn
    rospy.loginfo(rospy.get_caller_id() + " received: (lat: {0}, lon: {1})".format(message.latitude, message.longitude))
    query = 'INSERT INTO realtime(uav_id, latitude, longitude, timestamp) VALUE(%s, %s, %s, %s)'
    UAV_ID = '1'
    conn.cursor().execute(query, (UAV_ID, float(message.latitude), float(message.longitude), datetime.datetime.now()))
    conn.commit()
"""
def callback_with_system_id(message, system_id='1'):
    global conn
    rospy.loginfo(rospy.get_caller_id() + " received: (lat: {0}, lon: {1})".format(message.latitude, message.longitude))
    query = 'INSERT INTO realtime(uav_id, latitude, longitude, timestamp) VALUE(%s, %s, %s, %s)'
    conn.cursor().execute(query, (system_id, float(message.latitude), float(message.longitude), datetime.datetime.now()))
    conn.commit()

def callback_generator(uav_id):
    return lambda message: callback_with_system_id(message, system_id=uav_id)
        

def listener():
    rospy.init_node('position_updater', anonymous=True)
    rospy.Subscriber('mavros1/global_position/global', NavSatFix, callback_generator(uav_id='1'))
    rospy.Subscriber('mavros2/global_position/global', NavSatFix, callback_generator(uav_id='2'))
    rospy.Subscriber('mavros3/global_position/global', NavSatFix, callback_generator(uav_id='3'))
    rospy.spin()


if __name__ == '__main__':
    listener()