#include "Benchmark.hpp"
#include "UDP.hpp"
#include <chrono>
#include <cmath>
#include <fstream>
#include <string>
#include <sys/stat.h>
#include <vector>

class DM {
public:
  explicit DM(double timestepInput = 0.01, bool log = false, std::string ip = "127.0.0.1", std::string DMMode ="");
  ~DM(){};
  std::string columns =
      "Timestamp,distance,vTheta,vThetaDot,Vp,activationChange,vActivation,"
      "bModelIsBreaking,response,vpp";
  void runDM();
  // piecewise linear functions (support functions for DM)
  void CalcG(double &calcg) const;
  void CalcH(std::pair<float, double> &calch) const;
  void closeLog() {
    if (file.is_open()) {
      file.close();
    }
  }

// DM main functions
  // threat-assessment related
  - removed to protect IP
  
  // accumulator related
  - removed to protect IP
  
  // breaking model related
  - removed to protect IP
  
  // values for piecewise linear functions
  - removed to protect IP
  
  // vector (lists) for piecewise linear function
  - removed to protect IP
  
  // used to accelarate the EgoVehicle at the beginning of the Scenario
  bool initMove = true;
  // logging related
  std::string getDateTime();
  bool log = false;
  std::ofstream file;
  
  UDP udpObj;
};
