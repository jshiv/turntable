import os
import sys
import shutil
import json


path = os.getcwd()
package = path.split(os.sep)[-2]


def clean():

    if os.path.exists('./build'):
        shutil.rmtree('./build')


    if os.path.exists('./source/modules.rst'):
        os.system('rm ./source/modules.rst')

    if os.path.exists('./source/'+package+'.rst'):
        os.system('rm ./source/'+package+'*')






def main():

    clean()
    if os.path.exists('./source') == False:
        os.system('sphinx-quickstart')
    os.system('sphinx-apidoc -o ./source ../'+package+'')
    os.system('make html')




if __name__ == '__main__':
    main()