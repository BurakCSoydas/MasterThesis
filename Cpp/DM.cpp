#include "DM.hpp"
#include "Benchmark.hpp"
#include <algorithm>
#include <bits/getopt_core.h>
#include <cmath>
#include <iostream>
#include <iterator>
#include <ostream>
#include <string>
#include <utility>
#include <vector>
/**
 * Initiate Driver Model and setup logging if set to log.
 */
DM::DM(double timestepIn, bool logFlag, std::string ip, std::string DMMode)
    : timestep{timestepIn}, hValue{1.0F, 0.0}, log{logFlag}, udpObj{500, ip} {

  if (log) {
    // during benching we create logs to see its effect on performance.
    // The logs themselves are not useful and to avoid wasted storage
    // they are stored in  "/tmp/", where they get deleted automatically.
    std::string outputPath = "../tmp/";

    // check if output directory exists, and creates it if needed
    mkdir(outputPath.c_str(), 0777);

    // string as header for csv containing the names of the variables logged.
    columns =
        "Timestamp,distance,egoSpeed,vTheta,vThetaDot,Vp,activationChange,"
        "vActivation,bModelIsBreaking,response,vpp,targetlane\n";

    // log stored in *.csv file
    std::string filePath =
        outputPath + "Log-Cpp" + DMMode + getDateTime() + ".csv";
    file.open(filePath, std::ios_base::out);
    file << columns;
  }
}

/**
 * Returns the current datetime in the "-%m%d_%H%M_%S" format. Used for logfile
 * creation.
 */
std::string DM::getDateTime() {
  time_t rawtime;
  struct tm *timeinfo;
  char buffer[80];

  time(&rawtime);
  timeinfo = localtime(&rawtime);
  strftime(buffer, sizeof(buffer), "-%m%d_%H%M_%S", timeinfo);
  std::string str(buffer);
  return str;
}

/**
 * Receives OSI-data, steps the Driver Model and sends a breaking response to
 * brake the ego vehicle if required. Additionally, it initiates full-throttle
 * acceleration of the ego vehicle during the first loop.
 */
void DM::runDM() {

  if (not udpObj.firstGTReceived) {
    return;
  }
  // store values from previous run
  
  // calculate positional data, with the position of the vehciles being position of center plus half of its length
  
  // calculate optical size and looming of target vehicle
  
  // calculate prediction error

  // run accumulator
  
  // if activation value passed
  
    // activate breaking model
  
    // store previous break response
  
    // set up values for linear piece-wise funtions
  

  // if brake model is activated
    // update values via linear piece-wise functions
    
    // calculate brake response

    // calculate brake delay

    // finally, set break response

  // Reset prediction

  // calculate prediction for next cycle
  
  // increase internal counter

  // log driver model parameters
  if (log) // code in comments used for debugging, remove before end
  {
    char buffer[8196];
    memset((char *)&buffer, 0, sizeof(buffer));
    snprintf(buffer, 3000,
             "%.2f,%.5g,%.4g,%.4g,%.4g,%.4g,%.4g,%.4g,%i,%.4g,%.4g,%d\n",
             udpObj.data.timestamp, prevDistEgoToTarget, udpObj.data.egoSpeed,
             vTheta, vThetaDot, vp, activationChange, vActivation,
             bModelIsBraking, responseDM, vpp, udpObj.data.targetLane);
    std::string buff = buffer;
    file << buff;
  }
}

void DM::CalcH(std::pair<float, double> &calch) const {
  // linear piece-wise function
}


void DM::CalcG(double &calcg) const {
// linear piece-wise function
}

/**
 * This function is intended to be run parallely to a simulation using the
 * open-simulation-interface. It acts as the driver model for the ego vehicle in
 * a simulation with one target vehicle. The Driver Model accelerates the ego
 * vehicle to full speed at scenario start and keeps driving in a straight line.
 * It will bring the ego vehicle to a full stop when the target vehicle is in
 * the same lane and a crash woueld occur.
 */
int main(int argc, char **argv) { // initialise input parameters
  bool inputLog = false;
  int BMMode = 0;
  int inputIterations = 700;
  double inputTimestep = 0.01;
  std::string DMMode;
  std::string ip = "127.0.0.1";
  
  // parse arguments
  int c = 0;
  while ((c = getopt(argc, argv, "b:m:n:t:l")) != -1) {
    switch (c) {
    // parse b argument, check value and type before setting set benchmark mode
    case 'b':
      try { // input string to int
        BMMode = std::stoi(optarg);
        // value check
        if (BMMode < 0 or BMMode > 3) {
          std::cout << "Please enter one of the following values to set "
                       "benchmark mode"
                    << std::endl;
          std::cout
              << "0: OFF (DEFAULT, running now)\n\t1:AVG\n\t2:ALL\n\t3:BOTH"
              << std::endl;
        }
      } catch (std::invalid_argument const &ia) {
        std::cout << "Benchmark mode argument is not an integer" << std::endl;
        break;
      }

    // parse l argument and enable logging


    // parse m argument and modify output filename
    case 'm':
      DMMode = optarg;
      break;

    // parse n arguments, check value and type before setting number of
    // iterations
    case 'n':
      try {
        if (std::stoi(optarg) == 0) {
          std::cout
              << "Please enter the number of iterations [INTEGER] bigger than 0"
              << std::endl;
        } else {
          inputIterations = std::stoi(optarg);
        }
        break;
      } catch (std::invalid_argument const &ia) {
        std::cout << "Number of iterations argument not an integer"
                  << std::endl;
        break;
      }

    // parse t argument, check value and type before setting timestep
    case 't':
      try { // input string to double
        double timestep = std::stod(optarg);
        if (timestep == 0.0) {
          std::cout << "Please enter a timestep value [DOUBLE] bigger than 0.0"
                    << std::endl;
        }

        break;
      } catch (std::invalid_argument const &ia) {
        std::cout << "Timestep argument not a double" << std::endl;
        break;
      }
    case 'l':
      inputLog = true;
      break;
        
    }
  }

  // initialise benchmark, set its mode and init DM
  Benchmark benchmark(DMMode);
  benchmark.setMode(static_cast<BenchmarkMode>(BMMode));
  DM dm(inputTimestep, inputLog, ip, DMMode);
  
  for (int i = 0; i < inputIterations; ++i) {
    if (BMMode) {
      benchmark.startTimer();
    }

    dm.runDM();

    if (BMMode) {
      benchmark.stopTimer();
    }

    if (dm.responseDM > 0 and
        dm.udpObj.data.egoLane == dm.udpObj.data.targetLane) {
      dm.udpObj.respondToESMINI(0, dm.responseDM, 0.0, 0.0);
    } else {
      dm.udpObj.respondToESMINI();
    }

    dm.udpObj.receiveOSIGT();
  }

  if (BMMode) {
    benchmark.getResults();
  }
  if (inputLog) {
    dm.closeLog();
  }

  return 0;
}
