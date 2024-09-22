#!/bin/bash
{ \time -f "%e, %U, %S "  python ../Simulation/scenarioStart.py -v -b 2 -m V-PyDataclass 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyV-PyDataclass.csv &
{ \time -f "%e, %U, %S "  python DMDCls.py -b 2 -n 648 -m V-Py ; } 2>> ../output/timePyDataclassV-Py.csv
