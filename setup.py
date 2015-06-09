import argparse
import subprocess
import os
import sys
current_directory = os.getcwd()

stablecommit = "9a72a59b694ce9a4599a01d59e90a03ffc0dcf82"

def runTerminal(cmd):
	subprocess.call(cmd, shell=True)

def remove():
	runTerminal("rm -rf lammps")
	runTerminal("make clean")

def cloneLammps(head):
	runTerminal("git clone https://github.com/lammps/lammps.git")
	if not head:
		os.chdir("./lammps")
		runTerminal("git reset --hard "+stablecommit)
		os.chdir(current_directory)

def updateLammps():
	os.chdir("./lammps")
	runTerminal("git reset --hard HEAD")
	runTerminal("git pull")
	os.chdir(current_directory)
	
def cleanPackages():
	os.chdir("./lammps/src")
	runTerminal("make no-all")
	os.chdir(current_directory)

def activatePackage(package):
	os.chdir("./lammps/src")
	runTerminal("make yes-"+package)
	os.chdir(current_directory)

def standardPackages():
	cleanPackages()
	activatePackage("mc")
	activatePackage("molecule")

def compile():
	makeStyles()
	runTerminal("cp lammpscontroller.cpp lammps/src")
	runTerminal("cp lammps/src/STUBS/mpi.c lammps/src/mpi.cpp")
	runTerminal("make -j 8")

def makeStyles():
	os.chdir("./lammps/src")
	runTerminal("/bin/bash Make.sh style")
	os.chdir(current_directory)

helpstr = "LAMMPS web compiler v 0.99.\n" + \
	"LAMMPS Github repository: https://github.com/lammps/lammps\n" + \
	"Example commands:\n" + \
	"  python setup.py install --packages none\n" + \
	"  python setup.py install --head --packages standard\n" + \
	"\n" + \
	"or run 'python setup.py --help' for more information. \n"

lammpsdirExists = os.path.isdir("./lammps")

parser = argparse.ArgumentParser(description=helpstr, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("command", help="command can be one of the following: 'install', 'clone', 'update', 'remove', 'cleanpackages'")
parser.add_argument('-p','--packages', nargs='*', help='LAMMPS packages ("-p none" for no packages, or provide a list of packages.)', required=False)
parser.add_argument('--head', help='clone newest version at head commit. WARNING, this might not compile.', required=False, action='store_true')

if len(sys.argv) == 1:
	print helpstr

args = parser.parse_args()
command = args.command

print "Packages: ", args.packages

if not command in ["install", "clone", "update", "remove", "cleanpackages"]:
	print "Error, '"+command+"' is not a valid command. Must be one of 'install', 'update', 'remove'"
	exit()

if command == "remove":
	remove()
	exit()

if command == "cleanpackages":
	cleanPackages()
	exit()

if command == "clone":
	cloneLammps()

if command == "update":
	if not lammpsdirExists: cloneLammps(True)
	updateLammps()

if command == "install":
	if not lammpsdirExists: cloneLammps(args.head)
	if args.head == False:
		updateLammps()
	
	if not args.packages is None:
		if args.packages[0] == "none": cleanPackages()
		else:
			for package in args.packages:
				activatePackage(package)
	else: standardPackages()

	compile()