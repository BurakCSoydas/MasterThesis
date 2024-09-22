#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -v -b 2 -m VL-PyList 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppVL-PyList.csv &
{ \time -f "%e, %U, %S " python DMList.py -b 2 -n 648 -l -m VL-Cpp ; } 2>> ../output/timePyListVL-Cpp.csv
