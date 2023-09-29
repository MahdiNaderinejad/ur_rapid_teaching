import os

def clear_screen():
    os.system('clear')

def main_menu():
    clear_screen()

    print("UR10 Teaching Menu:")
    print(" 1. Teach a path")
    print(" 2. Playback and Move")
    print(" 3. Teach HOME point") # done
    print(" 4. Go HOME") # done
    print(" 5. Enable freedrive mode") # done
    print(" 0. Exit\n") # done

    choice = input("Select an option by entering its number: ")
    return choice
    
def modify_menu():
    clear_screen()

    print("View and Modify Points and Paths Menu:") # add view
    print(" 1. Rename a path")
    print(" 2. Modify points in a path")
    print(" 0. Go back\n")

    choice = input("Select an option by entering its number: ")
    return choice

def playback_move_menu():
    clear_screen()

    print("Playback and Move Menu:")
    print(" 1. Playback of a path (point by point)")
    print(" 0. Go back\n")
    
    choice = input("Select an option by entering its number: ")
    return choice

def paths_menu(waypoints_paths):
    clear_screen()
    print("Paths Menu")
    for id, path in enumerate(waypoints_paths,start=1):
        print(f' {id}. {path["path_name"]}')

    print(" 0. Go back\n")
    print(" 999. Main menu\n")
    choice = input("Select a path by entering its number: ")
    return choice

def waypoints_menu(waypoints):
    clear_screen()
    print("Waypoints Menu")
    for id,point in enumerate(waypoints, start=1):
        print(f' {id}. Waypoint {id}')
    print(" 0. Go back\n")
    print(" 999. Main menu\n")
    choice = input("Select a point by entering its number: ")
    return choice

def points_menu(points):
    clear_screen()
    print("Points Menu")
    for num,point in enumerate(points,start=1):
        name_ = point["point_name"]
        id_ = point["point_id"]
        print(f' {num}. {name_} - id: {id_}')
        
    print(" 0. Go back\n")
    print(" 999. Main menu\n")
    choice = input("Select a point by entering its number: ")
    return choice
