#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -v -b 2 -m VL-Cpp 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyVL-Cpp.csv &
{ \time -f "%e, %U, %S " ./DM -b 2 -n 648 -l -m VL-Py ; } 2>> ../output/timeCppVL-Py.csv
