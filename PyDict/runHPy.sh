#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -b 2 -m H-PyDict 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyH-PyDict.csv &
{ \time -f "%e, %U, %S " python DMDict.py -b 2 -n 648 -m H-Py ; } 2>> ../output/timePyDictH-Py.csv

