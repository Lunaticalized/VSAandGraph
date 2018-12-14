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


def parseAllTasks():
    TASKS = {}
    mypath = "./prose-benchmarks/Transformation.Text"
    cnt = 0
    for (dirpath, dirnames, filenames) in os.walk(mypath):

        subtask = dirpath.split("/")[-1]
        task = subtask.split(".")[0]
        if task == "Transformation":
            continue
        if task not in TASKS:
            TASKS[task] = {}

        if subtask not in TASKS[task]:
            TASKS[task][subtask] = []

        for filename in filenames:
            
            debris = filename.split('.')
            if debris[0] == 'spec' and debris[1] == 'json':
                fname = dirpath + "/" +filename
                file = open(fname, 'r')
                
                line = file.read()
                ret = json.loads(line)
                file.close()
                arr = ret["Examples"]
                
                for ex in arr:
                    try:
                        Input = removeNextLine("|".join(ex["Input"]))
                        Output = removeNextLine(ex["Output"])
                        if Input and Output:
                            s = Input + "^" + Output
                            TASKS[task][subtask].append(s)
                            cnt += 1
                    except UnicodeEncodeError:
                        pass
                    except TypeError:
                        pass
                    except ValueError:
                        pass 
    return TASKS

def hypo1():
    mypath = "./prose-benchmarks/Transformation.Text"
    outpath = "./data21/hypo1/"

    if not os.path.exists("./data21/"):
        os.mkdir("./data21/")
        os.mkdir("./data21/hypo1/")
        os.mkdir("./data21/hypo1/result/")

    if not os.path.exists("./data21/hypo1/"):
        os.mkdir("./data21/hypo1/")
        os.mkdir("./data21/hypo1/result/")

    if not os.path.exists("./data21/hypo1/result/"):
        os.mkdir("./data21/hypo1/result/")
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

def hypo2():
    mypath = "./prose-benchmarks/Transformation.Text"
    outpath = "./data21/hypo2/"

    if not os.path.exists("./data21/"):
        os.mkdir("./data21/")
        os.mkdir("./data21/hypo2/")
        os.mkdir("./data21/hypo2/result/")

    if not os.path.exists("./data21/hypo2/"):
        os.mkdir("./data21/hypo2/")
        os.mkdir("./data21/hypo2/result/")

    if not os.path.exists("./data21/hypo2/result/"):
        os.mkdir("./data21/hypo2/result/")


    TASKS = parseAllTasks()
    
    cnt = 0
    
    for task in TASKS:
        outfile = open(outpath + task + ".txt", "w")
        examples = []
        for subtask in TASKS[task]:
            subex = random.sample(TASKS[task][subtask], min(2, len(TASKS[task][subtask])))
            examples += subex
        print len(examples)
        print examples

        for ex in examples:
            try:
                print >> outfile, ex
                cnt += 1
            except UnicodeEncodeError:
                pass
            except TypeError:
                pass
            except ValueError:
                pass 

        outfile.close()

    


def hypo3():
    mypath = "./prose-benchmarks/Transformation.Text"
    outpath = "./data21/hypo3/"


    if not os.path.exists("./data21/"):
        os.mkdir("./data21/")
        os.mkdir("./data21/hypo3/")
        os.mkdir("./data21/hypo3/result/")

    if not os.path.exists("./data21/hypo3/"):
        os.mkdir("./data21/hypo3/")
        os.mkdir("./data21/hypo3/result/")

    if not os.path.exists("./data21/hypo3/result/"):
        os.mkdir("./data21/hypo3/result/")

    TASKS = parseAllTasks()
    
    cnt = 0
    
    for cnt in range(1000):
        outfile = open(outpath + str(cnt) + ".txt", "w")
        allthings = []
        for task in TASKS:
            examples = []
            for subtask in TASKS[task]:
                examples += TASKS[task][subtask]
            
            allthings += (random.sample(examples, 1))

        
        for ex in allthings:
            try:
                print >> outfile, ex
                cnt += 1
            except UnicodeEncodeError:
                pass
            except TypeError:
                pass
            except ValueError:
                pass 

        outfile.close()


def main():
    hypo1()
    hypo2()
    hypo3()
    

if __name__ == "__main__":
    main()