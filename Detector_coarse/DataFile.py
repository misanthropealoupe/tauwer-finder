import sys
import math
import numpy
import time
from ThreeTup import *
from scipy.sparse import *
import os

valsep = ' '
deltaH = 800.0
newl = '\n'
z = ThreeTup([0.0,0.0,1.0])
searchAngle = math.radians(20.0)
angleTol = math.radians(5.0)
minzdot = math.cos(searchAngle + angleTol)
maxzdot = math.cos(searchAngle - angleTol)
datumsize = 11
nlsize = 2
eqRad = 6378137 #equatorial radius (m)
polRad = 6356752.3 #polar radius (m)
datadir = "data"
slopedir = "slope_masks"
filesep = '/'
ext = 'grd'


def findboundaries():
    return False

#Proceed to the line with elevation data
def zerofile(f):
    f.seek(0,0)
    for x in xrange(1,6):
        f.readline()

def r(lat): #Latitude in radians
    return 1/math.sqrt(math.pow(math.cos(lat)/eqRad,2) + math.pow(math.sin(lat)/polRad,2))

def slopevalid(tup):
    val = tup*z
    return val <= maxzdot and val >= minzdot

def getinds(cornerindex):
    return [ThreeTup([(cornerindex+1)%4,0,0]),ThreeTup([0,cornerindex%4,0])]

def norm(lst):
    ret = 0;
    for l in lst:
        ret += math.pow(l,2)
    return math.sqrt(ret)

def azimuth(self):
    return ath.atan(self[1]/self[0]) + (self[0] < 0)*math.pi

def ensuredir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

class DataFile:
    def __init__(self, path, readData):
        self.path = path
        self.parseMetaData()
        self.openfiles = []
        if readData:
            getData()
    def parseMetaData(self):
        f = open(self.path, 'r+')
        #burn line
        f.readline()
        
        #set x,y dims
        line = f.readline().strip()
        self.dim = [int(entry) for entry in line.split(valsep)]
        
        #set min/max lon, lat, and height (m)
        line = f.readline().strip()
        self.lon = [math.radians(float(entry)) for entry in line.split(valsep)]
        line = f.readline().strip()
        self.lat = [math.radians(float(entry)) for entry in line.split(valsep)]
        self.dl = []
        self.dl.append(abs(self.lon[1] - self.lon[0])/float(self.dim[0]))
        self.dl.append(abs(self.lat[1] - self.lat[0])/float(self.dim[1]))
        self.avelat = (self.lat[1] - self.lat[0])/2.0
        self.ds = []
        self.ds.append(self.dl[0]*math.cos(self.avelat)*r(self.avelat))
        self.ds.append(self.dl[1]*r(self.avelat))
        line = f.readline().strip()
        self.h = [float(entry) for entry in line.split(valsep)]
        self.viable = (self.h[1] - self.h[0] >= deltaH)
        f.close()
    def getData(self, ind=-1):
        tstart = time.time()
        f = open(self.path,'r')
        zerofile(f)
        self.dat = numpy.zeros((self.dim[0],self.dim[1]), dtype=float)
        strval = ''
        char = f.read(1)
        nvals = 0
        ntot = self.dim[0]*self.dim[1]
        t = time.time()
        while(char is not None):
            if char == valsep or char == newl:
                xind = nvals % self.dim[0]                    
                yind = (nvals - xind)/self.dim[1]
                self.dat[xind,yind] = float(strval.strip())
                nvals += 1

                if nvals % int(inc) == 0:
                    tn = time.time()
                    print "ELAPSED {1}: {0}".format(tn - tstart,ind)
                    print "PROG {1}: {0}".format(1.0 - float(ntot - nvals)/float(ntot),ind)
                    print "ETA {1}: {0}".format(float(ntot - nvals)*float(tn - t)/inc,ind)
                    print "---------------------------------------------------------------"
                    t = tn
                strval = ''
            else:
                strval += char
            char = f.read(1)
        f.close()
        #return dat
    def efficientanalyze(self,uid=-1):
        f = open(self.path,'r') 
        #states = lil_matrix((2*(coarse[0] - 1),2*(coarse[1] - 1)),dtype=int)
        #coarsemask = lil_matrix((1,1),dtype=bool)
             coarsemask = self.scan(f,4,uid)
        base = self.path[:-(len(ext) + 1)]
        parentdir = filesep.join([base,datadir])
        ensuredir(parentdir)
        parentdir = filesep.join([parentdir,slopedir])
        ensuredir(parentdir)
        datapath = filesep.join([parentdir,base.split(filesep)[-1]])
        ensuredir(datapath)
        numpy.save(datapath,coarsemask)
        del coarsemask
        f.close()
    def scan(self,f,interval,uid=-1):
        coarse = [l/interval for l in self.dim]
        slopemask = lil_matrix((2*(coarse[0] - 1),2*(coarse[1] - 1)),dtype=bool)
        ntot = (coarse[0] - 1)*(coarse[0] - 1)
        inc = 0.005*float(ntot)
        t = time.time()
        tstart = time.time()
        nvals = 0
        for r in xrange(0,coarse[0] - 1):
            for c in xrange(0,coarse[1] - 1):
                ind = ThreeTup([4*r,4*c,0])
                base = self.getptT(f,ind)

                for j in xrange(0,4):
                    targetind = ThreeTup([2*r + int((j%4 > 1)),2*c + int((j + 1)%4 > 1),0])
                    deltr = ThreeTup([r + int((j + 1)%4 < 2),0,0])
                    #deltr[0] += (deltr[0] - 1)*(deltr[0] + 1)
                    deltc = ThreeTup([0,c + int(j%4 < 2),0])
                    #deltc[1] += (deltc[1] - 1)*(deltc[1] + 1)
                    hand = float((j%2 == 1))
                    hand += (hand - 1.0)*(hand + 1.0)

                    #t = time.time()
                    a = self.getptT(f,deltr)
                    #delt = (time.time() - t)
                    #print "Time to fetch: {0}".format(delt)
                    #print "Projection: {0}".format(8.0*float(ntot)*delt)

                    res = ((self.getptT(f,deltr) - base)//(self.getptT(f,deltc) - base))*hand
                    if(norm(res) != 0.0):
                        res = res*(1/norm(res))
                        slopemask[targetind[0],targetind[1]] = slopevalid(res)
                    #res = res*(1.0/norm(res))
                    #print [deltr[0],deltc[1]]
                    #print [res[0],res[1],res[2]]
                    #print [base[0],base[1],base[2]]
                    #print math.degrees(math.acos(abs(res[2])))

                nvals += 1
                if(nvals%int(inc) == 0):
                    tn = time.time()
                    print "ELAPSED {1}: {0}".format(tn - tstart,uid)
                    print "PROG {1}: {0}".format(1.0 - float(ntot - nvals)/float(ntot),uid)
                    print "ETA {1}: {0}".format(float(ntot - nvals)*float(tn - t)/inc,uid)
                    print "---------------------------------------------------------------"
                    t = tn
        return slopemask

    def getptT(self,f,tup):
        return self.getpt(f,int(tup[0]),int(tup[1]))

    def getpt(self,f,xind,yind):
        zerofile(f)
        ind = (xind + yind*(self.dim[1]))*datumsize + (yind*(self.dim[0]) + xind) #Adjust for spaces
        f.seek(ind,1)
        tup = self.getxy(xind,yind)
        val = f.read(datumsize)
        tup[2] = float(val.strip())
        return tup
    def getxy(self,xind,yind):
        return ThreeTup([float(xind)*self.ds[0],float(yind)*self.ds[1],0]) #negate y (lat) for handedness

    def getfile(self):
        f = open(self.path,'r+')
        self.openfiles.append(f)
        return f
    def closefiles(self):
        for f in self.openfiles:
            f.close()

class IncDatum(ThreeTup):
    def azimuth(self):
        return math.atan(self[1]/self[0]) + (self[0] < 0)*math.pi