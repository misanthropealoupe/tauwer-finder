import sys
import Queue
import threading
import time
import DataFile
from os import listdir
from os.path import isfile, join

fext = 'grd'
def main(argv=None):
    if argv is None:
        argv = sys.argv

    mypath = argv[1]
    files = [ join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) and f.split(".")[len(f.split(".")) - 1] == fext]
    f = open(files[0],'r')
    print f.read(200)
    d = DataFile.DataFile(files[0],False)

    f = d.getfile()
    ts = time.time()
    for i in xrange(0,10000):
        p = d.getpt(f,i,0)
    print "Perpoint: %f" % ((time.time() - ts)/10000.0)
    print "Per File: {0}".format(float(d.dim[0]*d.dim[1])*(time.time() - ts)/10000.0)
    d.closefiles()

if __name__ == "__main__":
    main()

