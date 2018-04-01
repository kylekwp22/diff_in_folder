import difflib
import sys
import fileinput
import os

#diff.py
#to find any difference between html sources

def main():
    if len(sys.argv) >=3:
    	folder1 = sys.argv[1]
    	folder2 = sys.argv[2]
    else:
	print 'Usage: python diff.py -folder1 -folder2'
	return

    concat_sources(folder1)
    concat_sources(folder2)
    _diff(os.getcwd()+'/'+str(folder1)+'/'+str(folder1)+'.html',os.getcwd()+'/'+str(folder2)+'/'+str(folder2)+'.html')
    

def concat_sources(folder):
	
	path = os.path.join(os.getcwd(),folder)
	html_files= []
	for root,dirs,files in os.walk(path):
		for file in files:
			if file.endswith(".html"):
				html_files.append(os.path.join(root,file))
		break
	print (html_files)

	temp_file = open(os.getcwd()+'/'+str(folder)+'/'+str(folder)+'.html','w')
	print(os.getcwd()+'/'+str(folder)+'/'+str(folder)+'.html'+ ' has been created')

	allfiles = fileinput.input(html_files)

	for line in allfiles:
   		temp_file.write(line)
	temp_file.close()
	return

    
def _diff(file1 , file2):
	diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())
	print ''.join(diff),
	return


if __name__ == '__main__':
     main()




