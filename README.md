# Processing the COMSOL export data
This script is written to process the export of COMSOL Multiphysics data. Currently, the script is only able 
to create graphs for the specified variables at specified time points.

This task appeared due to the need for careful enumeration of input parameters, however, saving each version of the 
model and / or saving graphs for each value is inconvenient. Moreover, it seemed to me very inconvenient to create 
images for each variable each time. Additional processing of the calculated values is also difficult, which is likely 
to be needed in the future. This script is supposed to solve at least part of these problems.

## Getting started
Example of the start:
```bash
./hellocomsol.py -in /home/COMSOL_export/data.txt -o /home/COMSOL_export/ -v U sr fn -t 5 30
```

This yields:
- parsing of `data.txt`;
- making `data_df.csv` for future quick start;
- plots of velocity, shear rate and fibrin concentrations at time points 5s and 30s.

## Output
In output directory ypu will find png plots and csv table.

## Requirements
I've got these versions, maybe other their versions will work.
- python 3.7;
- pandas 0.24.2;
- numpy 1.16.2;
- matplotlib 3.0.3;
- scipy 1.2.1.

## Notice please
### Input file format
Currently it requires COMSOL export with columns:

`time | x | y | velocity | shear rate | thrombin | fibrin | fibrinogen`

and only in that order.

### Time interval
This script is written for 30s calculations with 0.1 step.

### Interpolation issues
Due to the interpolation, vertical stripes appear which are yet to be dealt with.
However, they do not change the overall picture.