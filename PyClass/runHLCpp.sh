#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -b 2 -m HL-PyCls 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppHL-PyCls.csv &
{ \time -f "%e, %U, %S " python DMCls.py -b 2 -n 648 -l -m HL-Cpp ; } 2>> ../output/timePyClassHL-Cpp.csv

