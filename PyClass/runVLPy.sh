#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -v -b 2 -m VL-PyCls 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyVL-PyCls.csv &
{ \time -f "%e, %U, %S " python DMCls.py -b 2 -n 648 -l -m VL-Py ; } 2>> ../output/timePyClassVL-Py.csv

