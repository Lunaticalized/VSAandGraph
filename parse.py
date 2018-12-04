import json
import os
import random


def removeNextLine(s):
    ret = ""
    for c in s:
        if c == '\n' or c == '\t':
            ret += " "
        else:
            ret += c
    return ret

def plotDistribution(arr):
    import matplotlib.pyplot as plt
    import numpy as np
    
    bins = np.arange(0, max(arr) + 1.5) - 0.5
    plt.hist(arr, normed=False, bins=bins)
    plt.xlabel("Number of examples per task")
    plt.ylabel("Frequency")
    plt.show()

def ComputeCorpse(mypath, outname, prob=1, threshold=1000):

    outfile = open(outname, 'w')
    cnt = 0
    lengths = []
    
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        if random.random() > prob:
            continue
        for filename in filenames:
            debris = filename.split('.')
            if debris[0] == 'spec' and debris[1] == 'json':
                fname = dirpath + "/" +filename
                file = open(fname, 'r')
                line = file.read()
                ret = json.loads(line)

                arr = []
                
                if len(ret["Examples"]) > threshold:
                    arr = random.sample(ret["Examples"], threshold)
                else:
                    arr = ret["Examples"]
                
                lengths.append(len(arr))
                for ex in arr:
                    try:
                        Input = removeNextLine("|".join(ex["Input"]))
                        Output = removeNextLine(ex["Output"])
                        if Input and Output:
                            s = Input + "^" + Output
                            print s
                            print >> outfile, s
                            cnt += 1
                    except UnicodeEncodeError:
                        pass
                    except TypeError:
                        pass
                    except ValueError:
                        pass 
                file.close()
    print "\n\nTotally " + str(cnt) + " shits found." 
    outfile.close()
    
    lengths.sort()
    ss = set(lengths)
    checkpoints = [1.0 * i / 10 for i in range(10)]
    for val in ss:
        percent = 1.0*len([i for i in lengths if i >= val]) / len(lengths)
        est = 0.1 * round(10 * percent)
    #plotDistribution(lengths)




def sampleForClique():
    mypath = "./prose-benchmarks/Transformation.Text"
    outpath = "./data/feed/cliqueTest/"
    cnt = 0
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        for filename in filenames:
            debris = filename.split('.')
            if debris[0] == 'spec' and debris[1] == 'json':
                fname = dirpath + "/" +filename
                file = open(fname, 'r')
                outfile = open(outpath + str(cnt) + ".txt", "w")
                line = file.read()
                ret = json.loads(line)

                arr = ret["Examples"]
                
                for ex in arr:
                    try:
                        Input = removeNextLine("|".join(ex["Input"]))
                        Output = removeNextLine(ex["Output"])
                        if Input and Output:
                            s = Input + "^" + Output
                            print >> outfile, s
                            cnt += 1
                    except UnicodeEncodeError:
                        pass
                    except TypeError:
                        pass
                    except ValueError:
                        pass 
                file.close()
                outfile.close()


def main():
    threshold = 1
    prob = 66
    trial = 0
    # for trial in range(1000):

    mypath = "./prose-benchmarks/Transformation.Text"
    # outname =  "./data/feed/cliqueTest/testing"+str(trial)+"_"+str(threshold)+"_"+str(prob)+".txt"       
    #     ComputeCorpse(mypath, outname, prob, threshold)
    # thresholds = [1]
    # probs = [1]

    # for i in range(len(thresholds)):
    #     threshold = thresholds[i]
    #     prob = probs[i]
    #     ComputeCorpse(mypath, outname, prob, threshold)



    
    

if __name__ == "__main__":
    #main()
    sampleForClique()