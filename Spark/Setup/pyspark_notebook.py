#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This scripts creates a pyspark profile and kernel, that are necessary to load a spark-context in an ipython-notebook. 
# To check everything is working, execute:
#   ipython console --profile=pyspark,
#   ipython notebook --profile=pyspark,
# for ipython-2.x and lower. For ipython-3.x and gretaer use
#   ipython notebook
# In the notebook, you can change the kernel dynamically (right now, between the pyspark kernel and the usual python kernel).
# If you have installed juoyter locally (not only in the browser) you can use jupyter instead of ipython.

# See https://github.com/felixcheung/vagrant-projects,
# http://ramhiser.com/2015/02/01/configuring-ipython-notebook-support-for-pyspark/ and 
# http://thepowerofdata.io/configuring-jupyteripython-notebook-to-work-with-pyspark-1-4-0/.

# TODO: 

import getpass
import glob
import inspect
import os
import platform
import re
import subprocess
import sys
import time
import json 
from shutil import rmtree

#-----------------------
# PySpark
#

master = 'local[*]'

driver_memory = '4g'

os.umask(0077)  # ensure that always chmod go-wrx

pyspark_submit_args = os.getenv('PYSPARK_SUBMIT_ARGS', None)
if not pyspark_submit_args:
    pyspark_submit_args = ' --driver-memory %s' % (driver_memory)
pyspark_submit_args = ' --master %s %s' % (master, pyspark_submit_args)

# Change in spark-1.4 and higher:
spark_home = os.getenv('SPARK_HOME', None)
spark_release_file = spark_home + "/RELEASE"
if os.path.exists(spark_release_file) and ("Spark 1.4" in open(spark_release_file).read() or "Spark 1.5" in open(spark_release_file).read()):
    if not "pyspark-shell" in pyspark_submit_args: pyspark_submit_args += " pyspark-shell"


if not os.getenv('PYSPARK_PYTHON', None):
    os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON']='ipython' # PySpark Driver (ie. IPython)
profile_name = 'pyspark'
os.environ['PYSPARK_DRIVER_PYTHON_OPTS'] = 'notebook --profile=%s' % profile_name

#-----------------------
# IPython Notebook
#

ipython_notebook_config_template = '''c = get_config()
c.NotebookApp.ip = '{ip}'
c.NotebookApp.port = {port}
c.NotebookApp.open_browser = False
'''

pyspark_setup = '''import os, sys

spark_home = os.getenv('SPARK_HOME', None)
if spark_home:
    print 'Using $SPARK_HOME'
    sys.path.insert(0, spark_home + "/python")

    # Add the py4j to the path. Not needed if you install py4j: pip install py4j
    # If not installed, you may need to change the version number to match your install
    sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.8.2.1-src.zip'))

    os.environ['PYSPARK_SUBMIT_ARGS'] = '{pyspark_submit_args}'
    # Initialize PySpark to predefine the SparkContext variable 'sc'
    # sys.argv = ['{pyspark_submit_args}']
    execfile(os.path.join(spark_home, 'python/pyspark/shell.py'))
elif 'spark' in os.getenv('PATH'):
    os.system('pyspark {pyspark_submit_args}')
else:
    raise ValueError('SPARK_HOME environment variable is not set and binaries are not added to the PATH')
'''.format(pyspark_submit_args = pyspark_submit_args)

ip = 'localhost' # Warning: this is potentially insecure
port = 8081

jupyter_kernel = {
  'display_name': 'PySpark',
  'language': 'python',
  'argv': [
    'python',
    '-m',
    'IPython.kernel',
    '--profile=pyspark',
    '-f',
    '{connection_file}'
  ],
  'env': {
  'PYSPARK_SUBMIT_ARGS': pyspark_submit_args
 }
}
jupyter_kernel = json.dumps(jupyter_kernel)


#-----------------------
# Create profile and start
#

try:
    ipython_path                 = os.popen('ipython locate').read().rstrip('\n')
    ipython_profile_path         = ipython_path + '/profile_%s' % profile_name
    setup_py_path                = ipython_profile_path + '/startup/00-pyspark-setup.py'
    ipython_notebook_config_path = ipython_profile_path + '/ipython_notebook_config.py'
    ipython_kernel_config_path   = ipython_profile_path + '/ipython_kernel_config.py'
    jupyter_kernel_dir           = ipython_path + '/kernels/pyspark'
    jupyter_kernel_config_path   = jupyter_kernel_dir + '/kernel.json'

    rmtree(ipython_profile_path, ignore_errors = True)	
    rmtree(jupyter_kernel_dir, ignore_errors = True)
	
    if not os.path.exists(ipython_profile_path):
        print 'Creating IPython Notebook profile\n'
        cmd = 'ipython profile create %s' % profile_name
        os.system(cmd)
        print '\n'

    if not os.path.exists(setup_py_path):
        print 'Writing PySpark setup\n'
        setup_file = open(setup_py_path, 'w')
        setup_file.write(pyspark_setup)
        setup_file.close()
        os.chmod(setup_py_path, 0600)

    # matplotlib inline
    kernel_config = open(ipython_kernel_config_path).read()
    if "c.IPKernelApp.matplotlib = 'inline'" not in kernel_config:
        print 'Writing IPython kernel config\n'
        new_kernel_config = kernel_config.replace('# c.IPKernelApp.matplotlib = None', "c.IPKernelApp.matplotlib = 'inline'")
        kernel_file = open(ipython_kernel_config_path, 'w')
        kernel_file.write(new_kernel_config)
        kernel_file.close()
        os.chmod(ipython_kernel_config_path, 0600)

    if not os.path.exists(ipython_notebook_config_path) or 'open_browser = False' not in open(ipython_notebook_config_path).read():
        print 'Writing IPython Notebook config\n'
        config_file = open(ipython_notebook_config_path, 'w')
        config_file.write(ipython_notebook_config_template.format(ip = ip, port = port))
        config_file.close()
        os.chmod(ipython_notebook_config_path, 0600)

    # jupyter kernel    
    if not os.path.exists(jupyter_kernel_config_path):
        print 'Creating Jupyter Notebook kernel config\n'
        os.makedirs(jupyter_kernel_dir)
        config_file = open(jupyter_kernel_config_path, 'w')
        config_file.write(jupyter_kernel)
        config_file.close()
        os.chmod(jupyter_kernel_config_path, 0600)

except KeyboardInterrupt:
    print 'Aborted\n'
    sys.exit(1)
