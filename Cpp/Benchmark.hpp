#pragma once

#include <chrono>
#include <cwchar>
#include <fstream>
#include <iostream>
#include <string>
#include <unistd.h>
#include <vector>

enum BenchmarkMode { OFF, AVG, ALL, BOTH = AVG + ALL };

class Benchmark {
public:
  Benchmark( std::string DMModeInput = ""){ DMMode = DMModeInput ;}
  ~Benchmark(){};

  /**
   * set the Benchmark Mode
   *  1 = OFF
   *  2 = AVG
   *  3 = ALL
   *  4 = BOTH
   */
  void setMode(BenchmarkMode modeIn) { mode = modeIn; }

  /**
   * stores the time at time of call. Used to calculate the durations
   * with stopTimer().
   */
  void startTimer() { timerStart = std::chrono::steady_clock::now(); }

  /**
   * gets time it is called and calculates the duration since
   * the start time. The duration is then stored at the end of
   * a vector (dynamic array), holding all durations and adds
   * the new duration to a sum.
   */
  void stopTimer();

  /**
   * Depending on Benchmark.mode:
   * If mode == AVG: diplays timerSum/NoIterations
   * if mode == ALL: creates a .csv file containing all
   * benched durations.
   * Does both if mode == BOTH.
   */
  void getResults();

// private:
  /**
   * returns the current datetime ("%m%d_%H%M%S")
   */
  std::string getDateTime();
  std::chrono::time_point<std::chrono::steady_clock> timerStart, timerEnd;
  std::chrono::duration<long double, std::ratio<1, 1000000>> timerDuration,
      timerSum{0};
  std::vector<long double> allIterations;
  BenchmarkMode mode = BenchmarkMode::OFF;
  std::string DMMode;

};
