import subprocess

i=0
while i<10 :
    # subprocess.call("test1.py", shell=True)
    exec(open("test1.py").read())
    i+=1

    