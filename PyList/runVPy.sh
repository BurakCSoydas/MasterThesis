#!/bin/bash
{ \time -f "%e, %U, %S "  python ../Simulation/scenarioStart.py -v -b 2 -m V-PyList 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyV-PyList.csv &
{ \time -f "%e, %U, %S "  python DMList.py -b 2 -n 648 -m V-Py ; } 2>> ../output/timePyListV-Py.csv
