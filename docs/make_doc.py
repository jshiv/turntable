import os
import sys
import shutil
import sphinx
import argparse
import subprocess
from vinyl import utils

def clean():

    if os.path.exists('./_build'):
        shutil.rmtree('./_build')

    if os.path.exists('./generated'):
        shutil.rmtree('./generated')

    if os.path.exists('./Modulelist.rst'):
        os.system('rm ./Modulelist.rst')

def find_new_functions (module=None):

	modulelist = open('Modulelist.rst')
	strmodulelist = modulelist.read()
	modulelist.close()
	pathlist = utils.scanPath(root='../turntable/',pattern='*.py')

	for filename in pathlist:
		modulename = 'turntable.'+filename.split('/')[2].split('.')[0]
		strline = '.. automodule:: ' + modulename +'\n'
		if (module==None) or (module==modulename):
			flag = True
		else:
			flag = False 
		if (strline in strmodulelist) and flag: 
			print modulename
			idx = strmodulelist.find(strline)
			interpart = strmodulelist[idx:]
			idx2 = interpart.find('generated')
			interpart = interpart[idx2+12:]
			interpart = interpart.split('\n')
			fun_list = interpart[:interpart.index('')]
			fun_list = [el.split('\t')[-1] for el in fun_list]
			modulefile = open(filename)
			modulefilelst = modulefile.readlines()
			for line in modulefilelst:
				if line.replace(' ','').replace('\t','')[:1] in ['#','']:
					pass
				else: 
					if line[:3]=='def':
						func_name = line.split(' ')[1].split('(')[0]
						if func_name not in fun_list:
							print 'Found function to add: '+func_name
							modulelist = open('Modulelist.rst')
							tempmodulelist = open('tempmodulelist.rst','w')
							tempmodulelist2 = open('tempmodulelist2.rst','w')
							i=0
							for line2 in modulelist:
							    if i<5:
							        tempmodulelist.write(line2)
							    if line2==strline:
							        i = 1
							    if i>=1 and line2=='\n':
							        i+=1
							    if i==5 and line2!='\n':
							        tempmodulelist.write(line2)
							    if i==6 or line2=='':
							        tempmodulelist.write('\t'+func_name+'\n')
							        i = 7
							    if i>6:
							        tempmodulelist2.write(line2)
							if i==5:
								tempmodulelist.write('\t'+func_name+'\n')
							modulelist.close()
							tempmodulelist.close()
							tempmodulelist2.close()
							modulelist = open('Modulelist.rst','w')
							tempmodulelist = open('tempmodulelist.rst','r')
							tempmodulelist2 = open('tempmodulelist2.rst','r')
							modulelist.write(tempmodulelist.read()+tempmodulelist2.read())
							modulelist.close()
							tempmodulelist.close()
							tempmodulelist2.close()

	if os.path.exists('tempmodulelist.rst'):
		os.system('rm tempmodulelist.rst')
	if os.path.exists('tempmodulelist2.rst'):
		os.system('rm tempmodulelist2.rst')

def find_new_modules(filter=None):

	if filter==None:
		filter = []

	if os.path.exists('Modulelist.rst'):
		modulelist = open('Modulelist.rst')
		strmodulelist = modulelist.read()
		modulelist.close()
	else:
		strmodulelist = []
		modlist = open('Modulelist.rst', 'w')
		modlist.write('Module List\n===========\n')
		modlist.close()
	pathlist = utils.scanPath(root='../turntable/',pattern='*.py')
	for filename in pathlist:
		modulename = 'turntable.'+filename.split('/')[2].split('.')[0]
		strline = '.. automodule:: ' + modulename +'\n'
		if (strline not in strmodulelist) and ((modulename in filter) or (filter==[])) : 
			print 'Found module to add: ' + modulename
			tempmodulelist = open('Modulelist.rst','a')
			strtemp = ('\n\n{modname} module\n{dash} \n\n'+
			           '.. automodule:: {modname}\n\n'+
			           '.. currentmodule:: {modname}\n\n'+
			           'Content\n'+
			           '~~~~~~~\n\n'+
			           '.. autosummary:: \n'+
			           '\t:toctree: generated\n\n')
			insert_dash = '-'*(len(modulename)+7)
			tempmodulelist.write(strtemp.format(modname=modulename,dash=insert_dash))
			tempmodulelist.close()
			find_new_classes(modulename)
			find_new_functions(modulename)


def find_new_classes(module=None):

	modulelist = open('Modulelist.rst')
	strmodulelist = modulelist.read()
	modulelist.close()
	pathlist = utils.scanPath(root='../turntable/',pattern='*.py')

	for filename in pathlist:
		modulename = 'turntable.'+filename.split('/')[2].split('.')[0]
		strline = '.. automodule:: ' + modulename +'\n'
		if (module==None) or (module==modulename):
			flag = True
		else:
			flag = False 
		if (strline in strmodulelist) and flag: 
			idx = strmodulelist.find(strline)
			interpart = strmodulelist[idx:]
			idx2 = interpart.find('generated')
			interpart = interpart[idx2+12:]
			interpart = interpart.split('\n')
			fun_list = interpart[:interpart.index('')]
			fun_list = [el.split('\t')[-1] for el in fun_list]
			modulefile = open(filename)
			modulefilelst = modulefile.readlines()
			modulefile.close()
			for line in modulefilelst:
				if line.replace(' ','').replace('\t','')[:1] in ['#','']:
					pass
				else:
					if line[:5]=='class':
						class_name = line.split(' ')[1].split(':')[0]
						if '(' in class_name:
							 class_name = class_name.split('(')[0]
						if class_name not in fun_list:
							print 'Found class to add: '+class_name
							modulelist = open('Modulelist.rst')
							tempmodulelist = open('tempmodulelist.rst','w')
							tempmodulelist2 = open('tempmodulelist2.rst','w')
							i=0
							for line2 in modulelist:
							    if i<5:
							        tempmodulelist.write(line2)
							    if line2==strline:
							        i = 1
							    if i>0 and line2=='\n':
							        i+=1
							    if i==5 and line2!='\n':
							        tempmodulelist.write(line2)
							    if i==6:
							        tempmodulelist.write('\t'+class_name+'\n')
							        i = 7
							    if i>6:
							        tempmodulelist2.write(line2)
							if i==5:
								tempmodulelist.write('\t'+class_name+'\n')

							modulelist.close()
							tempmodulelist.close()
							tempmodulelist2.close()
							modulelist = open('Modulelist.rst','w')
							tempmodulelist = open('tempmodulelist.rst','r')
							tempmodulelist2 = open('tempmodulelist2.rst','r')
							modulelist.write(tempmodulelist.read()+tempmodulelist2.read())
							modulelist.close()
							tempmodulelist.close()
							tempmodulelist2.close()

							idx = modulefilelst.index(line)
							methods = []
							for next_line in modulefilelst[idx+1:]:
								if next_line.replace(' ','').replace('\t','')[:1] in ['#','']:
									pass 
								else:
									if next_line[:3]=='def':
										break
									if 'def ' in next_line[:10]:
										method = next_line.split('def ')[-1].split('(')[0]
										if method[:2] != '__':
											methods.append(method)

							generate_class(modulename+'.'+class_name,methods)


	if os.path.exists('tempmodulelist.rst'):
		os.system('rm tempmodulelist.rst')
	if os.path.exists('tempmodulelist2.rst'):
		os.system('rm tempmodulelist2.rst')




def generate_class(classname,methods):

	if  not os.path.exists('./generated'):
		os.system('mkdir ./generated')

	strpath = './generated/{classname}.rst'
	mthdpath = './generated/{method}.rst'

	liststr = classname.split('.')
	modulename = liststr[0]+'.'+liststr[1]
	smallclassname = liststr[2]

	strtemp = ('{classname}\n'+
			   '{dash}\n\n'+
			   '.. currentmodule:: {modulename}\n\n'+
			   '.. autoclass:: {smallclassname}\n\n')

	mthdtemp = ('{method}\n'+
			   '{dash}\n\n'+
			   '.. currentmodule:: {modulename}\n\n'+
			   '.. automethod:: {smallclassname}.{smethod}\n')

	classpath = strpath.format(classname=classname)
	classpath = classpath.replace(' ','')
	classstring = strtemp.format(classname=classname,dash='='*len(classname),modulename=modulename,smallclassname=smallclassname)
	classfile = open(classpath, 'w')
	classfile.write(classstring)
	classfile.close()

	for method in methods:
		methodname = classname+'.'+method 
		methodpath = mthdpath.format(method=methodname)
		methodpath = methodpath.replace(' ','')
		methodstring = mthdtemp.format(method=methodname,dash='='*len(methodname),modulename=modulename,smallclassname=smallclassname,smethod=method)
		methodfile = open(methodpath, 'w')
		methodfile.write(methodstring)


def main():

	# Filter on modules to build the doc for
	mod_filter = ['turntable.mapper','turntable.press','turntable.utils']

	arglist = sys.argv
	if len(arglist) > 2:
		raise SystemExit("make.py allows maximum one option")
	elif len(arglist)==2:
		arg = arglist[1]
	else:
		arg=None

	if arg not in ['html','clean','add_functions','add_modules','add_classes','build']:
		raise SystemExit("Please choose one of the following options: \n"+
						 "  html: to build the html files\n"+
						 "  clean: to clean the generated files\n"+
						 "  add_functions: to look for new functions to add to the documentation\n"+
						 "  add_modules: to look for new modules to add to the documentation\n"+
						 "  add_classes: to look for new classes to add to the documentation\n"+
						 "  build: to build the generated files\n")

	if arg=='clean':
		print 'Cleaning...'
		clean()

	else: 
		# check version
		#proc = subprocess.Popen(["python", "../setup.py","--version"], stdout=subprocess.PIPE, shell=True)
		#(out, err) = proc.communicate()
		version = "0.2"
		conffile = open('conf.py')
		conftemp = open('conftemp.py', 'w')
		for line in conffile:
			if line[:7] in ['release','version']:
				writeline = line[:7]+" = '"+version+"'"+'\n'
				conftemp.write(writeline)
			else:
				conftemp.write(line)
		conffile.close()
		conftemp.close()
		os.system('rm conf.py')
		os.system('mv conftemp.py conf.py')
		
		proc = subprocess.Popen(["pip", "freeze"], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		listpack = out.split('\r\n')[1:-1]
		listpack = [el.split('==')[0] for el in listpack]

		# if "numpydoc" not in listpack:
		# 	i = 0
		# 	while i<5:
		# 		print ('numpydoc needs to be intalled to build the documentation properly.\n'+
		# 			          'Do you want to install numpydoc? [y/n] ')
		# 		ans = raw_input()
		# 		if ans=='y':
		# 			i=5
		# 			os.system('pip install numpydoc')		
		# 		elif ans=='n' or i==4:
		# 			raise SystemExit('Aborting build...\n'+'Building HTML failed')
		# 		else: 
		# 			print "Please enter 'y' for 'yes' or 'n' for 'no'"   
		# 			i+=1
		# else:
		# 	print ('numpydoc package found.')

		# if "sphinxcontrib-fulltoc" not in listpack:
		# 	i = 0
		# 	while i<5:
		# 		print ('\nsphinxcontrb-fulltoc needs to be intalled to build the documentation properly.\n'+
		# 	          'Do you want to install sphinxcontrib-fulltoc? [y/n] ')
		# 		ans = raw_input()
		# 		if ans=='y':
		# 			os.system('sudo pip install sphinxcontrib-fulltoc') 
		# 			i=5
		# 		elif ans=='n' or i==4:
		# 			raise SystemExit('Aborting build...\n'+'Building HTML failed')
		# 		else: 
		# 			print "Please enter 'y' for 'yes' or 'n' for 'no'"   
		# 			i+=1
		# else:
		# 	print ('sphinxcontrib-fulltoc package found.')


		proc = subprocess.Popen(["latex", "-version"], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		listpack = out.split('\r\n')[1:-1]
		listpack = [el.split('==')[0] for el in listpack]

		if out[:7]=="'latex'":
			print ('Warning: latex needs to be intalled to build the documentation properly.\n'+
				   'You need to install a valid distribution of latex (Miktex on Windows) so the documentation is built properly.')


	if arg=='add_functions':
		find_new_functions()
		os.system('sphinx-autogen Modulelist.rst')
		if os.system('sphinx-build -b html ./ ./_build/html '):
		    raise SystemExit("Building HTML failed.")

	elif arg=='add_modules':
		find_new_modules(filter=mod_filter)
		os.system('sphinx-autogen Modulelist.rst')
		if os.system('sphinx-build -b html ./ ./_build/html '):
		    raise SystemExit("Building HTML failed.")

	elif arg=='add_classes':
		find_new_classes()
		os.system('sphinx-autogen Modulelist.rst')
		if os.system('sphinx-build -b html ./ ./_build/html '):
		    raise SystemExit("Building HTML failed.")

	elif arg=='html':
		print 'Cleaning...'
		clean()
		find_new_modules(filter=mod_filter)
		find_new_functions()
		find_new_classes()
		os.system('sphinx-autogen Modulelist.rst')
		if os.system('sphinx-build -b html ./ ./_build/html '):
		    raise SystemExit("Building HTML failed.")

	elif arg=='build':
		if os.system('sphinx-build -b html ./ ./_build/html '):
			raise SystemExit("Building HTML failed.")


if __name__ == '__main__':
	import sys
	sys.exit(main())