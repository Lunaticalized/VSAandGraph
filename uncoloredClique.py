from Graph import *
import os

def process(file, mypath, plot=False):

	avgRatio = 0
	avgCliq = 0
	cnt = 0
	avgN = 0
	M = 0
	for (dirpath, dirnames, filenames) in os.walk(mypath):
	    for filename in filenames:
	    	
	    	if filename.split(".")[1] != "txt" or "color" in filename:
	    		continue

	        g = Graph()
	        g.read(dirpath+filename)
	        print dirpath + filename
	        clique = g.find_maximal_cliques_greedy(0)
	        missing = g.countMissingPrograms(clique)        
	        maxSize = max([len(c) for c in clique])
	        ratio = maxSize*1.0 / g.n

	        
	        if plot:
	        	g.drawGraph()
		        #g.plotDegDistribution()
		        g.approximatePowerLaw()

	        avgRatio = (avgRatio * cnt + ratio) / (cnt + 1)
	        avgCliq = (avgCliq * cnt + maxSize + 0.0) / (cnt + 1)
	        avgN = (avgN * cnt + g.n + 0.0) / (cnt + 1)
	        cnt += 1
	        M = max(M, g.n)
	        #print filename, missing, maxSize, ratio
	print "Processed", cnt
	print "avg max clique size", avgCliq
	print "avg graph size", avgN
	print "avg ratio", avgRatio  
	print M
	#print avgRatio, avgCliq, avgN

def hypo1(plot=False):
	file = "hypo1.txt"
	mypath = "./data/hypo1/result/"
	process(file, mypath, plot)


def hypo2(plot=False):
	file = "hypo2.txt"
	mypath = "./data/sample2repeat100/result/"
	process(file, mypath, plot)



def hypo3(plot=False):
	file = "hypo3.txt"
	mypath = "./data/hypo3/result/"	
	process(file, mypath, plot)


def attempts(plot=False):
	file = "attempts.txt"
	mypath = "./data/attempts/result/"
	process(file, mypath, plot)


attempts()



