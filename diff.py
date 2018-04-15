import difflib
import sys
import fileinput
import os
import contextlib
import re
import os
import errno
import requests
import shutil
#import jsbeautifier
import unicodedata
import codecs
#import unidecode
import subprocess

#diff.py
#to find any difference between html sources
#written by kwp


download_js = False



def main():
    if len(sys.argv) >=3:
    	folder1 = sys.argv[1]
    	folder2 = sys.argv[2]
    else:
	print 'Usage: python diff.py name_of_the_folder1 name_of_the_folder2\r'
	#print 'Usage: python diff.py aaa.html bbb.html\r'
	return

    if '.sqlite' in sys.argv[1] and '.sqlite' in sys.argv[2]:
	print 'Comparing two sqlite files...'
	_diff(os.getcwd()+'/'+str(folder1),os.getcwd()+'/'+str(folder2))
    elif '.html'in sys.argv[1] and '.html' in sys.argv[2]:
	print 'Comparing two html files...'
	_diff(os.getcwd()+'/'+str(folder1),os.getcwd()+'/'+str(folder2))
    #elif len(sys.argv) >=4 and sys.argv[3] == '-c':
	#change_html_name(folder1)
	#change_html_name(folder2)
	#concat_sources(folder1,'home')
    	#concat_sources(folder2,'public_wifi')
    	#diff(os.getcwd()+'/'+str(folder1)+'/'+str(folder1)+'/'+str(folder1)+'.html',os.getcwd()+'/'+str(folder2)+'/'+str(folder2)+'/'+str(folder2)+'.html')	
    else:
	if len(sys.argv) >=4 and sys.argv[3] == '-js':
		print("download js enabled")
		global download_js
		download_js = True
	print 'recursive_diff'
	print(folder1)
	print(folder2)
	change_html_name(folder1)
	change_html_name(folder2)
    	_recursive_diff_detail(folder1,folder2)





def quote_html(s):
    '''Quote html special chars and replace space with nbsp'''
    def repl_quote_html(m):
        tokens = []
        quote_dict = {
            ' ': '&nbsp;',
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
        }
        for c in m.group(0):
            tokens.append(quote_dict[c])
        return ''.join(tokens)
    return re.sub('[ &<>"]', repl_quote_html, s)


def print_html(lines,output_txt):

    
    html_f = open(output_txt,'w')
    title = None
    q = quote_html
    html_f.write('<?DOCTYPE html?>\n')
    html_f.write('<html>\n')
    html_f.write('<head>\n')
    html_f.write('<meta http-equiv="Content-Type" content="text/html; charset={}">\n'
            .format(q('utf-8')))
    if title is not None:
        html_f.write('<title>{}</title>\n'.format(q('')))
    html_f.write('''
        <style>
            span.diffcommand { color: teal; }
            span.removed     { color: red; }
            span.inserted    { color: green; }
            span.linenumber  { color: purple; }
        </style>
    ''')
    html_f.write('</head>\n')
    html_f.write('<table>\n')
    html_f.write('<tbody>\n<tr>')
    for line in lines:
        if line.startswith('+++'):
            html_f.write(q(line)+'\n')
        elif line.startswith('---'):
            html_f.write(q(line)+'\n')
        elif line.startswith('+'):
            html_f.write('<span class="inserted">{}</span>\n'.format(q(line)))
        elif line.startswith('-'):
            html_f.write('<span class="removed">{}</span>\n'.format(q(line)))
        elif line.startswith('diff'):
            html_f.write('<span class="diffcommand">{}</span>\n'.format(q(line)))
        else:
            m = re.match(r'^@@.*?@@', line)
            if m:
                num = m.group(0)
                rest = line[len(num):]
                html_f.write('</tr><span class="linenumber">{}</span>{}\n<tr>'
                            .format(q(num), q(rest)))
            else:
                html_f.write(q(line))
        html_f.write('<br />\n')
    html_f.write('</tr></tbody>\n')
    html_f.write('</table>\n')
    html_f.write('</body>\n')
    html_f.write('</html>\n')








def generate_js(index,js_contents):
	filename = "./js_files/"+index+".js"
	

	if not os.path.exists(os.path.dirname(filename)):
	    try:
		os.makedirs(os.path.dirname(filename))
	    except OSError as exc: # Guard against race condition
		if exc.errno != errno.EEXIST:
		    raise

	with open(filename, "w") as f:
	    f.write(js_contents)

	return

def change_html_name(folder):
	path = os.path.join(os.getcwd(),folder)
	html_files= []
	if os.path.isdir(os.path.join('./',folder+'/'+folder)):
		shutil.rmtree(os.path.join('./',folder+'/'+folder))
	
	for root,dirs,files in os.walk(path):
		for file in files:
			if file.endswith(".html"):
				#html_files.append(os.path.join(root,file))
				content = open(os.path.join(root,file),'r').read()
				#res = jsbeautifier.beautify(content.replace(u'\u2019',u'\''))
				#print(content)	
				js_list=re.findall(r'<title>(.*)</title>',content)
				#print(os.path.join(root,file))
				if len(js_list)>=1:
					if not os.path.isdir(os.path.join(root,folder)):
					    print('Creating new folder')
					    os.makedirs(os.path.join(root,folder))
					shutil.copy(os.path.join(root,file),os.path.join(root,folder+'/'+file[0]+ file[1]+' - '+js_list[0][0:25].replace('/','_')+'.html'))
					'''
					res = jsbeautifier.beautify_file(os.path.join(root,folder+'/'+file[0]+' - '+js_list[0][0:25]+'.html'))
					f = open(os.path.join(root,folder+'/'+file[0]+' - '+js_list[0][0:25]+'clean.html'),'w')
					
					f.write(res.encode('utf-8'))
					'''
		break
	return 

def get_html_files(folder):
	path = os.path.join(os.getcwd(),folder+'/'+folder)
	print(path)
	html_files= []
	for root,dirs,files in os.walk(path):
		for file in files:
			if file.endswith(".html"):
				html_files.append(os.path.join(root,file))
		break
	#print (html_files)
	return html_files
	

def concat_sources(folder,my_string):
	temp_name =os.getcwd()+'/'+str(folder)+'/'+str(folder)+'/'+str(folder)+'.html'
	#result_name = os.getcwd()+'/'+str(folder)+'/'+str(folder)+'_clean.html'
	try:
		os.remove(temp_name)
	except OSError:
		pass
	html_files = get_html_files(folder)
	


	temp_file = open(temp_name,'w')
	print(temp_name+'.html'+ ' has been created')

	allfiles = fileinput.input(html_files)
	index_track = 0
	for line in allfiles:
		if line.startswith('<html'):
			temp_file.write('\r\n')
			temp_file.write('\r\n')
			temp_file.write('**************'+my_string+'***************Start of the file ' + html_files[index_track] + ' *****************************')
			index_track+=1
   		temp_file.write(line)
	temp_file.close()
	
	
	
	return


    
def _diff(file1 , file2):
	html_f = open('result.html','w')
	diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())
	with open('result.txt','w') as f:
		f.write('\r\n'.join(x[0:] for x in diff if re.match(r'=\"([^\"]*\.js[^\"]*)\"',x)),)
	
	print('result.txt has been created')
	file1_lines = open(file1,'r').readlines()
	file2_lines = open(file2,'r').readlines()
		

	html_diff = difflib.HtmlDiff(tabsize=8).make_file(file1_lines,file2_lines,file1,file2,context=True,numlines=3)
	html_f.write(html_diff)
	

	_make_js_list()
	
	
	return



def _make_js_list():
	js_txt = open('js_result.txt','w')
	content = open('result.txt','r').read()	


	js_list=re.findall(r'=\"([^\"]*\.js[^\"]*)\"',content)

	for index,entry in enumerate(js_list) :
		#print("adding http to " +entry)
		if (not entry.startswith('http://') ) and (not entry.startswith('https://')) :
			if entry.startswith('//'):
				js_list[index] = 'http:'+js_list[index]
			elif entry.startswith('**'):
				js_list[index] = '\r\n'+js_list[index]+'\r\n'
			else:
				js_list[index] = 'http://'+js_list[index]
	


	js_txt.write('\r\n'.join(js_list))
	print('Job Completed, js_result.txt has been created\r\n')
	global download_js
	if download_js == True :
		if os.path.isdir('./js_files'):
		    print('Cleaning up previous js_files')
		    shutil.rmtree('./js_files')
		    #os.makedirs('./js_files')
		    
	
		for index, jscript in enumerate(js_list):
			try:
				r = requests.get(jscript,timeout=5)
				print("Downloading "+jscript+" now")
				generate_js(str(index)+'__'+os.path.basename(jscript),r.text)
			except requests.exceptions.RequestException as err:
				print("warning:", err)
				continue
			except:
				print("Some Encoding Error while downloading js")
				continue
	else:
		print('download_js disabled, enable (adding -js at the end )it to download js files')	

	return






def _recursive_diff_detail(folder1, folder2):

	html_files_folder1= get_html_files(folder1)
	html_files_folder2= get_html_files(folder2)
	
	
	#print ("\r\n")
	#print (len(html_files_folder1))
	#html_f = open('result.html','w')
	f = open('result.txt','w')
	'''
	if os.path.isdir('./result_html'):
		print('Cleaning up previous js_files')
		shutil.rmtree('./result_html')
	if not os.path.isdir('./result_html'):
		os.makedirs(os.path.join(os.getcwd(),'result_html'))
	'''
	#f.write(codecs.BOM)
	if len(html_files_folder1) == len(html_files_folder2):
		total_num_files = len(html_files_folder2)
		print(total_num_files)
		for x in range(total_num_files):
			
			print("Comparing "+ str(os.path.basename(html_files_folder1[x])) +"(file #1) and "+ str(os.path.basename(html_files_folder2[x]))+" (file #2) to see if any injected things inside the file #2.")
			f.write("\r\n\r\n")
			f.write("*=\"**[+][+][+]****Injected .js into*****"+str(os.path.basename(html_files_folder2[x]))+" from the public wifi ****\"*\r\n")
			f.write("\r\n")
			
			#file1_lines = open(html_files_folder1[x],'r').readlines()
			#file2_lines = open(html_files_folder2[x],'r').readlines()
			#print('diff "'+html_files_folder1[x]+'" "'+html_files_folder2[x]+'"')
			p = subprocess.Popen('diff -u "'+html_files_folder1[x]+'" "'+html_files_folder2[x]+'"',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			diffs = []	
			#print( p.stdout.readlines())	
			lines = p.stdout.readlines()	
			for line in lines:
				#print_html(lines,os.path.join(os.getcwd(),'result_html/'+'[result] -'+str(os.path.basename(html_files_folder2[x]))))
				diffs.append(line)
				#if line[0] in ('>'):
				#	diffs.append(line)
			retval = p.wait()

			
	

			if diffs:
				#print(diffs)
				f.write(''.join(diffs))
			else:
				f.write('\r\n no change')
			
			f.write("\r\n******************************************************************************************")
	else:
		print('# of files in folder1 and # of files in folder 2 do not match')
	f.close()

	#p = subprocess.Popen('cat result.txt | python diff2html.py -o result.html',shell=True)

	print_html(open('result.txt','r').readlines(),'result.html')
	_make_js_list()
	

	
	print('Job Completed, result.txt has been created')
	return



if __name__ == '__main__':
     main()




