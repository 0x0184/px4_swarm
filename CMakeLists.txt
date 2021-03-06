cmake_minimum_required(VERSION 2.8.3)
project(px4_swarm)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)



catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_library(Vector3_library
   src/FormationFlight/SVector3.h
   src/FormationFlight/SVector3.cpp
)



add_executable(manual_controll src/manual_controll.cpp)
target_link_libraries(manual_controll ${catkin_LIBRARIES} Vector3_library)


add_executable(formation_flight src/FormationFlight/formation_flight.cpp)
target_link_libraries(formation_flight ${catkin_LIBRARIES} Vector3_library)
add_executable(gps_controller1 src/FormationFlight/gps_controller1.cpp)
target_link_libraries(gps_controller1 ${catkin_LIBRARIES} Vector3_library)
add_executable(gps_controller2 src/FormationFlight/gps_controller2.cpp)
target_link_libraries(gps_controller2 ${catkin_LIBRARIES} Vector3_library)
add_executable(gps_controller3 src/FormationFlight/gps_controller3.cpp)
target_link_libraries(gps_controller3 ${catkin_LIBRARIES} Vector3_library)
add_executable(gps_setpoint_flight1 src/FormationFlight/gps_setpoint_flight1.cpp)
target_link_libraries(gps_setpoint_flight1 ${catkin_LIBRARIES} Vector3_library)
add_executable(gps_setpoint_flight2 src/FormationFlight/gps_setpoint_flight2.cpp)
target_link_libraries(gps_setpoint_flight2 ${catkin_LIBRARIES} Vector3_library)
add_executable(gps_setpoint_flight3 src/FormationFlight/gps_setpoint_flight3.cpp)
target_link_libraries(gps_setpoint_flight3 ${catkin_LIBRARIES} Vector3_library)
add_executable(Mission_Manager src/FormationFlight/Mission_Manager.cpp)
target_link_libraries(Mission_Manager ${catkin_LIBRARIES} Vector3_library)
add_executable(Mission_start src/FormationFlight/Mission_start.cpp)
target_link_libraries(Mission_start ${catkin_LIBRARIES} Vector3_library)

add_executable(flocking src/FormationFlight/flocking.cpp)
target_link_libraries(flocking ${catkin_LIBRARIES} Vector3_library)
add_executable(flocking_formation src/FormationFlight/flocking_formation.cpp)
target_link_libraries(flocking_formation ${catkin_LIBRARIES} Vector3_library)



add_executable(keyboard_controller src/keyboard_controller.cpp)
target_link_libraries(keyboard_controller ${catkin_LIBRARIES})
