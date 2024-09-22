#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -b 2 -m H-PyList 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyH-PyList.csv &
{ \time -f "%e, %U, %S " python DMList.py -b 2 -n 648 -m H-Py ; } 2>> ../output/timePyListH-Py.csv

