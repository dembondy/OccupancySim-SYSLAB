# OccupancySim-SYSLAB
House occupancy simulator for SYSLAB. It receives a *setup.csv* file as input and outputs a *all.csv* file, of m x n dimensions, where m is the time length of the required simulation and n is the number of simulated rooms. The occupancy values are binary, 1 representing occupancy and 0 representing vacancy.

## Running the simulator

1. Open the setup.csv file and adjust the desired parameters
2. Run the following command in the terminal:

``` python3 OccupancySimulator.py ```

## Input content

The input csv file defines the following values (order does not matter):

Rooms: a number
MiddleManagers, a number
SeniorManagers, a number
Engineers, a number
AdministrativeStaff, a number
Ts, a string that pandas can parse, e.g. 1min, 5min, H, D
StartDate, a string with a date, e.g. 2016-09-09
EndDate, a string with a date, e.g. 2016-09-12. End date is non-inclusive.


