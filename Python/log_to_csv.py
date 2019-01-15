# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 13:27:27 2019

@author: kk426
"""
import os

def main():
    file_path = os.getcwd() + '\\file_to_csv.txt'
    
    f=open(file_path,"r+")
    
    f1 = f.readlines()
    
    for x in f1:
        #line here
        if x.find("***")==-1:
            x.replace(" Rx 1 ",",Rx,1,")
            

if __name__=="__main__":
    main()