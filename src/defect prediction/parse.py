# Result parer. Computes AUC and d2h on outputs from main_d2h.py, specifically
# designed for defect prediction. It is used as follows:
# 
# python3 parse.py FILENAME POS
#
# where FILENAME is the name of the file to parse, and POS is the index (0-
# based) of the result to parse.

import sys
import numpy as np

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Get the result line
    line = [x for x in lines if x[0] == '{'][int(sys.argv[2])]

    # Parse to a Python dict
    d = eval(line)

    li = list(d['counter_full'][0.2].values())
    med = [round(np.median(y), 3) for y in li]
    print('min pf:', min(li[29]))

