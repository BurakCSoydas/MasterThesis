#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -v -b 2 -m V-PyCls  1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppV-PyCls.csv &
{ \time -f "%e, %U, %S " python DMCls.py -b 2 -n 648 -m V-Cpp ; } 2>> ../output/timePyClassV-Cpp.csv 
