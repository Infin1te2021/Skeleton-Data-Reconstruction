# Skeleton Data Reconstruction

This is a side project, which is designed to facilitate the visualization of human skeletal data for the purposes of observation and analysis.

The skeletal data was obtained from the `NTU RGB+D` dataset, which is available for download on [Github](https://github.com/shahroudy/NTURGB-D). Additional sources will be added in the future if necessary. The joint information is presented in the following figure. It is highly recommended to refer to the [original paper](https://ieeexplore.ieee.org/document/7780484) and the [website](https://rose1.ntu.edu.sg/dataset/actionRecognition/) for more details.

![human_joint](./fig/humanbody.svg)

Cite from [NTU RGB+D: A Large Scale Dataset for 3D Human Activity Analysis](https://ieeexplore.ieee.org/document/7780484)

## Method

Matplotlib and Blener are the two main approaches to reconstruct the skeleton data.

## Usage

```text
usage: main.py [-h] [--num num to load] database plot option

This script loads and plots skeleton data from the NTU-RGBD, Kinetics, or MSCOCO datasets via Matplotlib or Blender.

positional arguments:
  database           The database to load. Options are: NTU-RGB+D-60, NTU-RGB+D-120, NTU-RGBD-All, Kinetics, MSCOCO2017 
  plot option        Choose the plot option. Options are: matplot, blender

options:
  -h, --help         show this help message and exit
  --num num to load  The number of files to load. Plot all if the number is -1. Default is 1.
```

Example:

```bash
python3 main.py NTU-RGB+D-All matplot --num=2
```

### Matplotlib

The torso may be labeled incorrectly, but this does not affect.
![gif_example](./fig/gif_example.gif)
