import time
start=time.time()
import os
from bs4 import BeautifulSoup
import requests
import threading
import csv

#The code reads an input file
#First line contains a number N - total test cases 
#followed by 2n lines; 2 for each test case.
#First line containing file name with their extension and second line containing directory of file.

#Alternatively comment out the next 2 lines to give manual input in order - No. of test cases,file name with extension,file directory
import sys
sys.stdin = open('input.txt','r')

#Get Input file's extension
def get_ext():
	fileName=input()
	#Raise Error if file does not contain an extension
	if(fileName.find(".")==-1):	
		#raise NameError("File Type Not Found")
		print("File missing extension")
	
	fileName=fileName.split(".")
	return fileName

#get cwd info of input file
def get_dir():
	#directory=os.getcwd()
	directory=input()
	directory=directory.split("\\")
	return directory[-1]

#web-Scraping ,Formatting our data and put it in a list for ease of operations
def get_info(ext):
	global info,lock
	lock.acquire()
	page=requests.get('https://www.fileinfo.com/extension/'+str(ext))
	soup=BeautifulSoup(page.text,'html.parser')

	headerInfo=soup.find(class_='headerInfo')
	info=[]
	#error handling
	try:
		headerInfo.div.decompose()
	except AttributeError:
		print("File type information not found")
		for i in range(7):
			info.append("Null")
		lock.release()
		return
	headerInfo=headerInfo.find_all('td')
	for item in headerInfo:
		if(item.text =='Popularity'):
			item.decompose()
		if(item.find('div',class_='formatx')):
			item.div.div.decompose()
			item.h4.decompose()
		info.append(item.text)

	info.__delitem__(3)
	info.__delitem__(2)

	temp=info[-1]
	temp=temp.split("\n\n\n\n")
	info.__delitem__(-1)
	[info.append(temp[i].strip('\n')) for i in range(len(temp))]
	lock.release()

#Takes directory as input and returns the associated file type
def dir_info(dir_list):
	global info2,lock
	lock.acquire()
	file_dir=get_dir()
	for i in dir_list:
		if i[0]==file_dir.lower():
			info2=[file_dir,i[1]]
			lock.release()
			return
	info2=[file_dir,"No Info Found"]
	lock.release()


#Write the output in a CSV file
fileType=csv.writer(open('output.csv','w'))
fileType.writerow(['File Name','Developer','Category','Format','Remarks',"Directory",'Directory Info'])


#Threading is implemented to gather data from different sources together to save time.
def writeData(fileType):
	cases=int(input())
	for i in range(cases):
		global info,lock,info2
		lock = threading.Lock()
		ext=get_ext()
		thread1=threading.Thread(target=get_info(ext[-1]))
		thread2=threading.Thread(target=dir_info(dir_list))
		thread1.start()
		thread2.start()
		thread1.join()
		thread2.join()
		details=info[:]
		fileType.writerow([ext[0]+"."+ext[-1]]+[details[i] for i in (1,3,5,6)]+info2)
		print("File",i+1,"classification complete.")

#A quick hack to replace a database file to reduce run time.
#The data was less, so this option seemed feasible
dir_list=[['bin','Contains all the binary files'],
['boot','Contains master boot records, sector/system map files and boot files'],
['dev','Contains common device file types'],
['etc','Contains all system related configuration files'],
['home','Contains personal configuration files (Dotfiles)'],
['initrd','Contains root files'],
['lib','Contains kernel modules and shared library images'],
['lost+found Contains corrupt and broken files '],
['media','Contains mount points for removable media'],
['mnt','Contains moint points or sub directories where the user can mount floppy or disk'],
['opt','Reserved for third party software installations'],
['proc','Contains runtime system information'],
['root','All the files and subdirectories originate from here.'],
['sbin','Contains only the binaries essential for booting, restoring, and repairing the system'],
['usr','Contains all the user binary files, their documentation, libraries etc'],
['var','Contains variable data like system logging files, mail and printer spool direcories.'],
['srv','Contains site specific data which is served by the system'],
['tmp','Contains file that are required temporarily to the system ']]


print("File type identification using file extension and file directory.")
print("Using web scraping from fileinfo.com and a local database of file directories.\n")
writeData((fileType))

#Measure Time taken to analyse all files
end=time.time()
print("Execution Complete.")
print("Please check CSV file generated in the containing folder to view output.")
print("Elapsed Time",end-start,"seconds")
