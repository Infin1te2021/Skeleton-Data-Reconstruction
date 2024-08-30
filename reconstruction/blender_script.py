import bpy
import mathutils
import sys

# def enable_gpus(device_type, use_cpus=False):
#   preferences = bpy.context.preferences
#   cycles_preferences = preferences.addons["cycles"].preferences
#   cuda_devices, opencl_devices = cycles_preferences.get_devices()

#   if device_type == "CUDA":
#     devices = cuda_devices
#   elif device_type == "OPENCL":
#     devices = opencl_devices
#   else:
#       raise RuntimeError("Unsupported device type")

#   activated_gpus = []

#   for device in devices:
#     if device.type == "CPU":
#       device.use = use_cpus
#     else:
#       device.use = True
#       activated_gpus.append(device.name)

#   cycles_preferences.compute_device_type = device_type
#   bpy.context.scene.cycles.device = "GPU"

#   return activated_gpus

def save_blender_file(filepath="rendered.blend"):
  bpy.ops.wm.save_as_mainfile(filepath=filepath)

def clear_scene():
  bpy.ops.object.select_all(action='SELECT')
  # bpy.ops.object.select_by_type(type='MESH')
  bpy.ops.object.delete()

def create_joint(coordinates, frame, radius=0.05):
  bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=coordinates)
  joint = bpy.context.object
  joint.location = coordinates
  joint.keyframe_insert(data_path="location", frame=frame)
  return joint

def create_bone(start, end, frame):
  # Create a cylinder between two points representing a bone
  direction = end - start
  length = direction.length
  bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=length, location=(start + end) / 2)
  bone = bpy.context.object

  # Align bone to point from start to end
  bone.rotation_mode = 'QUATERNION'
  bone.rotation_quaternion = direction.to_track_quat('Z', 'Y')

  # Set keyframes for the bone's location and rotation
  bone.keyframe_insert(data_path="location", frame=frame)
  bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
  
  return bone

def plot_skeleton_frame_blender(frame_data, connections, frame, save_path="rendered.blend"):
  # Enable GPU rendering
  # enable_gpus("CUDA")
  # Clear scene only on the first frame
  if frame == 1:
    clear_scene()
    
  joints = [create_joint(coord, frame) for coord in frame_data]

  for part, edges in connections.items():
    for vertice1, vertice2 in edges:
      start = joints[vertice1].location
      end = joints[vertice2].location
      create_bone(start, end, frame)

  if frame == 1:
    adjust_camera()

  # Save the Blender file after the scene is created and rendered
  save_blender_file(save_path)

def adjust_camera():
  # Set up the camera for a better view of the skeleton
  camera = bpy.data.objects.get("Camera")
  if camera is None:
    bpy.ops.object.camera_add(location=(5, -5, 5))
    camera = bpy.context.object
  camera.location = (5, -5, 5)
  camera.rotation_euler = (mathutils.Euler((1.1, 0, 0.9), 'XYZ'))

  # Set the camera to look at the origin
  camera_constraint = camera.constraints.get("Track To")
  if not camera_constraint:
    camera_constraint = camera.constraints.new(type='TRACK_TO')
    camera_constraint.target = bpy.data.objects.new("Empty", None)
    bpy.context.collection.objects.link(camera_constraint.target)
    camera_constraint.target.location = (0, 0, 0)
    camera_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    camera_constraint.up_axis = 'UP_Y'
  
  # Add a light if not present
  if not any(obj.type == 'LIGHT' for obj in bpy.data.objects):
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))