import re
import struct
import sys
import os
from time import sleep
import numpy
from subprocess import call, PIPE, Popen



def parse_args():
    # path, LPP pulse lenth ns, Identifier,
    X_array=[0.000,0.000,0.000,0.000,0.000]
    Y_array=[0.000,0.000,0.000,0.000,0.000]
    
    X_array[0] = float(sys.argv[1])
    X_array[1] = float(sys.argv[2])
    X_array[2] = float(sys.argv[3])
    X_array[3] = float(sys.argv[4])
    X_array[4] = float(sys.argv[5])
    
    Y_array[0] = float(sys.argv[6])
    Y_array[1] = float(sys.argv[7])
    Y_array[2] = float(sys.argv[8])
    Y_array[3] = float(sys.argv[9])
    Y_array[4] = float(sys.argv[10])


    return X_array, Y_array


if __name__ == "__main__":
    #fix_nvs_float()
    sleep(1)
    # Parse Arguments
    distance, readings = parse_args()
    
    p_array = numpy.polyfit(distance,readings,2)

    # Polynomial coefficients
    p1 = p_array[0]
    p2 = p_array[1]
    p3 = p_array[2]

    # Solve for peak
    peak_location = round((-1 * p2) / (p1 * 2), 3)

    #self.logger.info('Polynomial coefficients: ' +f' f(s) = {round(p1,4)}s^2 + {round(p2,4)}s^1 + {round(p3,4)}s^0')

    output = "{}, \n".format(peak_location)

    # Write results to output
    sys.stdout.write(output)
    sys.stdout.flush()
    sys.exit(0)

