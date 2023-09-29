import os, source.UR_initialization
from source.json_handling import *
from time import sleep, time
from source.menus_handling import *
import time
import source.teach_arm_gamepad
from source.misc_functions import *



def main():
   # Initializing the robot interfaces
    clear_screen()
    UR_Arm_IP_file = 'config/UR_Arm_IP.json'
    UR_Arm_IP = load_json(UR_Arm_IP_file)
    UR_Arm_IP = UR_Arm_IP[0]
    UR_Arm_IP = UR_Arm_IP["ip"]
    print("The current IPv4 for your UR Arm is "+UR_Arm_IP)
    to_change_ip = input("Press Enter to continue and 'c' to change it.")
    if to_change_ip == 'c' or to_change_ip == "C":
        clear_screen()
        UR_Arm_IP = input("Insert your new IP: ")
        save_to_json(UR_Arm_IP_file, [{"ip":UR_Arm_IP}])

    rtde_r, rtde_c = source.UR_initialization.UR_initializtion(UR_Arm_IP)

   # Loading the .json file including the paths and their waypoints 
    waypoints_path_file = 'config/waypoints_paths.json'
    waypoints_paths = load_json(waypoints_path_file)
    home_rest_position_file = 'config/home_rest_position.json'
    home_rest_position = load_json(home_rest_position_file)
    home_position = home_rest_position[0]
    rest_position = home_rest_position[1]

   # Program main loop 
    while True:

        main_menu_choice = main_menu()

        if main_menu_choice == '1':
            clear_screen()
            new_path_name = input("Insert a name for the new path and press Enter to continue. (Press 'q' to exit.)")
            if new_path_name=='q' or new_path_name=='Q':
                continue
            else:
                clear_screen()
                change_default = input("If you want to keep the default acceleration=0.1 m/s^2 and speed=0.1 m/s press Enter. Otherwise enter 'c'.")
                clear_screen()

                if change_default == 'c' or change_default == 'C':
                    while True:
                        clear_screen()
                        print(f'Adding path {new_path_name}:\n')
                        try:
                            new_path_v = float(input("Insert a speed (in range (0,3] m/s, default=0.1 m/s) for the new path and press Enter to continue."))
                            if new_path_v>0 and new_path_v<=3:
                                while True:
                                    clear_screen()
                                    print(f'Adding path {new_path_name}:\n')
                                    try:
                                        new_path_a = float(input("Insert an acceleration (in range (0,3] m/s^2, default=0.1 m/s^2) for the new path and press Enter to continue."))
                                        if new_path_a>0 and new_path_a<=3:
                                            break
                                        else:
                                            input("Invalid value. Please enter a value in range. Press Enter to try again.")
                                            continue
                                    except:
                                        input("Invalid input. Please enter a float number without any charachters before or after it. Press Enter to try again.")
                                break
                            else:
                                input("Invalid value. Please enter a value in range. Press Enter to try again.")
                                continue
                        except:
                            input("Invalid input. Please enter a float number without any charachters before or after it. Press Enter to try again.")
                else:
                    new_path_v = 0.1
                    new_path_a = 0.1         
                clear_screen()
                new_path = {"path_name": new_path_name, "speed":new_path_v, "acceleration":new_path_a, "waypoints":list()}
                input(print(f"New path ({new_path_name}) generated. Now we should teach the waypoints. Press Enter to continue... "))

                to_quit = False
                while True:
                    while True:
                        clear_screen()
                        points_num = len(new_path["waypoints"])
                        print(f"{points_num+1}. Path {new_path_name} - Teaching point {points_num+1} ...\n")
                        is_it_home = input("Is this the home position? (y/n) or press 'q' to exit. ")
                        if is_it_home == "y" or is_it_home == "Y":
                            print("Robot will home in 2 seconds...")
                            robot_setting(rtde_c,home_position)
                            new_path["waypoints"].append(home_position)
                            break
                        elif is_it_home == "n" or is_it_home == "N":
                            new_point = source.teach_arm_gamepad.teach_arm_gamepad(rtde_r,rtde_c)
                            if new_point != -1:
                                new_point_pose = new_point[0]
                                new_point_teach = new_point[1]
                                new_point = {"teach_space": new_point_teach ,"pose":new_point_pose , "is_home":False}
                                new_path["waypoints"].append(new_point)
                                break
                            else:
                                continue
                        elif is_it_home == "q" or is_it_home == "Q":
                            input(f"You will terminate the path teaching with {points_num} waypoints. Press Enter to continue. ")
                            to_quit = True
                            break
                        else:
                            input('Invalid input. Press Enter to try again...')
                    
                    if to_quit==True:
                        break
                waypoints_paths.append(new_path)
                save_to_json(waypoints_path_file,waypoints_paths)
                

        elif main_menu_choice == '2':
            while True:
                submenu_choice = playback_move_menu()
                
                if submenu_choice == '1':
                    path = paths_menu(waypoints_paths)
                    path = int(path)
                    path = waypoints_paths[path-1]
                    path_name = path["path_name"]
                    for i in range(3):
                        clear_screen()
                        print(f"Playback of path (point-by-point): {path_name} in {3-i} seconds")
                        sleep(1)
                    print(f"Playback of path: {path_name}...")
                    playback_v = path["speed"]
                    playback_a = path["acceleration"]
                    waypoints = path["waypoints"]
                    to_quit = False
                    for id, point in enumerate(waypoints):
                        while True:
                            clear_screen()
                            print(f"Playback of path: {path_name}...")
                            go_next = input(f"Currently at point {id}\nGoing to point {id+1}?\n(Press Enter to continue and 'q' to exit.) ")
                            if go_next=='':
                                if point["teach_space"]=="tool":
                                    rtde_c.moveL(point["pose"]["TCP"],playback_v,playback_a)
                                    sleep(0.1)
                                    break
                                else:
                                    rtde_c.moveJ(point["pose"]["Q"],playback_v,playback_a)
                                    sleep(0.1)
                                    break
                                
                            elif go_next=='q' or go_next=='Q':
                                for i in range(3):
                                    clear_screen()
                                    print(f"Quitting from path:{path_name} in {3-i} seconds")
                                    sleep(1)
                                clear_screen()
                                to_quit = True
                                break
                            else:
                                input("Invalid Input! Press Enter to try again... ")
                                continue
                        
                        if to_quit == True:
                            break

                elif submenu_choice == '0':
                    break

                else:
                    clear_screen()
                    input("Invalid input! Please press Enter and try again...")

        elif main_menu_choice == '3': # Teach HOME point
            clear_screen()
            print("Setting HOME position...")
            point = source.teach_arm_gamepad.teach_arm_gamepad(rtde_r,rtde_c)
            if point != -1:
                change_home_position(point,home_position,rest_position,home_rest_position_file)
                sleep(1)
            else:
                continue          
            

        elif main_menu_choice == '4': # Go HOME
            clear_screen()
            print("Moving to HOME position...")
            robot_setting(rtde_c,home_position)
            sleep(1)
        
        elif main_menu_choice == '5': # Enabling Freedrive Mode
            clear_screen()
            rtde_c.teachMode()
            print_robot_status(rtde_r)
            input("\nThe robot is in the freedrive mode. Press Enter when you are done with it ...")  
            print("Freedrive terminated! The robot is now back to the normal mode.")
            rtde_c.endTeachMode()
            sleep(1)


        elif main_menu_choice == '0': # Exit
            break

        else:
            clear_screen()
            input("Invalid input! Please press Enter and try again...")
    
    rtde_c.stopScript()
    clear_screen()

if __name__ == "__main__":
    main()
