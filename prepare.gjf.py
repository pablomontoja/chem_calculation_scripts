#!/usr/bin/python
import sys, os, getopt

class Gjf():

	def __init__(self, filename):
		self.file_content = []
		self.filename = filename
		self.final_filename = self.filename.split(".")[0] + "_dft"
		self.calculation_commands = ""
		self.where_are_matrix = 0
		# self.atoms = []
		# self.number_of_atoms = 0
		self.matrix = []
		
		
		
		
		
		self.charge = 0
		self.multiplicity = 0
		
		self.is_counterpoise = 0

		with open(self.filename, 'r') as file:
			self.file_content = file.readlines()

		for index, line in enumerate(self.file_content):
			if '#' in line: 
				self.calculation_commands = line
				self.where_are_matrix = index+5
			#if 'Symbolic Z-matrix:' in line: self.where_are_matrix = index+2
			#if 'orientation:' in line: self.where_are_matrix.append(index+5)
			#if 'Charge =' in line:
			#	self.charge = int(line.split("=")[1].split()[0])
			#	self.multiplicity = int(line.split("=")[2].split()[0])


		#self.atoms = self.get_atoms_from_initial_matrix()
		#self.number_of_atoms = len(self.atoms)
		
		self.matrix = self.get_matrix()

		# for index, coordinate in enumerate(self.matrix):			
		# 	self.matrix.append([self.atoms[index]] + coordinate)

		# print self.where_are_matrix

		self.save_new_gjf()



	def get_matrix(self):
		result = []

		for line in self.file_content[self.where_are_matrix:]:
			if len(line.strip()) == 0: break
			linia = line.strip().split()
			filter(None, linia)
			print linia
			result.append([linia[0], linia[1], linia[2], linia[3]])
		return result


	def save_new_gjf(self):
		gjf_file = []
		
		gjf_file.append("%rwf=" + self.final_filename + ".rwf\n")
		gjf_file.append("%chk=" + self.final_filename + ".chk\n")
		gjf_file.append("%mem=98GB\n")
		gjf_file.append("%nprocshared=24\n")
		# gjf_file.append("# m062x/GEN PSEUDO=READ opt(calcfc,ts,noeigen) freq\n")
		# gjf_file.append("# opt=modredundant m062x/3-21g*\n")   
		#gjf_file.append("# m062x/6-311g(d) opt freq\n")   
		# gjf_file.append("# m062x/6-311g(d) Integral(SuperFine) opt(calcfc,ts,noeigen) freq nosymm\n")
		gjf_file.append("# m062x/GEN PSEUDO=READ opt(ts,calcfc,noeigen) freq(noraman) scrf=(read,smd,solvent=toluene) nosymm\n")
		# gjf_file.append("# opt=modredundant m062x/3-21g*\n")  
		# gjf_file.append("# m062x/GEN PSEUDO=READ irc(MaxPoints=2)\n")
		# gjf_file.append("# m062x/GEN PSEUDO=READ pop(full,nbo)\n")
		# gjf_file.append("# m062x/6-311g(d) opt scrf=(read,smd,solvent=toluene) nosymm\n")
		gjf_file.append("\n")
		gjf_file.append(self.final_filename + "\n")
		gjf_file.append("\n")
		gjf_file.append("0 1" + "\n")
		
		for coordinate in self.matrix:			
			gjf_file.append(coordinate[0] + "\t\t\t" + coordinate[1] + "\t"+ coordinate[2] + "\t" + coordinate[3] + "\n")

		gjf_file.append("\n")

		##############################
		# gjf_file.append("I 0\n")
		# gjf_file.append("DEF2TZVP\n")
		# gjf_file.append("****\n")
		# gjf_file.append("C H N O 0\n")
		# gjf_file.append("6-311g(d)\n")
		# gjf_file.append("****\n")

		# gjf_file.append("\n")

		# gjf_file.append("I 0\n")
		# gjf_file.append("DEF2TZVP\n")

		# gjf_file.append("\n")
		# gjf_file.append("Radii=Bondi\n")
		gjf_file.append("Surface=sas\n")
		# gjf_file.append("B 7 1 S 8 -0.170000\n")
		gjf_file.append("\n")
		gjf_file.append("\n")
		###############################

		with open(self.final_filename+'.gjf', 'w') as writefile:
			for line in gjf_file:
				writefile.write(line)





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
		if file.endswith(".gjf"):
			print file[0]
			log_files.append(Gjf(file))


if __name__ == "__main__":
   main(sys.argv[1:])

