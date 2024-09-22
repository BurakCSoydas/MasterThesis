#include "Benchmark.hpp"
#include "esminiLib.hpp"
#include "osi_common.pb.h"
#include "osi_groundtruth.pb.h"
#include "osi_object.pb.h"
#include "osi_version.pb.h"
#include <bits/getopt_core.h>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <getopt.h>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

/**
 * Used to split a string preparing the arguments for the Simulation
 * Library.
 */
std::vector<std::string> SplitString(const std::string &s, char separator) {
  std::vector<std::string> output;
  std::string::size_type prev_pos = 0, pos = 0;

  while ((pos = s.find(separator, pos)) != std::string::npos) {
    std::string substring(s.substr(prev_pos, pos - prev_pos));
    output.push_back(substring);
    prev_pos = ++pos;
  }
  output.push_back(s.substr(prev_pos, pos - prev_pos)); // Last word

  return output;
}

int main(int argc, char **argv) {
  // instantiate variable used for args
  int inputBench = 0;
  std::string oscPath = "../resources/xosc/thesis.xosc";
  std::string visualArg = " --headless";
  float timeStep = 0.01;
  bool bench = false;
  // used to set ip to local ip
  const char ip[]("127.0.0.1");
  int BMMode = 0;
  std::string modifier = "";


  // parsing command line arguments to set benchmarking, toggle video output
  // as well as changing XOSC file and time-step. The arguments will be consumed
  // and the arguments leftover are used for setting ESMINI parameters
  int c = 0;
  while ((c = getopt(argc, argv, "b:m:o:vt:")) != -1) {
    switch (c) {
    // parse b argument, check value and type before setting benchmark mode
    case 'b':
      try {
        inputBench = std::stoi(optarg);
        if (inputBench < 0 or inputBench > 3) {
          std::cout << "Please enter one of the following values to set "
                       "benchmark mode"
                    << std::endl;
          std::cout
              << "0: OFF (DEFAULT, running now)\n\t1:AVG\n\t2:ALL\n\t3:BOTH"
              << std::endl;
        } else {
          BMMode = inputBench;
          bench = true;
        }      

      } catch (std::invalid_argument const &ia) {
        std::cout << "Benchmark mode argument is not an integer" << std::endl;
        break;
      }

    // parse m argument and modify output filename
    case 'm':
      modifier = optarg;
      break;

    // parsing o argument, used to change the scenario to a different .OSC file.
    case 'o':
      oscPath = optarg;
      break;

    // parse t argument for time-step, check the value and type before setting
    // it.
    case 't':
      try {
        if (std::stof(optarg) == 0.0) {
          std::cout << "Please enter a time-step value bigger than 0.0"
                    << std::endl;
        } else {
          timeStep = std::stof(optarg);
        }
        break;
      } catch (std::invalid_argument const &ex) {
        std::cout << "Time-step argument not a float: " << ex.what()
                  << std::endl;
        break;
      }

    // parse v argument. If true, set visualArg to predefined position and
    // resolution
    case 'v':
      visualArg = " --window 60 60 800 400";
      break;
    }
  }
  // prepare string used to pass arguments to ESMINI
  std::string argsComp =
      " esmini --seed 5 --disable_stdout --SingleThreaded --osi_receiver_ip 49198 --osc "; // --disable_stdout  // esmini and space before --disable_controllers --fixed_timestep 0.01 --osi_receiver_ip 49198 --record sim.dat
                                                 // closing" are important!
  argsComp.append(oscPath);
  argsComp.append(visualArg);

  // split the string into individual arguments
  std::vector<std::string> split = SplitString(argsComp, ' ');

  // prepare arguments for ESMINI Init
  std::vector<std::string> argsESMINI;

  for (int i = 0; i < (int)split.size(); i++) {
    argsESMINI.push_back(split[i]);
  }

  // get number of arguments and reserve space in memory to store them
  int argcSIM = (int)argsESMINI.size();
  char **argvSIM = (char **)malloc(argcSIM * sizeof(char *));

  // copy argument strings as c_strings into prepared memory
  for (int i = 0; i < argcSIM; i++) {
    argvSIM[i] = (char *)malloc((argsESMINI[i].size() + 1) * sizeof(char));
    strcpy(argvSIM[i], argsESMINI[i].c_str());
  }

  // initialize ESMINI and open OSI
  SE_InitWithArgs(argcSIM, const_cast<const char **>(argvSIM));
  SE_OpenOSISocket(ip);
  // instantiate Benchmark Object
  Benchmark benchmark(modifier);
  benchmark.setMode(static_cast<BenchmarkMode>(BMMode));
  // step simulation until end of the scenario or ESC is pressed
  while (SE_GetQuitFlag() == 0) {
    if (bench) {
      benchmark.startTimer();
    }
    SE_StepDT(timeStep);
    if (bench) {
      benchmark.stopTimer();
      // std::cout << benchmark.timerDuration.count() << std::endl;
    }
  }

  SE_Close();
  if (bench) {
    benchmark.getResults();
  }
  return 0;
}
