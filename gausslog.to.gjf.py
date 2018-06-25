#!/usr/bin/python
import sys, os, getopt

class GaussianLog():

	def __init__(self, filename):
		self.filename = filename
		self.last_matrix = []
		self.where_are_matrices = []
		self.initial_matrix_position = 0
		self.file_content = []
		self.atoms = []
		self.number_of_atoms = 0
		self.final_matrix = []
		self.charge = 0
		self.multiplicity = 0
		self.calculation_commands = ""
		self.is_counterpoise = 0

		with open(self.filename, 'r') as file:
			self.file_content = file.readlines()

		for index, line in enumerate(self.file_content):
			if '#' in line: self.calculation_commands = line
			if 'Symbolic Z-matrix:' in line: self.initial_matrix_position = index+2
			if 'orientation:' in line: self.where_are_matrices.append(index+5)
			if 'Charge =' in line:
				self.charge = int(line.split("=")[1].split()[0])
				self.multiplicity = int(line.split("=")[2].split()[0])

		if 'counterpoise' or 'Counterpoise' in self.calculation_commands:
			self.is_counterpoise = 1
			self.initial_matrix_position = self.initial_matrix_position + 2

		self.atoms = self.get_atoms_from_initial_matrix()
		self.number_of_atoms = len(self.atoms)
		
		self.last_matrix = self.get_last_matrix()

		for index, coordinate in enumerate(self.last_matrix):			
			self.final_matrix.append([self.atoms[index]] + coordinate)

		self.save_gjf()


	def get_atoms_from_initial_matrix(self):
		result = []

		for line in self.file_content[self.initial_matrix_position:]:
			if len(line.strip()) == 0: break
			result.append(line.strip().split(" ")[0])
		return result		
	
	def get_last_matrix(self):
		result = []
		print self.where_are_matrices
		print self.number_of_atoms

		for line in self.file_content[self.where_are_matrices[-1]:self.where_are_matrices[-1]+self.number_of_atoms]:
			dash_count = line.count('-')
			print line
			if dash_count > 6: break
			linia = line.strip().split()
			filter(None, linia)			
			result.append([linia[3], linia[4], linia[5]])
		return result

	def save_gjf(self):
		gjf_file = []

		gjf_file.append("%chk=" + self.filename.split(".")[0] + ".chk\n")
		gjf_file.append("%mem=32GB\n")
		gjf_file.append("%nprocshared=24\n")
		gjf_file.append("# freq wB97XD/6-31g(d)\n")
		gjf_file.append("\n")
		gjf_file.append(self.filename + "\n")
		gjf_file.append("\n")
		gjf_file.append(str(self.charge) + " " + str(self.multiplicity) + "\n")
		
		for coordinate in self.final_matrix:			
			gjf_file.append(coordinate[0] + "\t\t\t" + coordinate[1] + "\t"+ coordinate[2] + "\t" + coordinate[3] + "\n")

		gjf_file.append("\n")

		with open(self.filename.split(".")[0]+'.gjf', 'w') as writefile:
			for line in gjf_file:
				writefile.write(line)



# class Matrix():

# 	def __init__(self, file_content, initial_matrix_position, where_are_matrices):
# 		self.file_content = file_content
# 		self.initial_matrix_position = initial_matrix_position
# 		self.where_are_matrices = where_are_matrices

# 	def get_atoms_from_initial_matrix(self):
# 		result = []

# 		for line in self.file_content[initial_matrix_position:]:
# 			if line in ['\n']: break
# 			result.append(line)
# 		return result


		


def main(argv):
	# try:
	# 	opts, args = getopt.getopt(argv,"hg:x",["guest="])
	# except getopt.GetoptError:
	# 	print 'cp_generator.py -g <guest atoms range XX-XX>'
	# 	sys.exit(2)
	# for opt, arg in opts:
	# 	if opt == '-h':
	# 		print 'cp_generator.py -g <guest atoms range XX-XX>'
	# 		sys.exit()
	# 	elif opt in ("-g", "--guest"):
	# 		atoms_range = arg
	# 	elif opt == "-x":
	# 		mgfc = 1
	# print atoms_range

	log_files = []
	for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
		if file.endswith(".log"):
			log_files.append(GaussianLog(file))

	# for file in counter_files:
	# 	print file.filename + " : " + str(file.second_blank_line)
	# 	with open(file.filename.split(".")[0]+'_FREQ_CP.gjf', 'w') as writefile:
	# 		for line in file.counter_filedata:
	# 			writefile.write(line)
	# 	with open(file.filename.split(".")[0]+'_MGFC.gjf', 'w') as writefile:
	# 		for line in file.mgfc_filedata:
	# 			writefile.write(line)
	# 	with open(file.filename.split(".")[0]+'_GFC.gjf', 'w') as writefile:
	# 		for line in file.gfc_filedata:
	# 			writefile.write(line)

if __name__ == "__main__":
   main(sys.argv[1:])

