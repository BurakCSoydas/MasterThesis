#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -v -b 2 -m V-PyList  1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppV-PyList.csv &
{ \time -f "%e, %U, %S " python DMList.py -b 2 -n 648 -m V-Cpp ; } 2>> ../output/timePyListV-Cpp.csv 
