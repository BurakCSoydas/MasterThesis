#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -v -b 2 -m V-PyDict  1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppV-PyDict.csv &
{ \time -f "%e, %U, %S " python DMDict.py -b 2 -n 648 -m V-Cpp ; } 2>> ../output/timePyDictV-Cpp.csv 
