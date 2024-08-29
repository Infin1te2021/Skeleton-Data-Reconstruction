import numpy as np
import json
import os
import random
import subprocess
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
  connections = []

  for i in config["data"]:
    for key, value in i.items():
      dataset_names.append(key)
      path = os.path.join(root_path, value["path"])
      paths.append(path)
      joint_num.append(value["joint_num"])
      connections.append(value["connection"])

  for path in paths:
    if not os.path.exists(path):
      raise FileNotFoundError(f"Path does not exist: {path}")
  return dataset_names, paths, joint_num, connections

def run_blender_script(blender_path, data_file_path):
  blender_path = blender_path
  blender_script_path = "blender_script.py"

  command = [
    blender_path,
    '--background',
    '--python', blender_script_path,
    '--', data_file_path
  ]

  subprocess.run(command)

def process_skeleton_data(file_sequence):
  total_frames = int(file_sequence[0])
  index = 1
  all_frame_data = []

  for _ in range(total_frames):
    num_skeletons = int(file_sequence[index])
    frame_info = file_sequence[index+1]
    num_frame_joints = int(file_sequence[index+2])

    frame_data = []
    for i in range(num_frame_joints):
      line = file_sequence[index + 3 + i]
      coordinates = list(map(float, line.split()[:3]))
      frame_data.append(coordinates)

    all_frame_data.append(frame_data)

    index += 3 + num_frame_joints

  return all_frame_data

def load_data(num_to_load = 0):
  try:
    config_path, root_path = run_config_path_check()
    dataset_names, paths, joint_num, connections = load_data_path(config_path, root_path)

    all_data = []

    for path in paths:
      skeleton_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.skeleton')]
      all_data.extend(skeleton_files)

    if num_to_load > len(all_data):
      raise ValueError(f"num_to_load is greater than the number of skeleton files in the dataset")
    elif num_to_load == 0:
      selected_files = all_data
    else:
      selected_files = random.sample(all_data, num_to_load)

    processed_data = []

    for file in selected_files:
      with open(file, 'r') as f:
        file_sequence = f.readlines()
        file_data = process_skeleton_data(file_sequence)
        processed_data.append(file_data)

    return processed_data, connections

  except FileNotFoundError as e:
    print(e)
  except ValueError as e:
    print(e)

def plot_frame_3d(joint_coordinates, connections_group):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  x = [coord[0] for coord in joint_coordinates]
  y = [coord[1] for coord in joint_coordinates]
  z = [coord[2] for coord in joint_coordinates]
  
  # Plot in 3D
  ax.scatter(x, y, z, c='r', marker='o')
  
  color_list = ['blue', 'green', 'purple', 'orange', 'black', 'yellow', 'pink', 'brown', 'cyan', 'magenta']

  for color, (part, edges) in zip(color_list[0:(len(connections_group) % len(color_list))], connections_group.items()):
    for connection in edges:
      vertice1, vertice2 = connection
      x_values = [x[vertice1], x[vertice2]]
      y_values = [y[vertice1], y[vertice2]]
      z_values = [z[vertice1], z[vertice2]]
      ax.plot(x_values, y_values, z_values, c=color, label=part)

  # Avoid overlapping labels
  handles, labels = plt.gca().get_legend_handles_labels()
  by_label = dict(zip(labels, handles))
  plt.legend(by_label.values(), by_label.keys())

  # Set labels
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  
  plt.show()
  
def plot_skeleton_data(processed_data, connections, opt_matplot, opt_blender):
  if processed_data:
    if opt_matplot:
        for frame_data in processed_data[0]:
          plot_frame_3d(frame_data, connections[0])
    elif opt_blender:
      import blender_script
      for frame_num, frame_data in enumerate(processed_data[0], start=1):
        blender_script.plot_skeleton_frame_blender(frame_data, connections[0], frame=frame_num)
    else:
      print("No plotting option selected")
  else:
    print("No data to plot")