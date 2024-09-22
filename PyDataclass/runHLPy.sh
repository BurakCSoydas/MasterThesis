#!/bin/bash
{ \time -f "%e, %U, %S " python ../Simulation/scenarioStart.py -b 2 -m HL-PyDataclass 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMPyHL-PyDataclass.csv &
{ \time -f "%e, %U, %S " python DMDCls.py -b 2 -n 648 -l -m HL-Py ; } 2>> ../output/timePyDataclassHL-Py.csv

