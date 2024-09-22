#!/bin/bash
echo ""
echo -------------------------------------------------------------------------------
echo ""
declare -i loop=1
if (( $# == 1 )); then
  loop=$1
  echo input nr loops: $loop  
fi

echo Benchmarking PyDataclass

for ((i = 1 ; i < $loop+1 ; i++ )); do
  echo "---Loop: $i--- ---runVLPy ---" 
  bash runVLPy.sh 
  echo "---Loop: $i--- ---runVPy ---" 
  bash runVPy.sh 
  echo "---Loop: $i--- ---runHPy ---" 
  bash runHPy.sh
  echo "---Loop: $i--- ---runHLPy ---" 
  bash runHLPy.sh
  echo "---Loop: $i--- ---runVLCpp ---" 
  bash runVLCpp.sh 
  echo "---Loop: $i--- ---runVCpp ---" 
  bash runVCpp.sh 
  echo "---Loop: $i--- ---runHCpp ---" 
  bash runHCpp.sh
  echo "---Loop: $i--- ---runHLCpp ---" 
  bash runHLCpp.sh
done


