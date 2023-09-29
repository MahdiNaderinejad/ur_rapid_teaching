# ur_rapid_teaching
This project is a command-line UI for rapid teaching a Universal Robot e-series (UR) robot arm with a Sony PlayStation 4 Dual Shock gamepad and recording the waypoints for the tasks.

# Arm Teaching
Arm teaching basically means defining waypoints through which the robot is passed when performing a task. Each task contains various waypoints that must be grouped and played-back. Therefore, each teaching activity consists two main steps:
1. Putting the robot in the desired configuration
2. Saving that configuration as a waypoint
In order to satisfy the objective of this project, a command-line user interface is coded such that enables the robot arm operators to rapidly teach the robot to perform in the set of tasks they desire. This interface has the ability of enabling freedrive mode in the robot control surface, moving the robot with a Sony Playstation4 gamepad and recording its configuration in tool and joint space.

## Storage and File Management
Before explaining the teaching user interface, it is essential to have a clear understanding of how this interface records and organizes waypoints. In the directory of this interface, there is a JSON file named waypoints_paths.json. This file includes all the taught waypoints. This interface refers to subtasks as paths in which their corresponding speed, acceleration and waypoints are logged. Each waypoint has these attributes:
* path_name : Obviously the name of the path.
* speed: angular or translation maximum speed that robot must reach while operating the motion between the points of this path.
* acceleration: angular or translation maximum acceleration that robot must reach while operating the motion between the points of this path.
* waypoints: all the waypoints in this path that each has the features below:
* teach_space (tool/joint): The space in which the robot is moved to reach this configuration.
Pose
* TCP: a 6-row vector of {x,y,z,rx,ry,rz} of the TCP relative to the base frame.
* Q: a 6-row vector of {shoulder, arm, elbow, wrist1, wrist2, wrist3} robot’s joints angles.
* is_home: there is a defined home point for the robot. If this value is set to “true”, the interface will later change the pose values of the robot while the home point is changed.

## Loading and installing dependencies
Before cloning the interface repository and using it, the operator must install the devices and libraries.
  * Python packages
    - UR-RTDE
    - Pygame
    - Numpy
     
   * Hardware
     - UR Arm via ethernet to the PC
     - Set an IP for the Arm in its teach pendant and add an IpV4 IP for it in the connection settings in the the PC
     - Sony Playstation4 Dualshock Gamepad via USB to the PC
     - A keyboard connected to the PC

# Running the Program
Just launch the "main_arm_teaching_UI.py".

## UR initialization
### IP Verification
As said, the connection of the arm and PC is set through ethernet. Hence, the initialization of the corresponding interfaces begin with setting an IP for the connection. When the program starts, it shows the pre-defined IP and asks the user to change it if the IP is changed. The mentioned IP is saved in the  UR_Arm_IP.json file.

### Read and Control Interfaces
After IP verification, the program sets up the control and reading interfaces as introduced in the UR-RTDE section.

## Main Menu
When successfully set up, the program shows the main menu. The users can now select whatever they want to operate with the program. The options are as below:
1. Teach a path: Enables the user to teach a path by setting its name, speed, acceleration, and waypoints. Waypoints teaching is explained below.
2. Playback and Move: In order to check and verify the existing waypoints in the paths, the operator can have a point-by-point playback of motions by selecting this option. The movements are done from one point to another after pressing the Enter. The program waits for the users’ response before moving to the next point in a given path.
3. Teach HOME point: The HOME point is the configuration in which the operator wants to begin from, end in, or even pass through when teaching a path. Using this feature, the user is also able to put the robot in a safe pose and leave the work station.
4. Go HOME: Moves the robot to the HOME position. This action is done by moving the TCP linearly from the current pose to the HOME one.
5. Enable freedrive mode: Functions as same as pushing the freedrive button on the teach pendant.
6. Exit

### Waypoint Teaching
When the users are at the teaching step, they should move the robot to their desired pose using the gamepad. They have two spaces as options to teach their waypoints in:
Tool Space: Movements are mapped from the gamepad to the translational and rotational Cartesian coordinates of the TCP with respect to the robot’s base frame.
Joint Space: Movements are mapped from the gamepad to the 6 joint angles of the robot.
They also have the option to move the robot using the freedrive mode and then save the waypoint using the gamepad. Using all the aforementioned methods, they must pay attention to the teaching space in which the program is before pressing the save button. The teach_space of each point is set to the last mode in which the program was before verifying the point to be saved. The gamepad axes and buttons are described in the button below. The table below expresses the coordination of each axis or button to their corresponding degree of freedom of the robot’s TCP or joints.



## Playback
In order to playback the paths consecutively, an object named arm must be defined in a script. Then paths are played-back in the order of recalling them by their names. To play back the process, run this script while the arm is connected.

```
from arm_interface import Arm
arm = Arm()

arm.playback_arm(path1)
arm.playback_arm(path2)
```
