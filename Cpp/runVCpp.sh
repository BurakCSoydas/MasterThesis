#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -v -b 2 -m V-Cpp  1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppV-Cpp.csv &
{ \time -f "%e, %U, %S " ./DM -b 2 -n 648 -m V-Cpp ; } 2>> ../output/timeCppV-Cpp.csv 
