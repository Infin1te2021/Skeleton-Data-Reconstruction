from flask import Flask
import datetime
import visual as vs
[option_matplot, option_blender] = [False, True]

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
  processed_data, connections = vs.load_data(num_to_load=1)  # Load 1 file for example
  vs.plot_skeleton_data(processed_data, connections, option_matplot, option_blender)