#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -b 2 -m H-Cpp 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyH-Cpp.csv &
{ \time -f "%e, %U, %S " ./DM -b 2 -n 648 -m H-Py ; } 2>> ../output/timeCppH-Py.csv

