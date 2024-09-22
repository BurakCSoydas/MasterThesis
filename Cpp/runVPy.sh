#!/bin/bash
{ \time -f "%e, %U, %S "  python ../Simulation/scenarioStart.py -v -b 2 -m V-Cpp 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyV-Cpp.csv &
{ \time -f "%e, %U, %S "  ./DM -b 2 -n 648 -m V-Py ; } 2>> ../output/timeCppV-Py.csv
