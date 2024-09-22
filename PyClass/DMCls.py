
import UDPCls as UDP
import os
from numpy import nan, arctan2
from datetime import datetime
import argparse
import Benchmark


class DM(UDP.UDP):
    def __init__(
        self, timestep: float = 0.01, log: bool = False, ip="127.0.0.1", mode=""
    ):
        # logging related
        self.log = log
        if self.log:
            # during benching we create logs to see its effect on performance.
            # The logs themselves are not useful and to avoid wasted storage
            # they are stored in "/tmp/", where they get deleted automatically.
            self.outputPath: str = "../tmp/"
            # check if output directory exists, and creates it if needed
            if not os.path.exists(self.outputPath):
                os.mkdir(self.outputPath)
            # header as string for the csv, containing the names of the variables logged.
            self.columns = [
                "Timestamp,distance,egoSpeed,vTheta,vThetaDot,Vp,"
                + "activationChange,vActivation,bModelIsBreaking,"
                + "response,vpp,targetLane\n"
            ]
            timestamp: str = datetime.now().strftime("-%m%d-%H%M_%S")
            # log is stored in *.csv
            self.filePath: str = (
                self.outputPath + "Log-PyClass" + mode + timestamp + ".csv"
            )
            self.logFile = open(self.filePath, "w")
            self.logFile.writelines(self.columns)

        # used for initial acceleration at scenario start
        self.moveInit: bool = True

        # threat-assessment related
        - removed to protect IP
      
        # accumulator related
        - removed to protect IP
      
        # breaking model related
        - removed to protect IP
      
        # values for piecewise linear functions
        - removed to protect IP
      
        # vector (lists) for piecewise linear function
        - removed to protect IP

        # calculated brake response
        self.response: float = 0.0

        # Init UDP object
        self.UDP = UDP.UDP(ip)

    def __del__(self):
        self.UDP.close()

    def runDM(self):
        """steps the Driver Model using receiveOSIGT and sends a breaking response to brake the ego vehicle if required.
        """

        if not self.UDP.firstGTReceived:
            return

        # store values from previous run

        # calculate positional data, with the position of the vehciles being position of center plus half of its length

        # calculate optical size and looming of target vehicle

        # calculate prediction error
        
        # run accumulator

        # if activation value passed
            # activate breaking model

            # store previous break response

            # set up values for linear piece-wise funtions

        # if brake model is activated
            # update values via linear piece-wise functions
            
            # calculate brake response

            # calculate brake delay

            # finally, set break response

            # calculate brake response

        # reset Vpp

        # calculate prediction for the next cycle

        # increase internal counter

        # log driver model parameters
        if self.log:
            logString = str(self.UDP.DMData.timestamp) + ","
            logString += "{:.6g}".format(self.prevDistEgoToTarget) + ","
            logString += "{:.6g}".format(self.UDP.DMData.egoSpeed) + ","
            logString += "{:.4g}".format(self.vTheta) + ","
            logString += "{:.4g}".format(self.vThetaDot) + ","
            logString += "{:.4g}".format(self.vp) + ","
            logString += "{:.4g}".format(activationChange) + ","
            logString += "{:.4g}".format(self.vActivation) + ","
            logString += "{:}".format(self.bModelIsBraking) + ","
            logString += "{:.4g}".format(self.response) + ","
            logString += "{:.4g}".format(self.vpp) + ","
            logString += "{:.4g}".format(self.UDP.DMData.targetLane)
            logString += "\n"
            self.logFile.write(logString)

        return

    def CalcH(self, i):
        # linear piece-wise funtion

    def CalcG(self, i):
        # linear piece-wise funtion


def main():
    """This function is intended to be run parallely to a simulation using the open-simulation-interface.
    It acts as the driver model for the ego vehicle in a simulation with one target vehicle. The Driver
    Model accelerates the ego vehicle to full speed at scenario start and keeps driving in a straight line.
    It will bring the ego vehicle to a full stop when the target vehicle is in the same lane and too slow.
    """
    # input argument parsing and value checking
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bench", type=int, default=0)
    parser.add_argument("-l", "--log", action="store_true")
    parser.add_argument("-m", "--modifier", type=str, default="")
    parser.add_argument("-n", "--numberIterations", type=int, default=700)
    parser.add_argument("-t", "--timestep", type=float, default=0.01)
    args = parser.parse_args()

    # init bench and set mode during value check
    benchmark = benchmark = Benchmark.Benchmark(args.modifier)

    if args.bench < 0 or args.bench > 3:
        print(
            "Please enter one of the following values:\n\t0: OFF\n\t1:AVG\n\t2:ALL\n\t3: BOTH"
        )
        print("Defaulting to OFF.")
    else:
        benchmark.setMode(args.bench)

    if args.numberIterations <= 0:
        print("Please enter an integer value bigger than 1 as number of iterations.")

    if args.timestep <= 0:
        print("Please enter a float value bigger than 0.00 as timestep value.")

    # init driver model
    dm = DM(timestep=args.timestep, log=args.log, ip="127.0.0.1", mode=args.modifier)

    for _ in range(args.numberIterations):
        if args.bench:
            benchmark.startTimer()

        dm.runDM()

        if args.bench:
            benchmark.stopTimer()

        if (dm.response > 0) and (dm.UDP.DMData.egoLane == dm.UDP.DMData.targetLane):
            dm.UDP.respondToESMINI(brake=dm.response, throttle=0.0, steeringAngle=0.0)
        else:
            dm.UDP.respondToESMINI()

        dm.UDP.receiveOSIGT()


    # get results and clean up files
    if args.bench:
        benchmark.getResults(args.numberIterations)

    # print(f"ENDPOSITION: {dm.UDP.DMData.egoPosX}")
    if args.log:
        dm.logFile.close()
    print(dm.prevDistEgoToTarget)
    dm.close


if __name__ == "__main__":
    main()

