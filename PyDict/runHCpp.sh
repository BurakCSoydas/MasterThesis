#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -b 2 -m H-PyDict 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppH-PyDict.csv &
{ \time -f "%e, %U, %S " python DMDict.py -b 2 -n 648 -m H-Cpp ; } 2>> ../output/timePyDictH-Cpp.csv

