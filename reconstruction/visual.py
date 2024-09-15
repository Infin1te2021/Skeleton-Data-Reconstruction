import numpy as np
import json
import os
import random
import subprocess
import importlib

def import_matplotlib():
  global plt, FuncAnimation
  plt = importlib.import_module('matplotlib.pyplot')  # Correctly import the pyplot submodule
  FuncAnimation = importlib.import_module('matplotlib.animation').FuncAnimation

def import_blender():
  global bpy, mathutils
  bpy = importlib.import_module('bpy')
  mathutils = importlib.import_module('mathutils')

# Check the current path and load the config file path
def get_config_and_root_path():
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
def load_data_from_config(config_path, root_path):
  with open(config_path) as f:
    config = json.load(f)
  
  dataset_names = []
  paths = [] # Might need to delete (substitude) in the future
  joint_num = []
  connections = []
  
  # ntu_paths = []
  # mscoco_paths = []
  # other_paths = []

  for data_entry in config["data"]:
    for key, value in data_entry.items():
      dataset_names.append(key)
      path = os.path.join(root_path, value["path"])
      paths.append(path) # To be delete
      joint_num.append(value["joint_num"])
      connections.append(value["connection"])

      # if "NTU" in key:
      #   ntu_paths.append(path)
      #   connections.append(value["connection"])  # NTU-specific connection structure
      # elif "MSCOCO" in key:
      #   mscoco_paths.append(path)
      #   connections.append(value["connection"])  # MSCOCO-specific connection structure
      # else:
      #   other_paths.append(path)
      #   connections.append(value["connection"])

  blender_path = config["render"][1]["blender"]["path"]

  for path in paths:
    if not os.path.exists(path):
      raise FileNotFoundError(f"Path does not exist: {path}")
  return dataset_names, paths, joint_num, connections, blender_path

  # for path in ntu_paths + mscoco_paths + other_paths:
  #   if not os.path.exists(path):
  #     raise FileNotFoundError(f"Path does not exist: {path}")
  # return ntu_paths, mscoco_paths, other_paths, joint_num, connections, blender_path

# def execute_blender_script(blender_path, blend_file_path='./reconstruction/output/untitled.blend', script_path='./reconstruction/main.py'):
#   command = [
#     blender_path,
#     # blend_file_path,
#     '--background',
#     '--python', script_path
#     #'--', data_file_path
#   ]
#   print(command)
#   subprocess.run(command, check=True)

def parse_skeleton_data(file_sequence):
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

def load_skeleton_data(database_opt, subset_mask = '111', num_to_load = 0):
  try:
    config_path, root_path = get_config_and_root_path()
    dataset_names, paths, joint_num, connections, blender_path = load_data_from_config(config_path, root_path)
    # ntu_paths, mscoco_paths, other_paths, joint_num, connections, blender_path = load_data_from_config(config_path, root_path)

    all_data = []
    # ntu_data = []
    # mscoco_data = []
    # other_data = []

    if database_opt in dataset_names:
      print(f"Loading data from {database_opt} dataset")
      path2load = [paths[dataset_names.index(database_opt)]] # Make sure the paths are in a list
      if os.path.isdir(os.path.join(path2load[0], "train")) or \
        os.path.isdir(os.path.join(path2load[0], "val")) or \
        os.path.isdir(os.path.join(path2load[0], "test")):
        if subset_mask[0] == '1' and os.path.isdir(os.path.join(path2load[0], "train")):
          path2load.append(os.path.join(path2load[0], "train"))
        if subset_mask[1] == '1' and os.path.isdir(os.path.join(path2load[0], "val")):
          path2load.append(os.path.join(path2load[0], "val"))
        if subset_mask[2] == '1' and os.path.isdir(os.path.join(path2load[0], "test")):
          path2load.append(os.path.join(path2load[0], "test"))
        print(f"Paths to load based on subset mask {subset_mask}: {path2load}")
      elif database_opt == "NTU-RGB+D-All":
        print(f"Loading data from all NTU-RGB+D datasets")
        path2load = [paths[dataset_names.index("NTU-RGB+D-60")], paths[dataset_names.index("NTU-RGB+D-120")]]
      else:
        print(f"Load skeleton data from {database_opt} dataset directly")
    else:
      print(f"Database option not found in the config file")
      return None
    
    for subpath in path2load:
      if not os.path.exists(subpath):
        print(f"Subpath {subpath} does not exist.")
        continue  # Skip to the next path

      skeleton_files = [os.path.join(subpath, f) for f in os.listdir(subpath) if f.endswith('.skeleton') or f.endswith('.json')]
      if not skeleton_files:
        print(f"No skeleton files found in {subpath}.")
        continue

      all_data.extend(skeleton_files)
    
    # for path in ntu_paths:
    #   skeleton_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.skeleton')]
    #   ntu_data.extend(skeleton_files)

    # for path in mscoco_paths:
    #   skeleton_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    #   mscoco_data.extend(skeleton_files)

    # for path in mscoco_paths:
    #   skeleton_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')] ## Depends on the file format
    #   mscoco_data.extend(skeleton_files)

    # all_data = ntu_data + mscoco_data + other_data
    
    if num_to_load > len(all_data):
    # if num_to_load > len(ntu_data + mscoco_data + other_data):
      raise ValueError(f"num_to_load is greater than the number of skeleton files in the dataset")
    elif num_to_load == 0:
      selected_files = all_data
    else:
      selected_files = random.sample(all_data, num_to_load)

    processed_data = []
    for file in selected_files:
      with open(file, 'r') as f:
        file_sequence = f.readlines()
        file_data = parse_skeleton_data(file_sequence)
        processed_data.append(file_data)

    return processed_data, connections

  except FileNotFoundError as e:
    print(e)
  except ValueError as e:
    print(e)

def plot_frame_3d_animation(joint_coordinates_list, connections_group, padding=0.1):
  import_matplotlib()
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  # Calculate min and max for each axis with padding
  all_coords = np.array([coord for frame in joint_coordinates_list for coord in frame])
  x_min, y_min, z_min = all_coords.min(axis=0) - padding
  x_max, y_max, z_max = all_coords.max(axis=0) + padding

  ax.set_xlim(x_min, x_max)
  ax.set_ylim(y_min, y_max)
  ax.set_zlim(z_min, z_max)
  
  color_list = ['blue', 'green', 'purple', 'orange', 'black', 'yellow', 'pink', 'brown', 'cyan', 'magenta']
  color_cycle = color_list[:len(connections_group[0]) % len(color_list)]
  
  # Initialize the plot elements (scatter points and lines)
  scatter = ax.scatter([], [], [], c='r', marker='o')

  # Dictionary to hold line plots for each connection group
  line_plots = {part: [] for part in connections_group[0].keys()}

  # Assign colors to each part based on the color cycle
  part_colors = {part: color for part, color in zip(connections_group[0].keys(), color_cycle)}
  
  for part, edges in connections_group[0].items():
    for vertice1, vertice2 in edges:
      line, = ax.plot([], [], [], c=part_colors[part], label=part)
      line_plots[part].append(line)

  # Avoid overlapping labels
  handles, labels = plt.gca().get_legend_handles_labels()
  by_label = dict(zip(labels, handles))
  plt.legend(by_label.values(), by_label.keys())

  # Set labels
  ax.set_xlabel('X (Forward)')
  ax.set_ylabel('Y (Lateral)')
  ax.set_zlabel('Z (Up)')

  # Set the view to match the human body coordinate system
  ax.view_init(elev=125, azim=-90)  # Adjust the elevation and azimuth

  def init():
    # Initialize scatter plot
    scatter._offsets3d = ([], [], [])
    # Initialize line plots
    for lines in line_plots.values():
      for line in lines:
        line.set_data([], [])
        line.set_3d_properties([])
    return [scatter] + [line for lines in line_plots.values() for line in lines]

  def update(frame):
    joint_coordinates = joint_coordinates_list[frame]

    x = [coord[0] for coord in joint_coordinates]
    y = [coord[1] for coord in joint_coordinates]
    z = [coord[2] for coord in joint_coordinates]

    # Update scatter plot
    scatter._offsets3d = (x, y, z)

      # Update line plots
    for part, edges in connections_group[0].items():
      for line, (vertice1, vertice2) in zip(line_plots[part], edges):
        line.set_data([x[vertice1], x[vertice2]], [y[vertice1], y[vertice2]])
        line.set_3d_properties([z[vertice1], z[vertice2]])

    return [scatter] + [line for lines in line_plots.values() for line in lines]

  # Create animation
  anim = FuncAnimation(fig, update, frames=len(joint_coordinates_list), init_func=init, blit=True, repeat=True)
  # anim.save(filename="gif_example.gif", writer="pillow")
  plt.show()

def blender_frame_3d_animation():
  import_blender()
  def clear_scene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='ARMATURE')
    bpy.ops.object.delete()

def plot_skeleton_data(processed_data, connections, plot_opt):
# def plot_skeleton_data(ntu_processed_data, mscoco_processed_data, connections, plot_option, data_option):
  if processed_data:
    if plot_opt == "matplot":
      for frame_data in processed_data:
        plot_frame_3d_animation(frame_data, connections, padding=0.1)
    elif plot_opt == "blender":
      pass
  # if data_option[0]:
    # if plot_option[0]:
    #   for frame_data in ntu_processed_data:
    #     plot_frame_3d_animation(frame_data, connections, padding=0.1)
    # elif plot_option[1]:
    #   pass
      # clear_scene()
      # Check if any object exists before creating an armature
      # if len(bpy.data.objects) == 0:
        #armature = create_armature(processed_data, connections)
        #for bone in armature.data.bones:
        #  print(f"Bone: {bone.name}, Parent: {bone.parent.name if bone.parent else None}")
        # Animate skeleton with connections
        # animate_skeleton(armature, processed_data, connections)
        # save_blender_file()
      # else:
      #   print("Blender scene is not empty, unable to proceed.")
    else:
      print("No plotting option selected")
  # elif data_option[1]:
  #   if plot_option[0]:
  #     for frame_data in mscoco_processed_data:
  #       pass
  #       # plot_frame_2d(frame_data, connections, padding=0.1)
  else:
    print("No data to plot")