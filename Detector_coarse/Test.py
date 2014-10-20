import sys
import Queue
import threading
import time
from os import listdir
from os.path import isfile, join

fext = 'grd'
q = Queue.Queue()
def printdat(f,length):
	start = time.time()
	reads = 0
	while time.time() - start < 20.0:
		print f.read(length)
		++reads
		print reads

	q.put(True)
def main(argv=None):
    if argv is None:
        argv = sys.argv

    mypath = argv[1]
    files = [ join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) and f.split(".")[len(f.split(".")) - 1] == fext]
    fobj = []
    for i in xrange(0,int(argv[2])):
    	fobj.append(open(files[1]))
    	t = threading.Thread(target=printdat, args = (fobj[i],10))
    	t.daemon = True
    	t.start()

    print q.get();
if __name__ == "__main__":
    main()

