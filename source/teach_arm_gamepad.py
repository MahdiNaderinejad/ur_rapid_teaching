import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from menus_handling import clear_screen
import pygame
from numpy import abs, degrees
from time import time,sleep
from misc_functions import print_robot_status, freedrive_enabled


def map_to_range(value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def print_status(space,odd_space):
    clear_screen()
    print(f"Put the robot at the desired pose using the gamepad and press: \nCircle\t\t-> save\nSquare\t\t-> switch to {odd_space} space \nTriangle\t-> teach with freedrive\nCross\t\t-> exit\n")
    print(f"Current Space : {space}")

def teach_arm_gamepad(rtde_r,rtde_c):
    # Initialize Pygame
    pygame.init()

    # Initialize the gamepad
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()

    if joystick_count < 1:
        print("No joystick/gamepad found.")
        pygame.quit()
        return -1,-1

    joystick = pygame.joystick.Joystick(0)
    joystick.init()


    max_speed = 0.1
    print_interval = 0.5
    dQ = [0,0,0,0,0,0]
    last_print_time  = time()

    # Define axis indices for the gamepad
    LEFT_AXIS_X = 0
    LEFT_AXIS_Y = 1
    RIGHT_AXIS_X = 3
    RIGHT_AXIS_Y = 4

    RX_AXIS = 2
    RY_AXIS = 5

    CIRCLE_BUTTON = 1  # Change to the button index for the circle button
    CROSS_BUTTON = 0
    TRIANGLE_BUTTON = 2
    SQUARE_BUTTON = 3

    BUTTON_6 = 6
    BUTTON_7 = 7

    x_speed = 0
    y_speed = 0
    z_speed = 0
    rx_speed = 0
    ry_speed = 0
    rz_speed = 0

    space = "tool"
    odd_space = "joint"

    print_status(space,odd_space)
    
    while True:
        

        for event in pygame.event.get():

            if space == "tool":
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == LEFT_AXIS_X:
                        x_speed = event.value * -max_speed  # Adjust the scaling as needed
                    elif event.axis == LEFT_AXIS_Y:
                        y_speed = event.value * max_speed  # Adjust the scaling as needed
                    elif event.axis == RIGHT_AXIS_Y:
                        z_speed = event.value * -max_speed  # Adjust the scaling as needed
                    elif event.axis == RX_AXIS:
                        rx_speed = map_to_range(event.value,-1,1,0,1) * max_speed  # Adjust the scaling as needed
                    elif event.axis == RY_AXIS:
                        rx_speed = map_to_range(event.value,-1,1,0,1) * -max_speed  # Adjust the scaling as needed

                elif event.type == pygame.JOYHATMOTION:
                    hat_x, hat_y = event.value
                    if hat_x == 1:
                        rz_speed = 0.1  # Increase or decrease as needed
                    elif hat_x == -1:
                        rz_speed = -0.1  # Increase or decrease as needed
                    else:
                        rz_speed = 0  # Reset to 0 when released
                    if hat_y == 1:
                        ry_speed = 0.1  # Increase or decrease as needed
                    elif hat_y == -1:
                        ry_speed = -0.1  # Increase or decrease as needed
                    else:
                        ry_speed = 0  # Reset to 0 when released

                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == TRIANGLE_BUTTON:
                        x_speed = 0
                        y_speed = 0
                        z_speed = 0
                        rx_speed = 0
                        ry_speed = 0
                        rz_speed = 0
                        sleep(1)
                        rtde_c.speedStop(0.5)
                        freedrive_enabled(rtde_c)
                            
                            
                    
                    elif event.button == CIRCLE_BUTTON:
                        x_speed = 0
                        y_speed = 0
                        z_speed = 0
                        rx_speed = 0
                        ry_speed = 0
                        rz_speed = 0
                        
                        TCPPose= rtde_r.getActualTCPPose()
                        Qs = rtde_r.getActualQ()
                        point_ = {"TCP":TCPPose , "Q":Qs}
                        rtde_c.speedStop(0.5)
                        return [point_,space]
                    
                    elif event.button == CROSS_BUTTON:
                        x_speed = 0
                        y_speed = 0
                        z_speed = 0
                        rx_speed = 0
                        ry_speed = 0
                        rz_speed = 0
                        rtde_c.speedStop(0.5)
                        return -1

                    elif event.button == SQUARE_BUTTON:
                        space = "joint"
                        odd_space = "tool"
                        print_status(space,odd_space)


                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == BUTTON_6 or event.button == BUTTON_7:
                        rx_speed = 0  # Reset RX speed to 0 when either button is released

                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == BUTTON_6 and event.button == BUTTON_7:
                        rx_speed = 0  # Reset RX speed to 0 when either button is released

            elif space == "joint":
                    if event.type == pygame.JOYAXISMOTION:
                        if event.axis == LEFT_AXIS_X:
                            dQ[5] = event.value * -max_speed  # Adjust the scaling as needed
                        elif event.axis == LEFT_AXIS_Y:
                            dQ[4] = event.value * max_speed  # Adjust the scaling as needed
                        elif event.axis == RIGHT_AXIS_X:
                            dQ[3] = event.value * -max_speed  # Adjust the scaling as needed
                        elif event.axis == RIGHT_AXIS_Y:
                            dQ[2] = event.value * -max_speed  # Adjust the scaling as needed
                        elif event.axis == RX_AXIS:
                            dQ[1] = map_to_range(event.value,-1,1,0,1) * max_speed  # Adjust the scaling as needed
                        elif event.axis == RY_AXIS:
                            dQ[1] = map_to_range(event.value,-1,1,0,1) * -max_speed  # Adjust the scaling as needed

                    elif event.type == pygame.JOYHATMOTION:
                        hat_x, hat_y = event.value
                        if hat_x == 1:
                            dQ[0] = max_speed  # Increase or decrease as needed
                        elif hat_x == -1:
                            dQ[0] = -max_speed  # Increase or decrease as needed
                        else:
                            dQ[0] = 0  # Reset to 0 when released


                    elif event.type == pygame.JOYBUTTONDOWN:
                        if event.button == TRIANGLE_BUTTON:
                            dQ = [0,0,0,0,0,0]
                            sleep(1)
                            rtde_c.speedStop(0.5)
                            freedrive_enabled(rtde_c)
                                
                                
                        
                        elif event.button == CIRCLE_BUTTON:
                            dQ = [0,0,0,0,0,0]
                            TCPPose= rtde_r.getActualTCPPose()
                            Qs = rtde_r.getActualQ()
                            point_ = {"TCP":TCPPose , "Q":Qs}
                            rtde_c.speedStop(0.5)
                            return [point_,space]
                        
                        elif event.button == CROSS_BUTTON:
                            dQ = [0,0,0,0,0,0]
                            rtde_c.speedStop(0.5)
                            return -1

                        elif event.button == SQUARE_BUTTON:
                            space = "tool"
                            odd_space = "joint"
                            print_status(space,odd_space)


                    elif event.type == pygame.JOYBUTTONUP:
                        if event.button == BUTTON_6 or event.button == BUTTON_7:
                            dQ[1] = 0  # Reset RX speed to 0 when either button is released

                    elif event.type == pygame.JOYBUTTONDOWN:
                        if event.button == BUTTON_6 and event.button == BUTTON_7:
                            dQ[1] = 0  # Reset RX speed to 0 when either button is released


        curr_time  = time()

        if curr_time - last_print_time >= print_interval:
            print_status(space,odd_space)
            print_robot_status(rtde_r)
            last_print_time = curr_time

        # Move the robot's TCP/Joints using RTDE control
        
        speed_vector = [x_speed, y_speed, z_speed, rx_speed , ry_speed, rz_speed]
        for id,s in enumerate(speed_vector):
            if abs(s) <= 0.005 and id<3:
                speed_vector[id] = 0
        for id,s in enumerate(dQ):
            if abs(s) <= 0.05 and id>1:
                dQ[id] = 0
        if space == "tool":
            rtde_c.speedL(speed_vector, 0.35, 0.001)
            sleep(0.1)
            
        elif space == "joint":
            rtde_c.speedJ(dQ, 0.35, 0.001)
            sleep(0.1)
