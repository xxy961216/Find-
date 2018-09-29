import os
 
#根据文件扩展名判断文件类型
def endWith(s,*endstring):
    array = map(s.endswith,endstring)
    if True in array:
        return True
    else:
        return False
 
#将全部已搜索到的关键字列表中的内容保存到result.log文件
def writeResultLog(allExistsKeywords):
    #行分隔符
    ls = os.linesep
    #结果日志文件名
    logfilename = "result.log" #相对路径,文件在.py文件所在的目录中
    try:
        fobj = open(logfilename,'w')
    except:
        pass

    else:
        fobj.writelines(['%s%s' % (keyword,ls) for keyword in allExistsKeywords])
        fobj.close()    
 
 
#搜索指定关键字是否在指定的文件中存在
def searchFilesContent(dirname):
    #从searchkeywords.txt文件中初始化待搜索关键字列表
    filename = "searchkeywords.txt" #相对路径,文件在.py文件所在的目录中
    #待搜索关键字列表
    allSearchKeywords=[]
    #遍历文件当前行已搜索到的关键字列表
    existsKeywordsThisLine=[]
    #全部已搜索到的关键字列表
    allExistsKeywords=[]
 
    try:
        fobj = open(filename,'r');
    except:
        pass

    else:
        for eachLine in fobj:
            allSearchKeywords.append(eachLine.strip('\n')); #使用strip函数去除每行的换行符
        fobj.close();
 
    #从excludekeywords.txt文件中初始化要排除的搜索关键字列表
    filename = "excludekeywords.txt" #相对路径,文件在.py文件所在的目录中
    #要排除的搜索关键字列表
    allExcludedKeywords=[]
    try:
        fobj = open(filename,'r');
    except:
        pass
    else:
        for eachLine in fobj:
            allExcludedKeywords.append(eachLine.strip('\n')); #使用strip函数去除每行的换行符
        fobj.close();
 
    #从全部已搜索到的关键字列表排除掉不用搜索的关键字
    for excluedkw in allExcludedKeywords:
        if(excluedkw in allSearchKeywords):
            allSearchKeywords.remove(excluedkw);
 
 
    #遍历打开所有要在其中搜索内容的文件，若待搜索关键字列表为空，则不再继续遍历
    for root,dirs,files in os.walk(dirname):
        for file in files:
            if endWith(file,'.java','.xml','.properties'): #只在扩展名为.java/.xml/.properties文件中搜索
                #打开文件
                filename = root + os.sep + file #绝对路径
                filename = filename.replace("\\","\\\\") #将路径中的单反斜杠替换为双反斜杠，因为单反斜杠可能会导致将路径中的内容进行转义了，replace函数中"\\"表示单反斜杠，"\\\\"表示双反斜杠
                try:
                    fobj = open(filename,'r');
                except:
                    pass
                else:
                    #遍历文件的每一行
                    for fileLine in fobj:
                        #判断当前行是否包含所有搜索关键字
                        for keyword in allSearchKeywords:
                            #若包含，并添加到该行已搜索到的关键字列表中
                            if keyword.upper() in fileLine.upper(): #将搜索关键字和该行文本内容都转换为大写后再进行匹配
                                existsKeywordsThisLine.append(keyword)
 
                        #将这些搜索到的关键字添加到全部已搜索到的关键字列表中，并包含文件名信息
                        for keyword in existsKeywordsThisLine:
                            allExistsKeywords.append(keyword+"\t"+filename.replace("\\\\","\\"))
 
                        #将这些搜索到的关键字从待搜索关键字列表中移除（后续将不再搜索该关键字）
                        for keyword in existsKeywordsThisLine:
                            allSearchKeywords.remove(keyword)
 
                        #清空该行已搜索到的关键字列表内容
                        existsKeywordsThisLine = []
 
                        #若所有的关键字都搜索到了，则记录日志文件，并结束搜索工作
                        if len(allSearchKeywords)==0:
                            fobj.close();
                            writeResultLog(allExistsKeywords)
                            print ("DONE!")
                            return
                    fobj.close();
 
    #全部文件遍历结束
    writeResultLog(allExistsKeywords)
    print ("DONE!")
 
 
 
#仅当本python模块直接执行时，才执行如下语句，若被别的python模块引入，则不执行
if __name__ == '__main__':
    searchFilesContent(r"G:\ccsSmartPipe\SmartPipe\src\java")