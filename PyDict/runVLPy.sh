#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -v -b 2 -m VL-PyDict 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyVL-PyDict.csv &
{ \time -f "%e, %U, %S " python DMDict.py -b 2 -n 648 -l -m VL-Py ; } 2>> ../output/timePyDictVL-Py.csv

