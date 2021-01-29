# Hello, COMSOL

Currently, it is only able to create graphs for the specified variables at specified time points.

This task appeared due to the need for careful enumeration of input parameters, however,
saving each version of the model and / or saving graphs for each value is inconvenient. 
Moreover, it seemed to me very inconvenient to create images for each variable each time. 
Additional processing of the calculated values is also difficult, which is likely to be needed in the future. 
This repo is supposed to solve at least part of these problems.

## Current status

I'm on the stage of the research, so that's why I've reworked _hellocomsol.py_ script. 
I think code will change a lot in the future. Now there is only _run_for_CSV.py_ for making CSV from TXT. 
There is now a library called _hellocomsol_, where you can find functions that I use in Jupyter Notebook.

## Requirements

I've got these versions, maybe other their versions will work.

- python 3.7;
- pandas 0.24.2;
- numpy 1.16.2;
- matplotlib 3.0.3;
- scipy 1.2.1.

## Notice please

### Input file format

Currently, it requires COMSOL export with columns:

`time | x | y | velocity | shear rate | thrombin | fibrin | fibrinogen`

