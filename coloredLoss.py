
from Graph import *
import random
import os


"""
    To generate the averaged loss number distribution for the graphs
        stored under mypath

    withZero: generate the histogram with zero loss
"""

def process(mypath, withZero):
    
    loss = []
    cnt = 0
    losszero = 0
    M = 0
    MM = 0
    m = 1000000
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        for filename in filenames:
            g = GraphColor()
            if "newcolor" in filename:
                print dirpath+filename
    	        g.read(dirpath+filename)
    	        missing2 = g.metric2()  
                M = max(M, missing2)
                MM = max(MM, g.n)
                m = min(m, g.n)
                if missing2 > 0 or withZero:
            	    loss.append(missing2)
                if missing2 == 0:
                    losszero += 1

                cnt += 1
    print cnt, "found"
    print losszero, "are zero"
    print M		
    print MM, m    
    bins = np.arange(min(loss), max(loss), 0.01)
    plt.hist(loss, normed=False, bins=bins)
    plt.xlabel("Averaged program loss")
    plt.ylabel("Frequency")
    plt.show()


"""
    Return the predicted loss accuracy
         (if average loss number is larger than 0.3)
         for all graphs under mypath

    thre: parameter for the threshold
    
"""
def predict(mypath, thre):
    
    loss = []
    cnt = 0
    losszero = 0
    M = 0
    MM = 0
    m = 1000000

    total = 0
    correct = 0

    for (dirpath, dirnames, filenames) in os.walk(mypath):
        for filename in filenames:
            g = GraphColor()
            if "newcolor" in filename:
                g.read(dirpath+filename)
                missing2 = g.metric2()  
                M = max(M, missing2)
                MM = max(MM, g.n)
                m = min(m, g.n)

                actual = 0
                if missing2 > 0.4:
                    actual = 1

                predict = 0

                randv = int(g.n * random.random())

                if len(g.edges[randv]) > thre:
                    predict = 1

                total += 1

                if predict == actual:
                    correct += 1
    if total == 0:
        accu = 1
    else:
        accu = 1.0 * correct / total
    return accu

def hypo1(withZero):
    mypath = "data/hypo1/result/"
    process(mypath, withZero)

def hypo2(withZero):
    mypath = "./data/hypo2/result/"
    process(mypath, withZero)

def hypo3(withZero):
    mypath = "data/hypo3/result/"
    process(mypath, withZero)



def pred1(thre):
    mypath = "data/hypo1/result/"
    return predict(mypath, thre)


def pred2(thre):
    mypath = "./data/hypo2/result/"
    return predict(mypath, thre)

def pred3(thre):
    mypath = "data/hypo3/result/"
    return predict(mypath, thre)


def plotThreshold():
    cat1 = []
    cat2 = []
    cat3 = []
    cap = 16
    axis = range(0, cap)
    for th in range(0, cap):
        print "Threshold: " + str(th) + "/" + str(cap-1)
        a1 = pred1(th)
        a2 = pred2(th)
        a3 = pred3(th)
        cat1.append(a1)
        cat2.append(a2)
        cat3.append(a3)

    plt.scatter(axis,cat1)
    plt.scatter(axis,cat2)
    plt.scatter(axis,cat3)
    plt.plot(axis,cat1)
    plt.plot(axis,cat2)
    plt.plot(axis,cat3)
    plt.ylabel("Prediction accuracy")
    plt.xlabel("Threshold")
    plt.legend(['cat. 1', 'cat. 2', 'cat. 3'], loc='lower right')

    plt.show()


def computeLoss(withZero):
    hypo1(withZero)
    hypo2(withZero)
    hypo3(withZero)

computeLoss(False)
computeLoss(True)
plotThreshold()