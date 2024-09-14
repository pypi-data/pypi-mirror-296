from gpflib import GPF
gpf=GPF("GPFDat")
def GetBCC1():
    ret=gpf.BCC("冠军成绩")
    print(ret)
    
GetBCC1()    

