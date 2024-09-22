#include "Benchmark.hpp"
#include <ios>
#include <ostream>
#include <string>
#include <sys/stat.h>

void Benchmark::stopTimer() {
  timerEnd = std::chrono::steady_clock::now();
  timerDuration = timerEnd - timerStart;
  timerSum += timerDuration;

  allIterations.push_back(timerDuration.count());
}

void Benchmark::getResults() {
  if (mode == AVG or mode == BOTH) {
    std::cout << timerSum.count() / allIterations.size() << std::endl;
  }

  if (mode == ALL or mode == BOTH) {
    std::string outputPath = "../output/";
    mkdir(outputPath.c_str(), 0777);
    std::string dateTime = getDateTime();
    std::string filePath =
        outputPath + "Cpp" + DMMode + dateTime + ".csv";
    std::ofstream benchAllIt;
    benchAllIt.open(filePath, std::ios_base::out);
    for (auto result : allIterations) {
      benchAllIt << result << std::endl;
    }
    benchAllIt.close();
  }
}

std::string Benchmark::getDateTime() {
  time_t rawtime;
  struct tm *timeinfo;
  char buffer[80];

  time(&rawtime);
  timeinfo = localtime(&rawtime);
  strftime(buffer, sizeof(buffer), "-%m%d-%H%M_%S", timeinfo);
  std::string str(buffer);
  return str;
}
