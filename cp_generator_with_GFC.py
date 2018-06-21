#!/usr/bin/python
import sys, os, getopt

class GaussianFile:

	def __init__(self, filename):
		#super(GaussianFile, self).__init__()
		self.filename = filename
		self.filedata = []
		self.counter_filedata = []
		self.mgfc_filedata = []
		self.gfc_filedata = []
		self.first_blank_line = 0
		self.second_blank_line = 0
		self.third_blank_line = 0
		self.gfc_matrix = []
		self.mgfc_matrix = []

		#file = open(filename, "r")
		with open(self.filename, 'r') as file:
			self.filedata = file.readlines()

		#znajdowanie pustych linii
		x = 0
		i = 0		
		for line in self.filedata:
			if line in ['\n']:
				x = x + 1
				if x == 1: self.first_blank_line = i
				if x == 2: self.second_blank_line = i
				if x == 3: self.third_blank_line = i
			i = i + 1
		#print matrix data
		# y = 1
		# first_atom = int(atoms_range.split("-")[0])
		# last_atom = int(atoms_range.split("-")[1])
		# print first_atom
		# print last_atom
		# for line in self.filedata[self.second_blank_line:self.third_blank_line-2]:
		# 	if first_atom-1 >= y <= last_atom:
		# 		self.filedata[self.second_blank_line+y+1] = self.filedata[self.second_blank_line+y+1].rstrip() + " 1\n"
		# 	else:
		# 		self.filedata[self.second_blank_line+y+1] = self.filedata[self.second_blank_line+y+1].rstrip() + " 2\n"
		# 	y = y + 1
		# self.filedata[self.first_blank_line-1] = self.filedata[self.first_blank_line-1].rstrip() + " Counterpoise=2\n"
		# print self.filedata[self.first_blank_line-1]
		# self.filedata[self.second_blank_line+1] = "1 1 0 1 1 1\n"
		# print self.filedata[self.second_blank_line+1]

	def counterpoiseFile(self, atoms_range):
		self.counter_filedata = list(self.filedata)
		y = 1
		first_atom = int(atoms_range.split("-")[0])
		last_atom = int(atoms_range.split("-")[1])
		# print first_atom
		# print last_atom
		begin_of_matrix = self.second_blank_line+2
		end_of_matrix = self.third_blank_line
		index = 1
		for x in range(begin_of_matrix, end_of_matrix):
			if first_atom <= index <= last_atom:
				self.gfc_matrix.append(self.counter_filedata[x])
				self.counter_filedata[x] = self.counter_filedata[x].rstrip() + " 2\n"						
			else:
				self.mgfc_matrix.append(self.counter_filedata[x])
				self.counter_filedata[x] = self.counter_filedata[x].rstrip() + " 1\n"
			index += 1
		# for line in self.counter_filedata[self.second_blank_line:self.third_blank_line-2]:
		# 	print line
		# 	if first_atom-1 >= y <= last_atom:
		# 		self.counter_filedata[self.second_blank_line+y+1] = self.counter_filedata[self.second_blank_line+y+1].rstrip() + " 1\n"
		# 	else:
		# 		self.counter_filedata[self.second_blank_line+y+1] = self.counter_filedata[self.second_blank_line+y+1].rstrip() + " 2\n"
		# 	y = y + 1
		self.counter_filedata[self.first_blank_line-1] = self.counter_filedata[self.first_blank_line-1].rstrip() + " Counterpoise=2\n"
		# print self.counter_filedata[self.first_blank_line-1]
		self.counter_filedata[self.second_blank_line+1] = "1 1 0 1 1 1\n"
		# print self.counter_filedata[self.second_blank_line+1]

	def mgfcFile(self, atoms_range):
		first_atom = int(atoms_range.split("-")[0])
		last_atom = int(atoms_range.split("-")[1])
		cut_position = self.second_blank_line + 2
		self.mgfc_filedata = list(self.filedata)[:cut_position]
		self.mgfc_filedata[0] = "%chk=" + self.filename.split(".")[0] + '_MGFC.chk' + "\n"
		self.mgfc_filedata[self.second_blank_line+1] = "0 1\n"
		self.mgfc_filedata = self.mgfc_filedata + self.mgfc_matrix
		self.mgfc_filedata.append("\n")
		if "freq" not in self.mgfc_filedata[self.first_blank_line-1]:
			self.mgfc_filedata[self.first_blank_line-1] = self.mgfc_filedata[self.first_blank_line-1].rstrip() + " freq\n"

	def gfcFile(self, atoms_range):
		first_atom = int(atoms_range.split("-")[0])
		last_atom = int(atoms_range.split("-")[1])
		# cut_position1 = self.second_blank_line + 2
		# cut_position2 = first_atom + self.second_blank_line + 1
		cut_position = self.second_blank_line + 2
		self.gfc_filedata = list(self.filedata)[:cut_position]
		# self.gfc_filedata = list(self.filedata)[:cut_position1] + list(self.filedata)[cut_position2:]
		self.gfc_filedata[0] = "%chk=" + self.filename.split(".")[0] + '_GFC.chk' + "\n"
		self.gfc_filedata[self.second_blank_line+1] = "1 1\n"
		self.gfc_filedata = self.gfc_filedata + self.gfc_matrix
		self.gfc_filedata.append("\n")
		if "freq" not in self.gfc_filedata[self.first_blank_line-1]:
			self.gfc_filedata[self.first_blank_line-1] = self.gfc_filedata[self.first_blank_line-1].rstrip() + " freq\n"



def main(argv):
	atoms_range = ""
	mgfc = 0
	try:
		opts, args = getopt.getopt(argv,"hg:x",["guest="])
	except getopt.GetoptError:
		print 'cp_generator.py -g <guest atoms range XX-XX>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'cp_generator.py -g <guest atoms range XX-XX>'
			sys.exit()
		elif opt in ("-g", "--guest"):
			atoms_range = arg
		elif opt == "-x":
			mgfc = 1
	print atoms_range


	counter_files = []
	for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
		if file.endswith(".gjf"):
			gf = GaussianFile(file)
			gf.counterpoiseFile(atoms_range)
			gf.mgfcFile(atoms_range)
			gf.gfcFile(atoms_range)
			counter_files.append(gf)

	for file in counter_files:
		print file.filename + " : " + str(file.second_blank_line)
		with open(file.filename.split(".")[0]+'_CP.gjf', 'w') as writefile:
			for line in file.counter_filedata:
				writefile.write(line)
		with open(file.filename.split(".")[0]+'_MGFC.gjf', 'w') as writefile:
			for line in file.mgfc_filedata:
				writefile.write(line)
		with open(file.filename.split(".")[0]+'_GFC.gjf', 'w') as writefile:
			for line in file.gfc_filedata:
				writefile.write(line)
		command = "rm "+file.filename
		os.system(command)

if __name__ == "__main__":
	main(sys.argv[1:])