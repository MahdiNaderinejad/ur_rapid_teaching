def UR_initializtion(UR_Arm_IP):
    
    import rtde_control, rtde_receive, os
    from time import sleep
    os.system('clear')

    try:
        rtde_r = rtde_receive.RTDEReceiveInterface(UR_Arm_IP)
        print("Successfully set up RTDE recieve interface.")
        try:
            input("Put the robot in the REMOTE CONTROL mode and press Enter.")
            rtde_c = rtde_control.RTDEControlInterface(UR_Arm_IP)
            print("Successfully set up RTDE control interface.")
            print("All set up! Launching the command-line UI in 3 seconds ...")
            sleep(3)
            os.system('clear')
            return rtde_r, rtde_c
        except Exception as e:
            print("Error: An error occurred while setting up the RTDE control interface.")
            print(e)
    except Exception as e:
        print("Error: An error occurred while setting up the RTDE recieve interface.")
        print(e)

