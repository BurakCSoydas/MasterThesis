#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -v -b 2 -m VL-PyCls 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppVL-PyCls.csv &
{ \time -f "%e, %U, %S " python DMCls.py -b 2 -n 648 -l -m VL-Cpp ; } 2>> ../output/timePyClassVL-Cpp.csv
