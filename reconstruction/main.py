# from flask import Flask
import os
import sys
import argparse
import textwrap

def get_parser():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='''This script loads and plots skeleton data from the NTU-RGBD, Kinetics, or MSCOCO datasets via Matplotlib or Blender.''')

  parser.add_argument('database',
                      metavar="DATABASE",
                      type=str,
                      choices=['NTU-RGB+D-60', 'NTU-RGB+D-120', 'NTU-RGBD-All', 'Kinetics-skeleton', 'MSCOCO2017'],
                      help='Specify the dataset to load. Valid options are: NTU-RGB+D-60, NTU-RGB+D-120, NTU-RGBD-All, Kinetics, MSCOCO2017.')
  
  parser.add_argument('--subset_mask', 
                      metavar='BINARY_ENCODED_SUBSET',
                      type=str,
                      choices=['100', '101', '110', '111', '001', '010', '011'],
                      default=111,
                      help=textwrap.dedent('''\
                      Select dataset subsets using binary encoding. The three positions represent train, validation, and test, respectively.
                      Use 1 to include and 0 to exclude. Default is "111" (include all subsets).
                        '''))
  
  parser.add_argument('plot_option',
                      metavar='PLOT_OPTION',
                      type=str,
                      choices=['matplot', 'blender'],
                      help='Choose the plotting method. Valid options are: matplot, blender.')
  
  parser.add_argument('--num_files', 
                    metavar='NUM_FILES', 
                    type=int, 
                    default=1, 
                    help='Specify the number of files to load. Set to -1 to load all files. Default is 1.')
  
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

  processed_data, connections = vs.load_skeleton_data(database_opt=args.database, subset_mask=args.subset_mask, num_to_load=args.num_files)  # Load 1 file for example
  vs.plot_skeleton_data(processed_data, connections, plot_opt=args.plot_option)
# processed_data, connections = vs.load_skeleton_data(num_to_load = number_to_load)  # Load n file for example
# vs.plot_skeleton_data(processed_data, connections, opt_matplot = plt_opt, option_blender = data_opt)
