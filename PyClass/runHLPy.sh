#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -b 2 -m HL-PyCls 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyHL-PyCls.csv &
{ \time -f "%e, %U, %S " python DMCls.py -b 2 -n 648 -l -m HL-Py ; } 2>> ../output/timePyClassHL-Py.csv

