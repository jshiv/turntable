import os
import sys
import shutil


def clean():

    if os.path.exists('./build'):
        shutil.rmtree('./build')


    if os.path.exists('./source/modules.rst'):
        os.system('rm ./source/modules.rst')

    if os.path.exists('./source/turntable.rst'):
        os.system('rm ./source/turntable*')






def main():

	clean()
	os.system('sphinx-apidoc -o ./source ../turntable')
	os.system('make html')




if __name__ == '__main__':
	main()