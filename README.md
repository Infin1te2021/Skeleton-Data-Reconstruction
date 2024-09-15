# Skeleton Data Reconstruction

This is a side project, which is designed to facilitate the visualization of human skeletal data for the purposes of observation and analysis.

The skeletal data was obtained from the `NTU RGB+D` dataset, which is available for download on [Github](https://github.com/shahroudy/NTURGB-D). Additional sources will be added in the future if necessary. The joint information is presented in the following figure. It is highly recommended to refer to the [original paper](https://ieeexplore.ieee.org/document/7780484) and the [website](https://rose1.ntu.edu.sg/dataset/actionRecognition/) for more details.

![human_joint](./fig/humanbody.svg)

Cite from [NTU RGB+D: A Large Scale Dataset for 3D Human Activity Analysis](https://ieeexplore.ieee.org/document/7780484)

## Method

Matplotlib and Blener are the two main approaches to reconstruct the skeleton data.

## Usage

```text
usage: main.py [-h] [--subset_mask BINARY_ENCODED_SUBSET] [--num_files NUM_FILES] DATABASE PLOT_OPTION

This script loads and plots skeleton data from the NTU-RGBD, Kinetics, or MSCOCO datasets via Matplotlib or Blender.

positional arguments:
  DATABASE              Specify the dataset to load. Valid options are: NTU-RGB+D-60, NTU-RGB+D-120, NTU-RGBD-All, Kinetics-skeleton, MSCOCO2017.
  PLOT_OPTION           Choose the plotting method. Valid options are: matplot, blender.

options:
  -h, --help            show this help message and exit
  --subset_mask BINARY_ENCODED_SUBSET
                        Select dataset subsets using binary encoding. The three positions represent train, validation, and test, respectively.
                        Use 1 to include and 0 to exclude. Default is "111" (include all subsets).
  --num_files NUM_FILES
                        Specify the number of files to load. Set to -1 to load all files. Default is 1.
```

Example:

```bash
python3 main.py NTU-RGB+D-All matplot --num_files=2
```

```bash
## To be added soon ...
python3 main.py Kinetics-skeleton --subset_mask=110 matplot --num_files=2 
```

### Matplotlib

The torso may be labeled incorrectly, but this does not affect.
![gif_example](./fig/gif_example.gif)
