from gpflib import GPF
gpf=GPF("Chin")
Lua='''
Speedup(1)
OriOn()
Handle0=GetAS("<manner","","","","","","","","","")
Handle3=Freq(Handle0,"$Q",0)
Ret=Output(Handle3,1000)
return Ret

'''
def GetBCC1():
    ret=gpf.BCC("我们家")
    print(ret)
    
GetBCC1()    

