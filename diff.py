import difflib
import sys
import fileinput
import os
import contextlib


#diff.py
#to find any difference between html sources
#written by kwp

def main():
    if len(sys.argv) >=3:
    	folder1 = sys.argv[1]
    	folder2 = sys.argv[2]
    else:
	print 'Usage: python diff.py name_of_folder1 name_of_folder2\r'
	print 'Usage: python diff.py aaa.sqlite bbb.sqlite\r'
	return

    if '.sqlite' in sys.argv[1]:
	print 'Comparing two sqlite files...'
	_diff(os.getcwd()+'/'+str(folder1),os.getcwd()+'/'+str(folder2))
    else:
    	concat_sources(folder1)
    	concat_sources(folder2)
    	_diff(os.getcwd()+'/'+str(folder1)+'/'+str(folder1)+'.html',os.getcwd()+'/'+str(folder2)+'/'+str(folder2)+'.html')
    

def concat_sources(folder):

	try:
		os.remove(os.getcwd()+'/'+str(folder)+'/'+str(folder)+'.html')
	except OSError:
		pass
	
	path = os.path.join(os.getcwd(),folder)
	html_files= []
	for root,dirs,files in os.walk(path):
		for file in files:
			if file.endswith(".html"):
				html_files.append(os.path.join(root,file))
		break
	#print (html_files)

	

	temp_file = open(os.getcwd()+'/'+str(folder)+'/'+str(folder)+'.html','w')
	print(os.getcwd()+'/'+str(folder)+'/'+str(folder)+'.html'+ ' has been created')

	allfiles = fileinput.input(html_files)

	for line in allfiles:
   		temp_file.write(line)
	temp_file.close()
	return

    
def _diff(file1 , file2):
	diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())
	with open('result.txt','w') as f:
		f.write(''.join(diff),)
	
	print('result.txt has been created')
	
	return


if __name__ == '__main__':
     main()




