#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import NavSatFix
import pymysql.cursors
import datetime

DATABASE_HOST = 'localhost'
DATABASE_USER = 'root'
DATABASE_PASS = 'PASSWORD_OF_ROOT'
DATABASE_NAME = 'uavdb'

# Connect to the database
"""
conn = pymysql.connect(host=DATABASE_HOST,
                        user=DATABASE_USR,
                        password=DATABASE_PASS,
                        db=DATABASE_NAME,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
"""
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
    rospy.loginfo(rospy.get_caller_id() + " received: (lat: {0}, lon: {1})".format(message.latitude, message.longitude)
    query = 'UPDATE realtime SET Lattitude = %s, Longitude = %s, ReceiveDate = %s WHERE UAV_ID = %s'
    conn.cursor().execute(query, (message.latitude, message.longitude, datetime.datetime.now(), system_id))
    conn.commit()
    print('id: {}, lat={}, lng={}'.format(system_id, message.latitude, message.longitude))

def callback_generator(uav_id):
    return lambda message: callback_with_system_id(message, system_id=uav_id)
        

def listener():
    rospy.init_node('position_updater', anonymous=True)
    # leader id 2
    # follower id 3 4

    # Latitude Longitude GPSAltitude PressureAltitude ReceiveDate roll pitch raw

    rospy.Subscriber('mavros1/global_position/global', NavSatFix, callback_generator(uav_id='2'))
    rospy.Subscriber('mavros2/global_position/global', NavSatFix, callback_generator(uav_id='3'))
    rospy.Subscriber('mavros3/global_position/global', NavSatFix, callback_generator(uav_id='4'))
    rospy.spin()


if __name__ == '__main__':
    listener()