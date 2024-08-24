import numpy as np
import json
import os

# 1-sacrum, 2-middle of the spine, 3-neck, 4-head, 5-left shoulder 
# 6-left elbow, 7-left wrist, 8left hand, 9-right shoulder, 10-right elbow 
# 11-right wrist, 12right hand, 13-left hip, 14-left knee, 15-left ankle 
# 16-left foot, 17right hip, 18-right knee, 19-right ankle, 20-right foot 
# 21-spine, 22-tip of the left hand, 23-left thumb, 24-tip of the right hand, 25-right thumb

# Check the current path and load the config file path
def run_config_path_check():
  # Check if the current path is the root of the config file which requires to load the data path later
  current_path = os.getcwd()

  # If the running path is the root of the project 'NTU-DATA-RECONSTRUCTION', then add the config file path else use the current path
  if current_path.endswith("Reconstruction"):
    root_path = os.path.join(current_path, "reconstruction")
  else:
    root_path = current_path
  
  # Load the config file path
  config_path = os.path.join(root_path, "config.json")
  return config_path, root_path


# Load the data path from the config file and check if the path exists
def load_data_path(config_path, root_path):
  with open(config_path) as f:
    config = json.load(f)
  
  dataset_names = []
  paths = []
  joint_num = []

  for i in config["data"]:
    for key, value in i.items():
      dataset_names.append(key)
      path = os.path.join(root_path, value["path"])
      paths.append(path)
      joint_num.append(value["joint_num"])

  for path in paths:
    if not os.path.exists(path):
      raise FileNotFoundError(f"Path does not exist: {path}")
  
  return dataset_names, paths, joint_num


try:
  config_path, root_path = run_config_path_check()
  dataset_names, paths, joint_num = load_data_path(config_path, root_path)
except FileNotFoundError as e:
  print(e)
