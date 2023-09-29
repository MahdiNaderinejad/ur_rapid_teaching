from json_handling import load_json
import rtde_control
from time import sleep
from numpy import deg2rad
import os

class Arm:
    def __init__(self) -> None:
        self.err_id = [1,2,3,4]
        self.err_p_name = ["subtask1_1"]
        err_x = 0 # in mm
        err_y = 0 # in mm
        err_Rz = deg2rad(15)
        self.err_frame = "TCP"


        self.err_val = [0,err_y/1000,err_x/1000,err_Rz,0,0]
        self.paths = load_json("waypoints_paths.json")
        self.UR_Arm_IP = "172.31.0.105"
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
                        if id in self.err_id and p_name in self.err_p_name:
                            error = self.err_val
                        else:
                            error = [0,0,0,0,0,0]

                        if self.err_frame == "base":
                            target_pose = list(sum(i) for i in zip(point["pose"]["TCP"],error))
                        elif self.err_frame == "TCP":
                            print(point["pose"]["TCP"])
                            target_pose = self.rtde_c.poseTrans(point["pose"]["TCP"], error)
                            print(target_pose)
                            
                        self.rtde_c.moveL(point["pose"]["TCP"],playback_v,playback_a)
                        self.rtde_c.moveL(target_pose,playback_v,playback_a)
                        input()

                    else:
                        self.rtde_c.moveJ(point["pose"]["Q"],playback_v*4,playback_a*2)


                    # print(p_name, id)
                    # print(point["pose"]["TCP"])
                    # input()
                

                break