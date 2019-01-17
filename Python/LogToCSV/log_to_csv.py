# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 13:27:27 2019

@author: rohtua
"""
import os

def main():
    file_path = os.getcwd() + '\\logfile.log'
    file_csv = os.getcwd() + '\\logfile.csv'
    f=open(file_path,"r")
    f1 = f.readlines()
    for x in f1:
        y=x
        if x.find("***")==-1:
            x = x.replace(" ",",",6)
        elif x.find("***<Time>")==0:
            x = x.replace("><",">,<",6)
        x = x.replace("***","")
        f1[f1.index(y)] = x
    f1[5] = f1[len(f1)-3]
    f.close()
    f=open(file_csv,"w+")
    f.writelines(f1)
    f.close()
if __name__=="__main__":
    main()