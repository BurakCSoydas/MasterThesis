#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -b 2 -m H-PyCls 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyH-PyCls.csv &
{ \time -f "%e, %U, %S " python DMCls.py -b 2 -n 648 -m H-Py ; } 2>> ../output/timePyClassH-Py.csv

