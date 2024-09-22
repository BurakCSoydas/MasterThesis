import ctypes as ct
import argparse
from Benchmark import * 


def main():
    # parsing command line arguments to toggle benching and video output as
    # well as being able to change XOSC file and timestep
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--osc', default='../resources/xosc/thesis.xosc')
    parser.add_argument('-t', '--timestep',type=float, default=0.01)
    parser.add_argument('-n', '--numberIterations',type=int, default=700)
    parser.add_argument('-v', '--visual', action='store_true')
    parser.add_argument('-b', '--bench', type=int, default=0)
    parser.add_argument('-m','--modifier', type = str, default='')
    args = parser.parse_args()
    

    # variables used to get execution time
    bm = Benchmark(args.modifier)
    bm.setMode(args.bench) 

    # preparing arguments to pass to ESMINI Init
    if args.visual:
        visualarg = ["--window", "60", "60", "800", "400"]
    else:
        visualarg = ["--headless"]
    timestep = ct.c_float(float(args.timestep))

    # creating a char* array, passed to ESMINI Init
    # is equal to char* argv[] or char** argv
    # cargs = (ctypes.c_char_p * 4)(osc, visualarg, b'--seed 5', b'--disable_stdout')
    # using ctypes to get a handle on ESMINI inside Python
    se = ct.CDLL("../resources/lib/libesminiLib.so")

    # specify arguments types of esmini function
    se.SE_InitWithArgs.argtypes = [ct.c_int, ct.POINTER(ct.POINTER(ct.c_char))]
    
    # create the list of arguments
    cargs = [
        "--osc", args.osc,
        "--seed", "5",
        "--disable_stdout",
        "--SingleThreaded",
        "--osi_receiver_ip","49198",
        ]
    cargs += visualarg
# prepare argument list for ctypes use
    argv = (ct.POINTER(ct.c_char) * len(cargs))()
    argc = len(argv)
    for i, arg in enumerate(cargs):
        argv[i] = ct.create_string_buffer(arg.encode())

# init esmini
    if se.SE_InitWithArgs(argc, argv) != 0:
        exit(-1)
    se.SE_OpenOSISocket('127.0.0.1')

    while se.SE_GetQuitFlag() == 0:
        if args.bench:
            bm.startTimer()
        se.SE_StepDT(timestep)
        if args.bench:
            bm.stopTimer()
    se.SE_Close()
    if args.bench:
        bm.getResults(args.numberIterations)

if __name__ == "__main__":
    main()
