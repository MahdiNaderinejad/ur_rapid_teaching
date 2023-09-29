from json_handling import load_json
import rtde_control
from time import sleep
from numpy import deg2rad
import os

class Arm:
    def __init__(self) -> None:
        self.paths = load_json("waypoints_paths.json")
        UR_Arm_IP_file = 'logs/UR_Arm_IP.json'
        UR_Arm_IP = load_json(UR_Arm_IP_file)
        UR_Arm_IP = UR_Arm_IP[0]
        self.UR_Arm_IP = UR_Arm_IP["ip"]
        try:
            self.rtde_c = rtde_control.RTDEControlInterface(self.UR_Arm_IP)
            print(f"Connected to the RTDE Control surface on {self.UR_Arm_IP} !!!")
        except:
            print(f"Error while trying to connect to the RTDE Control surface on {self.UR_Arm_IP} !!!")
                
    def playback_arm(self, p_name):
        for p in self.paths:
            if p['path_name'] == p_name:
                playback_v = p["speed"]
                playback_a = p["acceleration"]

                for id,point in enumerate(p["waypoints"],start=1):
                    if point["teach_space"]=="tool":                            
                        self.rtde_c.moveL(point["pose"]["TCP"],playback_v,playback_a)
                    else:
                        self.rtde_c.moveJ(point["pose"]["Q"],playback_v*4,playback_a*2)

                break