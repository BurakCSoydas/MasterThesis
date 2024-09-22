#!/bin/bash
{ \time -f "%e, %U, %S " ../Simulation/scenarioStart -b 2 -m HL-Cpp 1>/dev/null ; }  2>&1 | cut -d"y" -f2 >> ../output/timeEMCppHL-Cpp.csv &
{ \time -f "%e, %U, %S " ./DM -b 2 -n 648 -l -m HL-Cpp ; } 2>> ../output/timeCppHL-Cpp.csv

