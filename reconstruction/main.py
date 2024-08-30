# from flask import Flask
import os
import sys
import datetime

[option_matplot, option_blender] = [False, True]

# Set the working directory to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)  # Add the script directory to the Python path
os.chdir(script_dir)  # Change working directory
import visual as vs
# x = datetime.datetime.now()

# Initializing flask app
# app = Flask(__name__)

# Route for seeing a data
# @app.route('/data')
# def get_time():
  # Returning an api for showing in  reactjs
#  return {
#    'Name':"geek", 
#    "Age":"22",
#    "Date":x, 
#    "programming":"python"
#    }

# Load and plot the data
if __name__ == "__main__":
  processed_data, connections = vs.load_skeleton_data(num_to_load=1)  # Load 1 file for example
  vs.plot_skeleton_data(processed_data, connections, option_matplot, option_blender)