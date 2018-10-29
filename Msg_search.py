#!/usr/bin/env python
# coding: utf-8
import re
import io
import os
import threading
import quopri
from time import ctime
import sys,getopt
reload(sys)
sys.setdefaultencoding('utf-8') 

opts, args = getopt.getopt(sys.argv[1:], "hf:t:l:dc")
m0=0
file_path = ""
target = ""
loglocation=""

for opt, arg in opts:
   if opt == "-h":
      print 'Msg_search.py -f <file_path> -t <target> -l <loglocation> -d <header> -c <content>'
      sys.exit()
   elif opt == "-f":
      file_path = arg
   elif opt == "-t":
      target = arg
      target_r=re.compile(target)
   elif opt == "-l":
      loglocation = arg
   elif opt == "-d":
      m0=1
   elif opt == "-c":
      m0=2

def file_location(file_path):
                                     
    os.chdir(file_path)
    content_list = os.listdir(os.curdir)
    for each in content_list:
        if os.path.splitext(each)[1] == '.msg':
            file_path_list.append(os.getcwd() + os.sep + each)
        if os.path.isdir(each):                               


            file_location(each)
            os.chdir(os.pardir)

    
file_path_list = []
file_location(file_path)                                  


def list_targetfile(file_path, target):      
                    
    f = io.open(file_path,'rb')
    count_list = []
    
    try:
        for each_line in f:
            each_line=quopri.decodestring(each_line)
            count = each_line.count(target)
            count_list.append(count)
        
    except:
        pass
    if count_list.count(0) != len(count_list):
        target_file_list.append(file_path)
    f.close()


threads = []
 


def find_target(file_path, target):
                     
    line_number = 1
    with io.open(file_path,'rb') as f1 , io.open(loglocation+'/result.log','a+',encoding='utf-8') as f2:
        for each_line in f1:
            each_line=quopri.decodestring(each_line)
            
            try:
               
               target=re.findall(target_r,each_line)[0]
               count = each_line.count(target)           
               begin = each_line.find(target)
               if begin != -1:
                   begin_list = []
                   while begin != -1:
                       begin_list.append(begin)
                       begin = each_line.find(target, begin+1)
                   begin_str = ''
                   for each in begin_list:
                       begin_str = begin_str + str(each) + 'st '            
                   f2.writelines(u'[-]Appeared at the %scharacter of line %d, totally %d times.' % (begin_str, line_number, count)+'\n')
            except:
               pass

            
            
            line_number += 1
        f1.close()
        f2.close()

def search_header(file_path, target):
    with io.open(file_path,'rb') as f1 , io.open(loglocation+'/result.log','a+',encoding='utf-8') as f2:
        try:
            target0=""
            Subject = re.findall(re.compile(r'Subject.*|From.*|To.*'), f1.read())
            for i in range(len(Subject)):
                target0 = re.findall(target_r,Subject[i])[0]
        except:
            pass
        if (target0!=""):
            f2.writelines(u'[-]Appeared at the message header in '+file_path+'\n')

def search_content(file_path, target):
    with io.open(file_path,'rb') as f1 , io.open(loglocation+'/result.log','a+',encoding='utf-8') as f2:
        content=quopri.decodestring(f1.read())
        result=re.findall(target_r,content)[0]
        print result
        if (result!=""):
            f2.writelines(u'[-]Appeared at the message content in '+file_path+'\n')

target_file_list = [] 

for i in file_path_list:
    list_targetfile(i, target)
         
def f0():
    for i in target_file_list:
        f = io.open(loglocation+'/result.log','a+',encoding='utf-8')
        f.writelines(u'%s'%i+'\n') 
        f.writelines(u'\n')
        find_target(i,target)
        f.writelines(u'----------------------------------------------'+'\n')
        f.close()

def f1():   
    for i in target_file_list:
        f = io.open(loglocation+'/result.log','a+',encoding='utf-8')
        search_header(i,target)    
        f.close()

def f2():
    for i in target_file_list:
        f = io.open(loglocation+'/result.log','a+',encoding='utf-8')
        search_content(i,target)
        f.close()

if __name__ == '__main__':
    if (m0==0):
        f0()
    elif(m0==1):
        f1()
    else:
        f2()
    print("\n")

    print("[-]All over %s" %ctime())

