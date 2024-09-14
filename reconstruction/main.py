# from flask import Flask
import os
import sys
import argparse

def get_parser():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='''This script loads and plots skeleton data from the NTU-RGBD, Kinetics, or MSCOCO datasets via Matplotlib or Blender.''')

  parser.add_argument('database', metavar="database", type=str, help='''The database to load. Options are: NTU-RGB+D-60, NTU-RGB+D-120, NTU-RGBD-All, Kinetics, MSCOCO2017 ''')
  parser.add_argument('plot', metavar='plot option', type=str, help='''Choose the plot option. Options are: matplot, blender''')
  parser.add_argument('--num', metavar='num to load', type=int, default=1, help='''The number of files to load. Plot all if the number is -1. Default is 1.''')

  return parser

# Set the working directory to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)  # Add the script directory to the Python path
os.chdir(script_dir)  # Change working directory
import visual as vs

# Load and plot the data
if __name__ == "__main__":
  parser = get_parser()
  args = parser.parse_args()

  processed_data, connections = vs.load_skeleton_data(database_opt=args.database, num_to_load=args.num)  # Load 1 file for example
  vs.plot_skeleton_data(processed_data, connections, plot_opt=args.plot)
# processed_data, connections = vs.load_skeleton_data(num_to_load = number_to_load)  # Load n file for example
# vs.plot_skeleton_data(processed_data, connections, opt_matplot = plt_opt, option_blender = data_opt)
