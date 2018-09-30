import os


file_path = input('Please enter the directory path you want to explore: ')
target = input('please enter the key word you want to find: ')


 


def file_location(file_path):                                  
    os.chdir(file_path)
    content_list = os.listdir(os.curdir)
    for each in content_list:
        if os.path.splitext(each)[1] == '.msg':
            file_path_list.append(os.getcwd() + os.sep + each)
        if os.path.isdir(each):                                #递归引用

            file_location(each)
            os.chdir(os.pardir)

file_path_list = []
file_location(file_path)                                       #目标文件路径存放至列表


def list_targetfile(file_path, target):                        #定义寻找内容中包含关键字的文件
    f = open(file_path,encoding='utf-8')
    count_list = []
    for each_line in f:
        count = each_line.count(target)
        count_list.append(count)
    if count_list.count(0) != len(count_list):
        target_file_list.append(file_path)
    f.close()


def find_target(file_path, target):
    logfilename = "result.log"                           #定义寻找文件中的关键字行数以及在该行中的位置
    f = open(file_path,encoding='utf-8')
    f1 = open(logfilename,'w')
    line_number = 1
    for each_line in f:
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
            print('Appeared at the %scharacter of line %d, totally %d times.' % (begin_str, line_number, count))    
            f1.writelines('Appeared at the %scharacter of line %d, totally %d times.' % (begin_str, line_number, count))
            
        line_number += 1
    f.close()
    f1.close()

target_file_list = []
for i in file_path_list:
    list_targetfile(i, target)                                 #获得内容中包含关键字的文件路径

for i in target_file_list:
    print(i)
    print()
    find_target(i, target)
    print('----------------------------------------------')
