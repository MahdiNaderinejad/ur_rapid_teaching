from numpy import degrees
from json_handling import *
from menus_handling import *

def change_home_position(point,home_position,rest_position,home_position_file):
    msg = "Do you want to change the HOME position to this pose? (y/n)"
    change_home = input(msg)
    while True:
        if change_home == "y" or change_home == "Y":
            home_position['pose'] = point[0]
            home_position['teach_space'] = point[1]
            save_to_json(home_position_file, [home_position,rest_position])
            print("HOME position set successfully!")
            break
        elif change_home == "n" or change_home == "N":
            print("HOME position is not changed!")
            break
        else:
            change_home = input("Sorry! We didn't get you. We try again...\n"+msg)

def change_rest_position(point,home_position,rest_position,home_position_file):
    msg = "Do you want to change the REST position to this pose? (y/n)"
    change_rest = input(msg)
    while True:
        if change_rest == "y" or change_rest == "Y":
            rest_position['pose'] = point[0]
            rest_position['teach_space'] = point[1]
            save_to_json(home_position_file, [home_position,rest_position])
            print("REST position set successfully!")
            break
        elif change_rest == "n" or change_rest == "N":
            print("REST position is not changed!")
            break
        else:
            change_rest = input("Sorry! We didn't get you. We try again...\n"+msg)

def robot_setting(rtde_c,position):
    v = 0.1
    a = 0.1
    rtde_c.moveL(position['pose']['TCP'],v,a)
    point_name = position["point_name"]
    print(f"The robot is currently at {point_name} position!")

def freedrive_enabled(rtde_c):
    
    rtde_c.teachMode()
    input("Freedrive mode enabled. Put the robot at the desired pose and press Enter.")
    rtde_c.endTeachMode()

def print_robot_status(rtde_r):


    print("\n>>>>>>>>>>>>>>>>> UR Logs <<<<<<<<<<<<<<<<<")
    TCPPose= rtde_r.getActualTCPPose()
    Qs = degrees(rtde_r.getActualQ())

    joints_ = ["Base","Shoulder","Elbow","Wrist1","Wrist2","Wrist3"]
    TCP_ = ["X","Y","Z","RX","RY","RZ"]

    print("TCP POSE -> ")
    for i , val in enumerate(TCPPose):
        print(f"\t{TCP_[i]}:\t\t{val:.2f}")


    print("JOINT ANGLES -> ")
    for i , val in enumerate(Qs):
        if i == 1:
            print(f"\t{joints_[i]}:\t{val:.2f}")
        else:
            print(f"\t{joints_[i]}:\t\t{val:.2f}")
    print()