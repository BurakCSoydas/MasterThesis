
from enum import Flag
from time import perf_counter_ns as timerNS
from datetime import datetime
import os


class Benchmark:
    """This class was written to benchmark software conviniently.
    It prints the average time to console or creates a .csv file
    containing all bench times of the run."""

    class BenchmarkMode(Flag):
        OFF = 0
        AVG = 1
        ALL = 2
        BOTH = 3

    def __init__(self, DMMode=""):
        # variables used to store times
        self.timerStart: float
        self.timerEnd: float
        self.timerSum: float = 0
        self.allDurations: list[float] = []
        self.mode: BenchmarkMode = self.BenchmarkMode.OFF
        self.DMMode: str = DMMode

    def setMode(self, selection: int = 0):
        """sets the Benchmark Mode
        1 = OFF
        2 = AVG
        3 = ALL
        4 = BOTH"""
        self.mode = self.BenchmarkMode(selection)

    def startTimer(self):
        """stores the timepoint when called. Used to calculate the durations
        with stopTimer()."""
        self.timerStart = timerNS()

    def stopTimer(self):
        """gets the timepoint when called and calculates the duration since
        the start timepoint. The duration is then stored at the end of an
        array, as well as added to a sum."""
        self.timerEnd = timerNS()
        self.timerDuration = (self.timerEnd - self.timerStart)/1000
        self.allDurations.append(self.timerDuration)
        self.timerSum += self.timerDuration

    def getResults(self, noIterations: int = 700):
        """Depending on Benchmark.mode:
        If mode == AVG: diplays timerSum/NoIterations
        if mode == ALL: creates a .csv file containing all
        bench durations.
        Does both if mode == BOTH."""
        if self.mode == self.BenchmarkMode.AVG or self.mode == self.BenchmarkMode.BOTH:
            print(self.timerSum / noIterations)
        if self.mode == self.BenchmarkMode.ALL or self.mode == self.BenchmarkMode.BOTH:
            datetimeString = datetime.today().strftime("-%m%d-%H%M_%S")
            path = "../output/"
            if not os.path.exists(path):
                os.makedirs(path)
            with open(
                path + "PyDict" + self.DMMode + datetimeString + ".csv",
                "w",
            ) as fileALL:
                for _, entry in enumerate(self.allDurations):
                    fileALL.write(str(entry) + "\n")

