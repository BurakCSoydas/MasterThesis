#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -b 2 -m H-Cpp 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppH-Cpp.csv &
{ \time -f "%e, %U, %S " ./DM -b 2 -n 648 -m H-Cpp ; } 2>> ../output/timeCppH-Cpp.csv

