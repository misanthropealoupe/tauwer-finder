import sys
from os import listdir
from os.path import isfile, join

fext = 'grd'
def main(argv=None):
    if argv is None:
        argv = sys.argv

    mypath = argv[1]
    files = [ join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) and f.split(".")[len(f.split(".")) - 1] == fext]
    f = open(files[int(argv[2])],'r+')
    print f.read(1000)
    f.close()
    del f

if __name__ == "__main__":
    main()

