import DataFile
import sys
import numpy
import multiprocessing
import math
import Queue
from os import listdir
from os.path import isfile, join

fext = 'grd'
#threadct = 5
def procact(fileq, ind):
    while(not fileq.empty()):
        datafile = fileq.get()
        #datafile.getData(ind)
        datafile.efficientanalyze(ind)
        fileq.task_done()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    # etc., replacing sys.argv with argv in the getopt() call.

    mypath = argv[1]
    files = [ join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) and f.split(".")[len(f.split(".")) - 1] == fext]
    i = 0;
    procs = []
    fileqs = []

    threadct = int(argv[2])
    perthread = len(files)/threadct
    for j in xrange(0,threadct):

        thisq = Queue.Queue()
        for k in xrange(j*perthread, (j+1)*perthread):
            thisq.put(DataFile.DataFile(files[k],False))

        p = multiprocessing.Process(target=procact,args=(thisq,j + 1))
        fileqs.append(thisq)
        procs.append(p)
    for p in procs:
        p.start()

if __name__ == "__main__":
    main()

