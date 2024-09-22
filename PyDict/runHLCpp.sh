#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -b 2 -m HL-PyDict 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppHL-PyDict.csv &
{ \time -f "%e, %U, %S " python DMDict.py -b 2 -n 648 -l -m HL-Cpp ; } 2>> ../output/timePyDictHL-Cpp.csv

