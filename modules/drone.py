import pymavlink
from pymavlink import mavutil   

class Drone:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.mavlink_connection = pymavlink.mavutil.mavlink_connection(connection_string)
        self.mavlink_connection.wait_heartbeat()
        print("Connected to drone and received heartbeat.")
        
    def arm(self):
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,  # confirmation
            1,  # arm
            0, 0, 0, 0, 0, 0
        )
        
    def takeoff(self, altitude):
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,  # confirmation
            0, 0, 0, 0, 0, 0, altitude
        )
        
    def land(self):
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        
    def rtl(self):
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
    
    def set_speed(self, vx, vy, vz):
        self.mavlink_connection.mav.set_position_target_local_ned_send(
            int(self.mavlink_connection.time_since("SYSTEM_TIME")),
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
            0b110111000111,
            0, 0, 0,
            vx, vy, vz,
            0, 0, 0,
            0, 0)
        
    def set_yaw_rate(self, yaw_rate):
        self.mavlink_connection.mav.set_position_target_local_ned_send(
            int(self.mavlink_connection.time_since("SYSTEM_TIME")),
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
            0b010111000111,
            0, 0, 0,
            0, 0, 0,
            0, 0, 0,
            0, yaw_rate,
        )
        
    def set_speed_and_yaw_rate(self, vx, vy, vz, yaw_rate):
        self.mavlink_connection.mav.set_position_target_local_ned_send(
            int(self.mavlink_connection.time_since("SYSTEM_TIME")),
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
            0b010111000111,
            0, 0, 0,
            vx, vy, vz,
            0, 0, 0,
            0, yaw_rate
        )
        