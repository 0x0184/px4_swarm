#!/usr/bin/python
import rospy
from std_msgs.msg import Float64

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
    rospy.loginfo("[heading_watcher] ID: {0}, degree: {1}".format(system_id, message.data))
    query = 'UPDATE realtime SET heading = %s, ReceiveDate = %s WHERE UAV_ID = %s'
    conn.cursor().execute(query, (message.data, datetime.now(), system_id))
    conn.commit()

def callback_generator(uav_id):
    return lambda message: callback_with_system_id(message, system_id=uav_id)

def listener():
    rospy.init_node('heading_watcher', anonymous=True)

    for i in xrange(1, 4):
        rospy.Subscriber('mavros{}/global_position/compass_hdg'.format(i), Float64, callback_generator(uav_id=i+1))
    rospy.spin()


if __name__ == '__main__':
    listener()