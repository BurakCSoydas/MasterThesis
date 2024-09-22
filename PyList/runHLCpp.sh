#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -b 2 -m HL-PyList 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppHL-PyList.csv &
{ \time -f "%e, %U, %S " python DMList.py -b 2 -n 648 -l -m HL-Cpp ; } 2>> ../output/timePyListHL-Cpp.csv

