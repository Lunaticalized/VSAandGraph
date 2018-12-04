
from Graph import *

import os


"""
    To generate the averaged loss number distribution for hypo3


"""

def process(mypath):
    
    loss = []
    cnt = 0
    losszero = 0
    M = 0
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        for filename in filenames:
            g = GraphColor()
            if "color" in filename:
                print dirpath+filename
    	        g.read(dirpath+filename)
    	        missing2 = g.metric2()  
                M = max(M, missing2)
                if missing2 > 0 or True:

            	   loss.append(missing2)
                if missing2 == 0:
                    losszero += 1

                cnt += 1
    print cnt, "found"
    print losszero, "are zero"
    print M		    
    bins = np.arange(min(loss), max(loss), 0.01)
    plt.hist(loss, normed=False, bins=bins)
    plt.xlabel("Averaged program loss")
    plt.ylabel("Frequency")
    plt.show()



def hypo1():
    mypath = "data/hypo1/result/"

    process(mypath)


def hypo2():
    mypath = "./data/sample2repeat100/result/"
    process(mypath)



def hypo3():
    mypath = "data/hypo3/result/"

    process(mypath)


hypo2()
