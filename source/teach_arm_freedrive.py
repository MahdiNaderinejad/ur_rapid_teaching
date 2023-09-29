

def teach_arm(rtde_r,rtde_c):
    
    rtde_c.teachMode()
    teach_choice = input("Freedrive mode enabled. Put the robot at the desired pose and press Enter. (Press 'q' to exit)")
    rtde_c.endTeachMode()

    TCPPose= rtde_r.getActualTCPPose()
    Qs = rtde_r.getActualQ()
    point_ = {"TCP":TCPPose , "Q":Qs}
    space = "freedrive"

    while True:
        if teach_choice=='':
            return 1
        elif teach_choice=='q' or teach_choice=='Q':
            return -1
        else:
            teach_choice = input("Invalid input! Please press Enter for saving the current position or 'q' to quit.")