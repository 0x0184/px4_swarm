#include <ros/ros.h>
#include <geometry_msgs/Vector3.h>
#include <sensor_msgs/NavSatFix.h>
#include <math.h>
#include <std_msgs/Bool.h>
#define MissionSize 11



geometry_msgs::Vector3 dir;
sensor_msgs::NavSatFix Missions[MissionSize];
sensor_msgs::NavSatFix CurrentMission;
bool arrived=false;
int MissionNum=0;
ros::Publisher mission_pub;
double MstartTime;
double MTime;


void ReceiveMissionReceived(std_msgs::Bool vel)
{
    arrived=vel.data;

    if(arrived)
    {        
        ROS_INFO("Current Mission : %d",MissionNum);
        if(MissionNum <= MissionSize)
        {
            MissionNum++;            
            ROS_INFO("arrived!! Goto Next WP");
        }        
        else if (MissionNum>MissionSize)
        {
            ROS_INFO("finished");
        }
    }    
}
void InputMission(sensor_msgs::NavSatFix M,int order)
{
    Missions[order]=M;
}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "Mission_Manager");
  ros::NodeHandle n;
  sensor_msgs::NavSatFix tmp;

  double latitudes[MissionSize] = {
      // TODO
  };
  double longitudes[MissionSize] = {
      // TODO
  };
  for (int i = 0; i < MissionSize; i++) {
      tmp.latitude = latitudes[i];
      tmp.longitude = longitudes[i];
      tmp.altitude = 5;
      InputMission(tmp, i);
  }

  ros::Subscriber arr_sub=n.subscribe("/arrived1", 10, ReceiveMissionReceived);
//  mission_pub = n.advertise<sensor_msgs::NavSatFix>("/manual_Mission",10);
  mission_pub = n.advertise<sensor_msgs::NavSatFix>("/target1",10);

  ros::Rate loop_rate(20);
  while(ros::ok()){
      CurrentMission=Missions[MissionNum];
      mission_pub.publish(CurrentMission);
      ros::spinOnce();
      loop_rate.sleep();
  }

  return 0;
}
