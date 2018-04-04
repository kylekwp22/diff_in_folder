import difflib
import sys
import fileinput
import os
import contextlib
import re


#diff.py
#to find any difference between html sources
#written by kwp

def main():
    if len(sys.argv) >=3:
    	folder1 = sys.argv[1]
    	folder2 = sys.argv[2]
    elif len(sys.argv) >=4 and sys.argv[3] == '-r':
	print 'Using Recursive Method'
    else:
	print 'Usage: python diff.py name_of_folder1 name_of_folder2\r'
	print 'Usage: python diff.py name_of_folder1 name_of_folder2 -c (for massive concat & compare)\r'
	print 'Usage: python diff.py aaa.sqlite bbb.sqlite\r'
	print 'Usage: python diff.py aaa.html bbb.html\r'
	return

    if '.sqlite' in sys.argv[1] and '.sqlite' in sys.argv[2]:
	print 'Comparing two sqlite files...'
	_diff(os.getcwd()+'/'+str(folder1),os.getcwd()+'/'+str(folder2))
    elif '.html'in sys.argv[1] and '.html' in sys.argv[2]:
	print 'Comparing two html files...'
	_diff(os.getcwd()+'/'+str(folder1),os.getcwd()+'/'+str(folder2))
    elif len(sys.argv) >=4 and sys.argv[3] == '-c':
	concat_sources(folder1)
    	concat_sources(folder2)
    	_diff(os.getcwd()+'/'+str(folder1)+'/'+str(folder1)+'.html',os.getcwd()+'/'+str(folder2)+'/'+str(folder2)+'.html')
    else:
    	_recursive_diff(folder1,folder2)

def get_html_files(folder):
	path = os.path.join(os.getcwd(),folder)
	html_files= []
	for root,dirs,files in os.walk(path):
		for file in files:
			if file.endswith(".html"):
				html_files.append(os.path.join(root,file))
		break
	#print (html_files)
	return html_files
	

def concat_sources(folder):

	try:
		os.remove(os.getcwd()+'/'+str(folder)+'/'+str(folder)+'.html')
	except OSError:
		pass
	html_files = get_html_files(folder)
	

	

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
		f.write(''.join(x[0:] for x in diff if re.match(r"[+]\s*<script",x)),)
	
	print('result.txt has been created')
	
	return


def _recursive_diff(folder1, folder2):

	html_files_folder1= get_html_files(folder1)
	html_files_folder2= get_html_files(folder2)

	f = open('result.txt','w')
	if len(html_files_folder1) == len(html_files_folder2):
		for x in range(0,len(html_files_folder1)-1):
			f.write("\r\r\r\r")
			f.write("------------------Analyzing------------"+str(x)+"th .html file to see if any injected scripts exist--------------------------------------")
			f.write("\r\r")
			diff = difflib.ndiff(open(html_files_folder1[x]).readlines(),open(html_files_folder2[x]).readlines())
			f.write(''.join(x[0:] for x in diff if re.match(r"[+]\s*<script",x)),)
			f.write("------------------------------------------------------------------------------")
	else:
		print('# of files in folder1 and # of files in folder 2 do not match')	

	print('Job Completed, result.txt has been created')
	return


if __name__ == '__main__':
     main()




