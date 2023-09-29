import json

# Load UR-RTDE paths and posture points from a JSON file
def load_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Save UR-RTDE posture points to a JSON file
def save_to_json(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Add a new point to a path
def add_point_to_path(path, pose, speed, acceleration):
    new_point = {
        "pose": pose,
        "speed": speed,
        "acceleration": acceleration
    }
    path.append(new_point)

# Delete a point from a path
def delete_point_from_path(path, index):
    if 0 <= index < len(path):
        del path[index]
        print("Point deleted successfully.")
    else:
        print("Invalid point index.")

# Reorder points within a path
def reorder_points_in_path(path, from_index, to_index):
    if 0 <= from_index < len(path) and 0 <= to_index < len(path):
        path.insert(to_index, path.pop(from_index))
        print("Points reordered successfully.")
    else:
        print("Invalid point index.")