#!/usr/bin/python
import sys, os, getopt

class GaussianFile:

	def __init__(self, filename, atoms_range):
		#super(GaussianFile, self).__init__()
		self.filename = filename
		self.filedata = []
		self.first_blank_line = 0
		self.second_blank_line = 0
		self.third_blank_line = 0

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
		y = 1
		first_atom = int(atoms_range.split("-")[0])
		last_atom = int(atoms_range.split("-")[1])
		print first_atom
		print last_atom
		for line in self.filedata[self.second_blank_line:self.third_blank_line-2]:
			if first_atom-1 >= y <= last_atom:
				self.filedata[self.second_blank_line+y+1] = self.filedata[self.second_blank_line+y+1].rstrip() + " 1\n"
			else:
				self.filedata[self.second_blank_line+y+1] = self.filedata[self.second_blank_line+y+1].rstrip() + " 2\n"
			y = y + 1
		self.filedata[self.first_blank_line-1] = self.filedata[self.first_blank_line-1].rstrip() + " Counterpoise=2\n"
		print self.filedata[self.first_blank_line-1]
		self.filedata[self.second_blank_line+1] = "1 1 0 1 1 1\n"
		print self.filedata[self.second_blank_line+1]



def main(argv):
	atoms_range = ""
	try:
		opts, args = getopt.getopt(argv,"hg:",["guest="])
	except getopt.GetoptError:
		print 'cp_generator.py -g <guest atoms range XX-XX>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'cp_generator.py -g <guest atoms range XX-XX>'
			sys.exit()
		elif opt in ("-g", "--guest"):
			atoms_range = arg
	print atoms_range


	files = []
	for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
		if file.endswith(".gjf"):
			files.append(GaussianFile(file,atoms_range))

	for file in files:
		print file.filename + " : " + str(file.second_blank_line)
		with open(file.filename.split(".")[0]+'_CP.gjf', 'w') as writefile:
			for line in file.filedata:
				writefile.write(line)

if __name__ == "__main__":
   main(sys.argv[1:])