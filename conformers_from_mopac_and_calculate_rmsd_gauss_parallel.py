#!/usr/bin/env python
__doc__ = \
"""

Calculate Root-mean-square deviation (RMSD) of Two Molecules Using Rotation
===========================================================================

Calculate Root-mean-square deviation (RMSD) between structure A and B, in XYZ
or PDB format, using transformation and rotation. The order of the atoms *must*
be the same for both structures.

For more information, usage, example and citation read more at
https://github.com/charnley/rmsd

"""

__version__ = '1.2.5'


import numpy as np
import re

import sys, os, operator, math
from joblib import Parallel, delayed
import multiprocessing as mp

R_CONST = 0.0083144598 # kJ/mol*K
T_CONST = 298.15 # K
RT_CONST = R_CONST*T_CONST

class Conformer:	 

   def __init__(self, filename):
   	self.filename = filename
   	self.ratio = 0.000
   	self.value = 0.000
   	self.diff = 0.000
	ind = 0
	file = open(filename, "r")
	for index, line in enumerate(file):
		if "FINAL HEAT OF FORMATION" in line:
			self.extractEnergy(line.rstrip('\n'))
			ind = 1
	if ind == 0:
		print "ERROR IN FILE: "+filename
		print "You must move the file somewhere else."
		print "						"
		exit()

   def extractEnergy(self, line):
   	self.lastscfenergy = float(line.rstrip('\n').split("=")[2].strip().split(" ")[0])
   	#print self.lastscfenergy
   	self.lastscfinkjpermole = self.lastscfenergy

   def convertHartreeTokJPerMole(self, value):
		return value*2625.500


class ConformerTools:

	def __init__(self, allConformers):
		self.listofenergies = []
		self.exponentofenergies = []
		for conf in allConformers:
			self.listofenergies.append(conf.lastscfinkjpermole)

		self.listofenergies.sort()
		self.lowestconfenergy = self.listofenergies[0]
		for conf in allConformers:
			self.exponentofenergies.append(math.exp( -(conf.lastscfinkjpermole-self.lowestconfenergy)/RT_CONST) )

		self.sumofenergyexponents = sum(self.exponentofenergies)

		for conf in allConformers:
			self.setRatio(conf)


	def setRatio(self, conf):
		value = 100*(math.exp( -(conf.lastscfinkjpermole-self.lowestconfenergy)/RT_CONST))/self.sumofenergyexponents
		conf.ratio = str(value) + "%"
		conf.value = value/100
		conf.diff = conf.lastscfinkjpermole-self.lowestconfenergy

		#return str(value) + "%"

	def convertHartreeTokJPerMole(self, value):
		return value*2625.500



# Python 2/3 compatibility
# Make range a iterator in Python 2
try:
	range = xrange
except NameError:
	pass


def kabsch_rmsd(P, Q):
	"""
	Rotate matrix P unto Q using Kabsch algorithm and calculate the RMSD.

	Parameters
	----------
	P : array
		(N,D) matrix, where N is points and D is dimension.
	Q : array
		(N,D) matrix, where N is points and D is dimension.

	Returns
	-------
	rmsd : float
		root-mean squared deviation
	"""
	P = kabsch_rotate(P, Q)
	return rmsd(P, Q)


def kabsch_rotate(P, Q):
	"""
	Rotate matrix P unto matrix Q using Kabsch algorithm.

	Parameters
	----------
	P : array
		(N,D) matrix, where N is points and D is dimension.
	Q : array
		(N,D) matrix, where N is points and D is dimension.

	Returns
	-------
	P : array
		(N,D) matrix, where N is points and D is dimension,
		rotated

	"""
	U = kabsch(P, Q)

	# Rotate P
	P = np.dot(P, U)
	return P


def kabsch(P, Q):
	"""
	The optimal rotation matrix U is calculated and then used to rotate matrix
	P unto matrix Q so the minimum root-mean-square deviation (RMSD) can be
	calculated.

	Using the Kabsch algorithm with two sets of paired point P and Q, centered
	around the centroid. Each vector set is represented as an NxD
	matrix, where D is the the dimension of the space.

	The algorithm works in three steps:
	- a translation of P and Q
	- the computation of a covariance matrix C
	- computation of the optimal rotation matrix U

	http://en.wikipedia.org/wiki/Kabsch_algorithm

	Parameters
	----------
	P : array
		(N,D) matrix, where N is points and D is dimension.
	Q : array
		(N,D) matrix, where N is points and D is dimension.

	Returns
	-------
	U : matrix
		Rotation matrix (D,D)

	Example
	-----
	TODO

	"""

	# Computation of the covariance matrix
	C = np.dot(np.transpose(P), Q)

	# Computation of the optimal rotation matrix
	# This can be done using singular value decomposition (SVD)
	# Getting the sign of the det(V)*(W) to decide
	# whether we need to correct our rotation matrix to ensure a
	# right-handed coordinate system.
	# And finally calculating the optimal rotation matrix U
	# see http://en.wikipedia.org/wiki/Kabsch_algorithm
	V, S, W = np.linalg.svd(C)
	d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

	if d:
		S[-1] = -S[-1]
		V[:, -1] = -V[:, -1]

	# Create Rotation matrix U
	U = np.dot(V, W)

	return U


def quaternion_rmsd(P, Q):
	"""
	Rotate matrix P unto Q and calculate the RMSD

	based on doi:10.1016/1049-9660(91)90036-O

	Parameters
	----------
	P : array
		(N,D) matrix, where N is points and D is dimension.
	P : array
		(N,D) matrix, where N is points and D is dimension.

	Returns
	-------
	rmsd : float
	"""
	rot = quaternion_rotate(P, Q)
	P = np.dot(P, rot)
	return rmsd(P, Q)


def quaternion_transform(r):
	"""
	Get optimal rotation
	note: translation will be zero when the centroids of each molecule are the
	same
	"""
	Wt_r = makeW(*r).T
	Q_r = makeQ(*r)
	rot = Wt_r.dot(Q_r)[:3, :3]
	return rot


def makeW(r1, r2, r3, r4=0):
	"""
	matrix involved in quaternion rotation
	"""
	W = np.asarray([
			 [r4, r3, -r2, r1],
			 [-r3, r4, r1, r2],
			 [r2, -r1, r4, r3],
			 [-r1, -r2, -r3, r4]])
	return W


def makeQ(r1, r2, r3, r4=0):
	"""
	matrix involved in quaternion rotation
	"""
	Q = np.asarray([
			 [r4, -r3, r2, r1],
			 [r3, r4, -r1, r2],
			 [-r2, r1, r4, r3],
			 [-r1, -r2, -r3, r4]])
	return Q


def quaternion_rotate(X, Y):
	"""
	Calculate the rotation

	Parameters
	----------
	X : array
		(N,D) matrix, where N is points and D is dimension.
	Y: array
		(N,D) matrix, where N is points and D is dimension.

	Returns
	-------
	rot : matrix
		Rotation matrix (D,D)
	"""
	N = X.shape[0]
	W = np.asarray([makeW(*Y[k]) for k in range(N)])
	Q = np.asarray([makeQ(*X[k]) for k in range(N)])
	Qt_dot_W = np.asarray([np.dot(Q[k].T, W[k]) for k in range(N)])
	W_minus_Q = np.asarray([W[k] - Q[k] for k in range(N)])
	A = np.sum(Qt_dot_W, axis=0)
	eigen = np.linalg.eigh(A)
	r = eigen[1][:, eigen[0].argmax()]
	rot = quaternion_transform(r)
	return rot


def centroid(X):
	"""
	Calculate the centroid from a vectorset X.

	https://en.wikipedia.org/wiki/Centroid
	Centroid is the mean position of all the points in all of the coordinate
	directions.

	C = sum(X)/len(X)

	Parameters
	----------
	X : array
		(N,D) matrix, where N is points and D is dimension.

	Returns
	-------
	C : float
		centeroid

	"""
	C = X.mean(axis=0)
	return C


def rmsd(V, W):
	"""
	Calculate Root-mean-square deviation from two sets of vectors V and W.

	Parameters
	----------
	V : array
		(N,D) matrix, where N is points and D is dimension.
	W : array
		(N,D) matrix, where N is points and D is dimension.

	Returns
	-------
	rmsd : float
		Root-mean-square deviation

	"""
	D = len(V[0])
	N = len(V)
	rmsd = 0.0
	for v, w in zip(V, W):
		rmsd += sum([(v[i] - w[i])**2.0 for i in range(D)])
	return np.sqrt(rmsd/N)


def write_coordinates(atoms, V, title=""):
	"""
	Print coordinates V with corresponding atoms to stdout in XYZ format.

	Parameters
	----------
	atoms : list
		List of atomic types
	V : array
		(N,3) matrix of atomic coordinates
	title : string (optional)
		Title of molecule

	"""
	N, D = V.shape

	print(str(N))
	print(title)

	for i in range(N):
		atom = atoms[i]
		atom = atom[0].upper() + atom[1:]
		print("{0:2s} {1:15.8f} {2:15.8f} {3:15.8f}".format(
				atom, V[i, 0], V[i, 1], V[i, 2]))


def get_coordinates(filename, fmt):
	"""
	Get coordinates from filename in format fmt. Supports XYZ and PDB.

	Parameters
	----------
	filename : string
		Filename to read
	fmt : string
		Format of filename. Either xyz or pdb.

	Returns
	-------
	atoms : list
		List of atomic types
	V : array
		(N,3) where N is number of atoms

	"""
	if fmt == "xyz":
		return get_coordinates_xyz(filename)
	elif fmt == "pdb":
		return get_coordinates_pdb(filename)
	exit("Could not recognize file format: {:s}".format(fmt))


def get_coordinates_pdb(filename):
	"""
	Get coordinates from the first chain in a pdb file
	and return a vectorset with all the coordinates.

	Parameters
	----------
	filename : string
		Filename to read

	Returns
	-------
	atoms : list
		List of atomic types
	V : array
		(N,3) where N is number of atoms

	"""
	# PDB files tend to be a bit of a mess. The x, y and z coordinates
	# are supposed to be in column 31-38, 39-46 and 47-54, but this is
	# not always the case.
	# Because of this the three first columns containing a decimal is used.
	# Since the format doesn't require a space between columns, we use the
	# above column indices as a fallback.
	x_column = None
	V = list()
	# Same with atoms and atom naming.
	# The most robust way to do this is probably
	# to assume that the atomtype is given in column 3.
	atoms = list()

	with open(filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			if line.startswith("TER") or line.startswith("END"):
				break
			if line.startswith("ATOM"):
				tokens = line.split()
				# Try to get the atomtype
				try:
					atom = tokens[2][0]
					if atom in ("H", "C", "N", "O", "S", "P"):
						atoms.append(atom)
					else:
						# e.g. 1HD1
						atom = tokens[2][1]
						if atom == "H":
							atoms.append(atom)
						else:
							raise Exception
				except:
						exit("Error parsing atomtype for the following line: \n{0:s}".format(line))

				if x_column == None:
					try:
						# look for x column
						for i, x in enumerate(tokens):
							if "." in x and "." in tokens[i + 1] and "." in tokens[i + 2]:
								x_column = i
								break
					except IndexError:
						exit("Error parsing coordinates for the following line: \n{0:s}".format(line))
				# Try to read the coordinates
				try:
					V.append(np.asarray(tokens[x_column:x_column + 3], dtype=float))
				except:
					# If that doesn't work, use hardcoded indices
					try:
						x = line[30:38]
						y = line[38:46]
						z = line[46:54]
						V.append(np.asarray([x, y ,z], dtype=float))
					except:
						exit("Error parsing input for the following line: \n{0:s}".format(line))


	V = np.asarray(V)
	atoms = np.asarray(atoms)
	assert(V.shape[0] == atoms.size)
	return atoms, V


def get_coordinates_xyz(filename):
	"""
	Get coordinates from filename and return a vectorset with all the
	coordinates, in XYZ format.

	Parameters
	----------
	filename : string
		Filename to read

	Returns
	-------
	atoms : list
		List of atomic types
	V : array
		(N,3) where N is number of atoms

	"""

	f = open(filename, 'r')
	V = list()
	atoms = list()
	n_atoms = 0

	# Read the first line to obtain the number of atoms to read
	try:
		n_atoms = int(f.readline())
	except ValueError:
		exit("Could not obtain the number of atoms in the .xyz file.")

	# Skip the title line
	f.readline()

	# Use the number of atoms to not read beyond the end of a file
	for lines_read, line in enumerate(f):

		if lines_read == n_atoms:
			break

		atom = re.findall(r'[a-zA-Z]+', line)[0]
		atom = atom.upper()

		numbers = re.findall(r'[-]?\d+\.\d*(?:[Ee][-\+]\d+)?', line)
		numbers = [float(number) for number in numbers]

		# The numbers are not valid unless we obtain exacly three
		if len(numbers) == 3:
			V.append(np.array(numbers))
			atoms.append(atom)
		else:
			exit("Reading the .xyz file failed in line {0}. Please check the format.".format(lines_read + 2))

	f.close()
	atoms = np.array(atoms)
	V = np.array(V)
	return atoms, V




class Result:	 

	def __init__(self, filename1, filename2):
		self.filename1 = filename1
		self.filename2 = filename2
		self.normal = 0
		self.kabsch = 0
		self.quater = 0


class Calculate:	

	def __init__(self, listofcalcs):
		self.listofcalcs = listofcalcs
		self.listofresults = []
		#print(zip([self]*len(self.listofcalcs), self.listofcalcs))
		#self.run()
		#res = Parallel(n_jobs=8)(delayed(self.run)(i) for i in self.listofcalcs)		

	def run(self):
		#res = Parallel(n_jobs=8)(delayed(self.f)(i) for i in zip([self]*len(self.listofcalcs), self.listofcalcs))
		p = mp.Pool(processes=8)
		res = p.map(unwrap_self_f, zip([self]*len(self.listofcalcs), self.listofcalcs))
		#print res.quater
		self.listofresults = list(res)
		

	def f(self, calc):
		structure_a = calc[0]
		structure_b = calc[1]
		# self.normal = 0
		# self.kabsch = 0
		# self.quater = 0
		file_format = structure_a.split('.')[-1]
		p_atoms, p_all = get_coordinates(structure_a, file_format)
		q_atoms, q_all = get_coordinates(structure_b, file_format)
		if np.count_nonzero(p_atoms != q_atoms):
			exit("Atoms not in the same order")

		P = p_all[:]
		Q = q_all[:]
		result = Result(structure_a, structure_b)
		result.normal = rmsd(P, Q)
		#print("Normal RMSD: {0}".format(result.normal))
		Pc = centroid(P)
		Qc = centroid(Q)
		P -= Pc
		Q -= Qc
		result.kabsch = kabsch_rmsd(P, Q)
		result.quater = quaternion_rmsd(P, Q)
		#print("Kabsch RMSD: {0}".format(result.kabsch))
		#print("Quater RMSD: {0} {1} {2}".format(result.quater, self.structure_a, self.structure_b))
		#self.listofresults.append(result)
		#print result.quater
		return result

	def results(self):
		return self.listofresults



def unwrap_self_f(arg, **kwarg):
    return Calculate.f(*arg, **kwarg)


def main(argv):
	import argparse
	import sys, getopt
	import os, operator
	import glob
	import shutil

	gauss_log = 0

	try:
		opts, args = getopt.getopt(argv,"g")
	except getopt.GetoptError:
		print 'conformers_from_mopac_and_calculate_rmsd_gauss_parallel.py'
		print '-g  jesli logi z gaussiana zamiast z mopaca'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-x":
			gauss_log = 1

	listofconformers = []
	error_conformers = []


	for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
		if file.endswith(".out"):
			# sprawdzenie czy nie ma bledu
			outfile = open(file, "r")
			for index, line in enumerate(outfile):
				if "NUMBER OF CYCLES EXCEEDED" in line:
					error_conformers.append(file)
					break
				if "JOB ENDED NORMALLY" in line:
					listofconformers.append(Conformer(file))
					break

	print error_conformers

	if len(error_conformers) > 0:
		current_folder_path = os.path.dirname(os.path.abspath(__file__))
		error_folder_path = os.path.dirname(os.path.abspath(__file__))+"/error"
		os.mkdir(error_folder_path)
		for file in error_conformers:
			file_current_path = current_folder_path + "/" + file
			file_new_path = error_folder_path + "/" + file
			shutil.move(file_current_path, file_new_path)
			shutil.move(file_current_path.split(".")[0]+".mop", file_new_path.split(".")[0]+".mop")
			shutil.move(file_current_path.split(".")[0]+".den", file_new_path.split(".")[0]+".den")
			shutil.move(file_current_path.split(".")[0]+".res", file_new_path.split(".")[0]+".res")
			shutil.move(file_current_path.split(".")[0]+".xyz", file_new_path.split(".")[0]+".xyz")
			shutil.move(file_current_path.split(".")[0]+".pbs", file_new_path.split(".")[0]+".pbs")
		sys.exit("Wykryto " + str(len(error_conformers)) + " plikow z bledem. Zostaly przekopiowane do folderu /error")


	listofconformers.sort(key=operator.attrgetter('lastscfenergy'))
	calculateConformers = ConformerTools(listofconformers)

	listoffiles = []

	for conf in listofconformers:
		if conf.diff < 22:
			listoffiles.append(conf.filename.split('.')[0]+".xyz")
			print conf.filename + "   :   " + str(conf.lastscfenergy) + "   :   " + str(conf.ratio) + "   :   " + str(conf.diff)
			command = "babel -imopout "+conf.filename+" -oxyz "+conf.filename.split(".")[0]+".xyz"
			os.system(command)
			command2 = "tail -n +3 "+conf.filename.split(".")[0]+".xyz"+" > "+conf.filename.split(".")[0]+".gjf"
			os.system(command2)
			command3 = "echo -en '\\n' >> "+conf.filename.split(".")[0]+".gjf"
			os.system(command3)


	listofcalcs = []

	count = len(listoffiles)
	print count

	for idx, val in enumerate(listoffiles):
		for x in listoffiles[idx+1:]:
			listofcalcs.append([val,x])
			#Calculate(val,x,listofresults)

	# for x in listofcalcs:
	# 	print x[0] + " - " + x[1]

	a = Calculate(listofcalcs)
	a.run()

	print a.listofresults.count

	

	filestoremove = []

	a.listofresults.sort(key=operator.attrgetter('quater'))
	print "Normal" + "\t:\t" + "Kabsch" + "\t:\t" + "Quater" + "\t:\t" + "File 1" + "\t:\t" + "File 2"
	for res in a.listofresults:		
		if res.quater < 1.5: 
			print str(res.normal) + "\t:\t" + str(res.kabsch) + "\t:\t" + str(res.quater) + "\t:\t" + str(res.filename1) + "\t:\t" + str(res.filename2)
			templistofconformers = []
			templistofconformers.append(Conformer(res.filename1.split(".")[0]+".out"))
			templistofconformers.append(Conformer(res.filename2.split(".")[0]+".out"))
			calculateConformers = ConformerTools(templistofconformers)
			for conf in templistofconformers:
				if conf.diff > 0: 
					if conf.filename not in filestoremove: filestoremove.append(conf.filename)

	print "FILES TO REMOVE: "+str(filestoremove)

	for file in filestoremove:
		command4 = "rm "+file.split(".")[0]+".xyz"
		os.system(command4)
		command5 = "rm "+file.split(".")[0]+".gjf"
		os.system(command5)

	for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
		if file.endswith(".gjf"):
			command6 = "mv "+file.split(".")[0]+".gjf"+" "+file.split(".")[0]+"_wB97XD_631gd.gjf"
			os.system(command6)
	# args = parser.parse_args()
	# print(args.structure_a)
	# print(args.structure_b)
	# calc = Calculate(args.structure_a,args.structure_b)



if __name__ == "__main__":
	main(sys.argv[1:])


#########################################################################################
##  scl enable python27 bash
#########################################################################################